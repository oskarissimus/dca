# 💸 DCA

Dollar-cost averaging for xtb and zonda. Made with 🐍 Python and 🌐 Terraform on ☁️ GCP.

## Setup

If you know your way around Terraform and GCP, here is a quick guide to get you started. If you are new to Terraform, GCP, or both, please refer to the detailed guide below.

### 🚀 Quickstart Guide

1. Create `terraform.tfvars` file based on `variables.tf`
2. `terraform init`
3. `terraform apply -target=module.project-services`
4. Wait some time for services to be enabled
5. `terraform apply`
6. Enjoy

### Detailed Guide

#### 1. 🛠️ Prerequisites

1. Create project in GCP
2. Install gcloud CLI
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
6. Enable crucial services for Terraform to work
   ```bash
   gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com
   ```

#### 2. 🔐 Setup Service Account and Credentials

```bash
gcloud service-account create terraform
export SA=terraform@$PROJECT_ID.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA" --role="roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account=$SA
```

#### 3. 🔧 Setup Terraform

1. Create `terraform.tfvars` file based on `variables.tf` file. Fill in all required values.
2. `terraform init`
3. Enable all required services before building resources. There is a [known issue](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/google_project_service#newly-activated-service-errors) that enabling services doesn’t happen instantly, and there is no way to verify it, so explicit sleep 60s is added, so we won’t be annoyed by any errors `terraform apply -target=module.project-services && sleep 60`

#### 4. 🚀 Deploy Cloud Function and Other Resources

```bash
terraform apply
```

#### 5. 💰 Profit

## 🏗️ Architecture

Cloud function is a central point of this system. It is written in python with 2 API clients (xtb and zonda). Those clients are built by a factory function. There is also a cloud scheduler that periodicaly sends predefined message to pubsub that triggers the cloud function.

## 🔧 Configuration

There are 2 places to interact with this bot

1. json files in `terraform/commands/` dir
2. schedules in `terraform/schedules.tf` file

Contents of JSON files are sent to pubsub on a given schedule.

### Adding new schedule

Just copy some existing schedule inside `terraform/schedules.tf` and adjust its values. You might also want to create new JSON file with some other amounts, symbols or markets and reference it in new schedule.

### Modifying command

Commands are JSON objects with 3 keys as in example below

```json
{
  "exchange_name": "zonda",
  "symbol": "BTC-PLN",
  "desired_value_pln": 6
}
```

- currently valid `exchange_name` are `"zonda"` `"xtb"`
- `symbol` can be anything that given exchange supports
- `desired_value_pln` speaks for itself - number of units to buy will be determined by `desired_value_pln / price`

### Modyfing schedule

Each schedule is technically `google_cloud_scheduler_job` as in example below:

```terraform
resource "google_cloud_scheduler_job" "buy_btc_twice_a_day" {
  name      = "buy_btc_twice_a_day"
  schedule  = "0 10,22 * * *"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_btc_command_file)
  }
}
```

There are 3 important things here

- `name` (in this case `buy_btc_twice_a_day`) - something unique
- `schedule` - cron expression (in this case `"0 10,22 * * *"`)
- `data`
