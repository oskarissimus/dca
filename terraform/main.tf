terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = "europe-central2"
}
