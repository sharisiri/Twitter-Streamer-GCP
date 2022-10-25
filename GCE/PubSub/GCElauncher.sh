#1 To launch VM instance and spin up tweetstreamer.py
gcloud compute instances create <VM_NAME> \
--project=<YOUR_PROJECT_ID> \
--zone=<YOUR_ZONE> \
--machine-type=<INSTANCE_TYPE> \
--service-account=<SERVICE_ACCOUNT_EMAIL> \
--create-disk=auto-delete=yes,boot=yes,device-name=<VM-NAME>,image=projects/debian-cloud/global/images/debian-11-bullseye-v20220920,mode=rw,size=10 \
--metadata=startup-script-url=gs://<YOUR_GCS_BUCKET>/startup-script.sh

#2 To check output from VM without SSH-ing in.
gcloud compute instances get-serial-port-output <VM_NAME> \
--zone=<YOUR_ZONE>


#3 M1 Mac Apache Beam dependency hell: Launch your Beam Instance from Colaboratory. Upload Creds.json and beamtwittersentiment.py and make sure to reference them correctly before launching.
!pip install httplib2==0.15.0
!pip install google-api-python-client==1.6
!pip install google-cloud-language==1.3.0

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