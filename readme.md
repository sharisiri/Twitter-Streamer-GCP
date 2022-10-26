# Twitter Streamer GCP

## Introduction

This repo contains the source code for the writeup on how to build a streaming pipeline in GCP using the Twitter API, GCE, Pub / Sub, Dataflow, and BigQuery.

![Twitter Sentiment Streaming Pipeline](https://user-images.githubusercontent.com/37027404/197961365-78ae53aa-4e08-48f1-aab2-31eeed5c1b05.png)

## Set up

Clone the repo to your local environment. Follow the steps in the article and save the necessery credentials and files to the local repo:

```
git clone https://github.com/sharisiri/twitter-streamer-GCP.git
cd twitter-streamer-GCP
code .
```
Install the necessary Dataflow dependencies:
```
pip install ‘apache-beam[gcp]’
pip install google-cloud-language==2.6.1
```
Modify the credentials in beamtwittersentiment.py and then run:
```
python3 beamtwittersentiment.py \
    --project "<YOUR_PROJECT_ID>" \
    --input_topic "projects/<PROJECT_ID>/subscriptions/<YOUR_PUBSUB_SUBSCRIPTION>" \
    --runner DataflowRunner \
    --staging_location "gs://<YOUR_BEAM_BUCKET>/stg" \
    --temp_location "gs://YOUR_BEAM_BUCKET/temp" \
    --region europe-north1 \
    --save_main_session True \
    --streaming \
    --max_num_workers 1
```
Upload GCE files to storage bucket via gsutil or cloud console:

```
gsutil cp pubsub_creds.json gs://<BUCKET_NAME>/ \
gsutil cp tweetstreamer.py gs://<BUCKET_NAME>/ \
gsutil cp requirements.txt gs://<BUCKET_NAME>/
```
Start Compute Engine and Tweet streamer script:
```
gcloud compute instances create <VM_NAME> \
--project=<YOUR_PROJECT_ID> \
--zone=<YOUR_ZONE> \
--machine-type=<INSTANCE_TYPE> \
--service-account=<SERVICE_ACCOUNT_EMAIL> \
--create-disk=auto-delete=yes,boot=yes,device-name=<VM-NAME>,image=projects/debian-cloud/global/images/debian-11-bullseye-v20220920,mode=rw,size=10 \
--metadata=startup-script-url=gs://<BUCKET_NAME>/startup-script.sh
```

Check BigQuery after a minte or two and confirm that tweets are stored correctly.
