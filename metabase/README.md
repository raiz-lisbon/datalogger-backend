### 1. Deploy Metabase to Heroku

### 2. Create service account for Metabase

```
gcloud iam service-accounts create datalogger-metabase
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-metabase@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-metabase@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.jobUser"
gcloud projects add-iam-policy-binding environment-data --member="serviceAccount:datalogger-metabase@environment-data.iam.gserviceaccount.com" --role="roles/bigquery.metadataViewer"
gcloud iam service-accounts keys create metabase/serviceaccount-datalogger-metabase.json --iam-account=datalogger-metabase@environment-data.iam.gserviceaccount.com
```
