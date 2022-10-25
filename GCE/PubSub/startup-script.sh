#! /bin/bash
cd /home/$USER
apt -qq update
apt-get install -yq python3 python3-pip
gsutil cp gs://<BUCKET_NAME>/pubsub_creds.json .
gsutil cp gs://<BUCKET_NAME>/requirements.txt .
gsutil cp gs://<BUCKET_NAME>/tweetstreamer.py .
pip3 install -r requirements.txt
python3 tweetstreamer.py