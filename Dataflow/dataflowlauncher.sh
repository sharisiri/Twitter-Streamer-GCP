# If you're on an M1 Mac - Run this on Colaboratory instead to avoid dependency hell. Upload Creds.json and beamtwittersentiment.py and make sure to reference them correctly before launching.

!python3 beamtwittersentiment.py \
    --project "<YOUR_PROJECT_ID>" \
    --input_topic "projects/<PROJECT_ID>/subscriptions/<YOUR_PUBSUB_SUBSCRIPTION>" \
    --runner DataflowRunner \
    --staging_location "gs://<YOUR_BEAM_BUCKET>/stg" \
    --temp_location "gs://YOUR_BEAM_BUCKET/temp" \
    --region europe-north1 \
    --save_main_session True \
    --streaming \
    --max_num_workers 1