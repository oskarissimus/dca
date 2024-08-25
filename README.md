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

### 1. 🛠️ Prerequisites

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

## 2. 🔐 Setup Service Account and Credentials

```bash
gcloud service-account create terraform
export SA=terraform@$PROJECT_ID.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA" --role="roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account=$SA
```

## 3. 🔧 Setup Terraform

1. Create `terraform.tfvars` file based on `variables.tf` file. Fill in all required values.
2. `terraform init`
3. Enable all required services before building resources. There is a [known issue](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/google_project_service#newly-activated-service-errors) that enabling services doesn’t happen instantly, and there is no way to verify it, so explicit sleep 60s is added, so we won’t be annoyed by any errors `terraform apply -target=module.project-services && sleep 60`

## 4. 🚀 Deploy Cloud Function and Other Resources

```bash
terraform apply
```

## 5. 💰 Profit
