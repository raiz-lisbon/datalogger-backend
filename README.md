### 1. Python Virtual Environment

#### 1.1 To activate:

```
source venv/bin/activate
```

#### 1.2 To verify it's activated:

```
which python
```

Should output `./venv/bin/python`

### 2. gcloud CLI

#### 2.1 Set project

```
gcloud config set project environment-data
```

#### 2.2 Create PubSub topic (if doesn't exist)

```
gcloud pubsub topics create datalogger
```

#### 2.3 Create subscription (if doesn't exist)

```
gcloud pubsub subscriptions create datalogger-sub --topic datalogger --enable-message-ordering
```
