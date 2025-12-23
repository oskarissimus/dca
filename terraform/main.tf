terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
  }

  backend "gcs" {
    bucket = "dca-2025-tfstate"
    prefix = "terraform/state"
  }
}

data "google_project" "default" {}

provider "google" {
  project = "dca-2025"
  region  = var.region
}
