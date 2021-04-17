## PubSub Publisher

To run on the Raspberry Pis, collect sensor data and add them to the PubSub queue

NOTE: execute commands from datalogger folder

#### 1. Create service account for datalogger publisher

```
gcloud iam service-accounts create datalogger-pub
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-pub@environment-data.iam.gserviceaccount.com" --role="roles/pubsub.publisher"
gcloud iam service-accounts keys create pubsub/serviceaccount-datalogger-pub.json --iam-account=datalogger-pub@environment-data.iam.gserviceaccount.com
```

#### 2. Run publisher with environment variable

```
GOOGLE_APPLICATION_CREDENTIALS="pubsub/serviceaccount-datalogger-pub.json" python pubsub/pub.py
```
