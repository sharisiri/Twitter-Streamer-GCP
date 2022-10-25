#1 To launch VM instance and spin up tweetstreamer.py
gcloud compute instances create <VM_NAME> \
--project=<YOUR_PROJECT_ID> \
--zone=<YOUR_ZONE> \
--machine-type=<INSTANCE_TYPE> \
--service-account=<SERVICE_ACCOUNT_EMAIL> \
--create-disk=auto-delete=yes,boot=yes,device-name=<VM-NAME>,image=projects/debian-cloud/global/images/debian-11-bullseye-v20220920,mode=rw,size=10 \
--metadata=startup-script-url=gs://<BUCKET_NAME>/startup-script.sh

#2 To check output from VM without SSH-ing in.
gcloud compute instances get-serial-port-output <VM_NAME> \
--zone=<YOUR_ZONE>