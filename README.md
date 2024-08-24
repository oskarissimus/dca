# DCA

Dollar-cost averaging for xtb and zonda. Made with python and terraform on gcp.

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

# Scratchpad

```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
