
#!/usr/bin/env python
import argparse
import json
import os
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import re

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<YOUR_CREDS.JSON_FILE>"
INPUT_SUBSCRIPTION = "projects/<PROJECT_ID>/subscriptions/<YOUR_PUBSUB_SUBSCRIPTION>"
BIGQUERY_TABLE = "<PROJECT_ID>:<DATASET_ID>.<TABLE_NAME>"
BIGQUERY_SCHEMA = "text:STRING, id:STRING, created_at:STRING, timestamp:TIMESTAMP, tweet:STRING, sentiment_score:FLOAT, magnitude_score:FLOAT"


class CustomParsing(beam.DoFn):
    """ Custom ParallelDo class to apply a custom transformation """

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def process(self, element: bytes, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam):
        # Super important to keep this import here and not at the top.
        from google.cloud import language_v1
        parsed = json.loads(element.decode("utf-8"))
        text = parsed["text"]
        # Removes website URLs
        text = re.sub('http://\S+|https://\S+', '', text)
        # Removes mentions
        text = re.sub(r"@[A-Za-z0-9]+", "", text)
        # Removes mentions where username has underscores
        text = re.sub(r"@[A-Za-z0-9]+_", "", text)
        # Removes hashtags
        text = re.sub(r"#[A-Za-z0-9]+", "", text)
        # Removes punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Removes retweets
        text = text.replace("RT", "")
        text = text.lower()
        text = text.strip()
        parsed["tweet"] = text
        parsed["timestamp"] = timestamp.to_rfc3339()

        # Instantiates the Language API client
        client = language_v1.LanguageServiceClient()
        # Analyzes the input text
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects sentiment
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        parsed["sentiment_score"] = sentiment.score
        parsed["magnitude_score"] = sentiment.magnitude

        yield parsed


def run():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_subscription",
        help='Input PubSub subscription of the form "projects/<PROJECT_ID>/subscriptions/<YOUR_PUBSUB_SUBSCRIPTION>."',
        default=INPUT_SUBSCRIPTION,
    )
    parser.add_argument(
        "--output_table", help="Output BigQuery Table", default=BIGQUERY_TABLE
    )
    parser.add_argument(
        "--output_schema",
        help="Output BigQuery Schema in text format",
        default=BIGQUERY_SCHEMA,
    )
    known_args, pipeline_args = parser.parse_known_args()

    # Creating pipeline options
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True

    # Defining our pipeline and its steps
    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "ReadFromPubSub" >> beam.io.gcp.pubsub.ReadFromPubSub(
                subscription=known_args.input_subscription, timestamp_attribute=None
            )
            | "CustomParse" >> beam.ParDo(CustomParsing())
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                known_args.output_table,
                schema=known_args.output_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )


if __name__ == "__main__":
    run()
