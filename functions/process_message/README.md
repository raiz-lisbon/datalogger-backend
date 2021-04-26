## Cloud Function

To retrieve messages from PubSub queue and add them to BigQuery

NOTE: execute commands from datalogger folder

NOTE 2: PubSub might deliver messages multiple times!

### 1. LOCAL DEV ONLY

#### 1.1 Create service account for datalogger publisher

```
gcloud iam service-accounts create datalogger-sub
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-sub@environment-data.iam.gserviceaccount.com" --role="roles/pubsub.subscriber"
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-sub@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-sub@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.jobUser"
gcloud iam service-accounts keys create serviceaccount-datalogger-sub.json --iam-account=datalogger-sub@environment-data.iam.gserviceaccount.com
```

#### 1.2 LOCAL DEV ONLY: Run subscribe with environment variable

From `functions/process_message` folder:

```
GOOGLE_APPLICATION_CREDENTIALS="serviceaccount-datalogger-sub.json" functions-framework --target=process_message --signature-type=event
```

### 2. Deploy Cloud Function

From `datalogger` folder:

```
gcloud functions deploy process_message --source functions/process_message --entry-point process_message --runtime python38 --trigger-topic datalogger --memory 128MB --max-instances 3
```
