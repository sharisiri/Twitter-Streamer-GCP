#! /bin/bash
cd /home/$USER
apt -qq update
apt-get install -yq python3 python3-pip
gsutil cp gs://<YOUR_BEAM_BUCKET>/pubsub_creds.json .
gsutil cp gs://<YOUR_BEAM_BUCKET>/requirements.txt .
gsutil cp gs://<YOUR_BEAM_BUCKET>/tweetstreamer.py .
pip3 install -r requirements.txt
python3 tweetstreamer.py