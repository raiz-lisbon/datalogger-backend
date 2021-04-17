## Cloud Function

To retrieve messages from PubSub queue and add them to BigQuery

NOTE: execute commands from datalogger folder

NOTE 2: PubSub might deliver messages multiple times!

### 1. LOCAL DEV ONLY

#### 1.1 Create service account for datalogger publisher

```
gcloud iam service-accounts create datalogger-sub
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-sub@environment-data.iam.gserviceaccount.com" --role="roles/pubsub.subscriber"
gcloud iam service-accounts keys create functions/serviceaccount-datalogger-sub.json --iam-account=datalogger-sub@environment-data.iam.gserviceaccount.com
```

#### 1.2 LOCAL DEV ONLY: Run subscribe with environment variable

```
GOOGLE_APPLICATION_CREDENTIALS="functions/serviceaccount-datalogger-sub.json" python functions/sub.py
```
