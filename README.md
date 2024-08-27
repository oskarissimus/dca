# 💸 DCA

Dollar-cost averaging for xtb and zonda. Made with 🐍 Python and 🌐 Terraform on ☁️ GCP.

## Cost

I chose Google Cloud Platform (GCP) because, contrary to what you might think, it is actually more cost-effective. The paid resources include:

- **Pub/Sub**: Inexpensive due to the small number of messages.
- **Cloud Functions**: Affordable because of the low number of executions.
- **Cloud Scheduler**: Cost-effective given the minimal number of scheduled tasks.

Since cloud services charge based on usage, my specific needs - purchasing some cryptocurrency six times a day and other assets a couple of times a month - resulted in a monthly cost of approximately 3 PLN, which is very cheap. I opted for this setup because the alternative would have been running my own VPS with a constant cron job, which would have been at least ten times more expensive.

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
3. Go to terraform dir `cd terraform`
4. Login into gcloud
   ```bash
   gcloud auth application-default login
   ```
5. Set env var for future use
   ```bash
   export PROJECT_ID=<your project id here>
   ```
6. Set default project
   ```bash
   gcloud config set project $PROJECT_ID
   ```
7. Enable crucial services for Terraform to work
   ```bash
   gcloud services enable serviceusage.googleapis.com cloudresourcemanager.googleapis.com
   ```
8. Set quota project
   ```bash
   gcloud auth application-default set-quota-project $PROJECT_ID
   ```

#### 2. 🔐 Setup Service Account and Credentials

```bash
gcloud iam service-accounts create terraform
export SA=terraform@$PROJECT_ID.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA" --role="roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account=$SA
```

#### 3. 🔧 Setup Terraform

1. Create `terraform.tfvars` file based on `variables.tf` file. Fill in all required values.
2. Initialize Terraform

   ```bash
   terraform init
   ```

3. Enable all required services before building resources. There is a [known issue](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/google_project_service#newly-activated-service-errors) that enabling services doesn’t happen instantly, and there is no way to verify it, so explicit sleep 60s is added, so we won’t be annoyed by any errors
   ```bash
   terraform apply -target=module.project-services && sleep 60
   ```

#### 4. 🚀 Deploy Cloud Function and Other Resources

```bash
terraform apply
```

#### 5. 💰 Profit

## 🏗️ Architecture

Cloud function is a central point of this system. It is written in python with 2 API clients (xtb and zonda). Those clients are built by a factory function. There is also a cloud scheduler that periodicaly sends predefined message to pubsub that triggers the cloud function.

## 🔧 Configuration

Schedules are defined in `terraform.tfvars` file in format as in example below:

```terraform
schedules = {
  buy_btc_twice_a_day = {
    exchange_name     = "zonda"
    symbol            = "BTC-PLN"
    desired_value_pln = 6
    schedule          = "0 10,22 * * *"
  }
}
```

- currently valid `exchange_name` are `"zonda"` `"xtb"`
- `symbol` can be anything that given exchange supports
- `desired_value_pln` speaks for itself - number of units to buy will be determined by `desired_value_pln / price`
- `schedule` - cron expression (in this case `"0 10,22 * * *"`)

To add new schedule, just add new key-value pair to `schedules` map.

## Zonda API

Required API permission is **Zarządzanie zamówieniami i zmiana konfiguracji rynku**

## Screenshots
### Deployed schedule
![Deployed schedule](https://github.com/user-attachments/assets/14f689e9-93ed-4bf7-8479-aa6ac099c67c)

### Deployed cloud function
![Deployed cloud function](https://github.com/user-attachments/assets/9ff00a81-00c2-4497-a6b3-317ec989a15f)


