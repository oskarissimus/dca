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

# Quickstart guide

## 1. Prerequisites

1. Create project in gcp
2. Install gcloud cli
3. Login into gcloud
   ```bash
   gcloud auth application-default login
   ```
4. Set env var for future use
   ```bash
   export PROJECT_ID=<your project id here>
   ```
5. Set default project
   ```bash
   gcloud config set project $PROJECT_ID
   ```
6. Enable crucial services for terraform to work
   ```bash
   gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com
   ```

## 2. Setup service account and credentials

```bash
gcloud service-account create terraform
export SA=terraform@$PROJECT_ID.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA" --role="roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account=$SA
```

## 3. Setup terraform

1. Create `terraform.tfvars` file based on `variables.tf` file. Fill in all required values.
2. `terraform init`
3. Enable all required services before building resources. There is [known issue](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/google_project_service#newly-activated-service-errors) that enabling services doesnt happen instantly, and there is no way to verify it, so explicit sleep 60s is added, so we wont be annoyed by any errors `terraform apply -target=module.project-services && sleep 60`

## 4. Deploy cloud function and other resources

```bash
terraform apply
```

## 5. Profit
