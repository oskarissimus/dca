# dca

dollar-cost averaging dla s&p 500 na platformie xtb

1. znaleźć dokumentację dla API XTB
2. założyć konto na sandboxie XTB
3. odpalić jakiegoś requesta w jupyter notebook
4. tworzenie zlecenia przez API
5. przygotować dane zlecenia które ma się tworzyć
6. napisać skrypt korzystający z apscheduler który kupuje co minutę jednostkę CSPX S&P500

```
gcloud functions deploy dca-xtb-function \
--gen2 \
--region=europe-central2 \
--runtime=python310 \
--source=. \
--entry-point=kupuj \
--trigger-topic=buy_on_xtb \
--env-vars-file=.env.yaml
```

```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

```
gcloud scheduler jobs update pubsub buy_usa_bonds_daily \
    --location=europe-central2 \
    --schedule="0 14 * * 1-5" \
    --topic=buy_on_xtb \
    --message-body='{"symbol": "IBTA.UK", "volume": 6}'
```

```
# co tydzień we wtorek do 21 dnia miesiąca - czyli co tydzień trzy razy w miesiącu
gcloud scheduler jobs update pubsub buy_snp500_three_times_a_month \
    --location=europe-central2 \
    --schedule="30 14 1-21 * 2" \
    --topic=buy_on_xtb \
    --message-body='{"symbol": "CSPX.UK_9", "volume": 1}'
```

```
gcloud pubsub topics publish buy_on_xtb --message='{"symbol": "IBTA.UK", "volume": 6}'
```

# messages to implement

```
{"exchange_name": "zonda", "symbol": "BTC-PLN", "desired_value_pln": 6}
{"exchange_name": "zonda", "symbol": "LTC-PLN", "desired_value_pln": 6}
{"exchange_name": "zonda", "symbol": "ETH-PLN", "desired_value_pln": 6}
{"exchange_name": "xtb", "symbol": "CSPX.UK", "desired_value_pln": 2000}
{"exchange_name": "xtb", "symbol": "IBTA.UK", "desired_value_pln": 150}
```

# get roles for specific user

```
gcloud projects get-iam-policy <YOUR GCLOUD PROJECT>  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:<YOUR SERVICE ACCOUNT>"
```

# roles for terraform user

```
roles/cloudfunctions.admin
roles/cloudscheduler.admin
roles/iam.securityAdmin
roles/iam.serviceAccountUser
roles/pubsub.admin
roles/secretmanager.admin
roles/serviceusage.serviceUsageAdmin
roles/storage.admin
```

# quickstart guide

1. create project in gcp
2. install gcloud cli
3. `gcloud auth application-default login`
4. `gcloud config set project PROJECT_ID`
5. `gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com`
6. `gcloud service-account create terraform`
7. `gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:terraform@PROJECT_ID.iam.gserviceaccount.com" --role="roles/owner"`
8. `gcloud iam service-accounts keys create credentials.json --iam-account=terraform@dca-2138.iam.gserviceaccount.com`
9. `terraform init`
10. `terraform apply`
