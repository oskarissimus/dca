# Bootstrap configuration for Terraform state bucket
# Run this ONCE manually before initializing the main terraform configuration:
#   cd terraform/bootstrap
#   terraform init
#   terraform apply
#
# After the bucket is created, initialize the main config:
#   cd ..
#   terraform init -migrate-state

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
  }
}

variable "region" {
  default = "europe-central2"
}

data "google_project" "default" {}

provider "google" {
  project = "dca-2025"
  region  = var.region
}

resource "google_storage_bucket" "tfstate" {
  name     = "${data.google_project.default.project_id}-tfstate"
  location = var.region

  # Prevent accidental deletion
  force_destroy = false

  # Enable versioning to recover from accidental state corruption
  versioning {
    enabled = true
  }

  # Uniform bucket-level access for simpler IAM
  uniform_bucket_level_access = true

  # Lifecycle rule to clean up old versions after 30 days
  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }
    action {
      type = "Delete"
    }
  }
}

output "bucket_name" {
  value       = google_storage_bucket.tfstate.name
  description = "The name of the Terraform state bucket"
}
