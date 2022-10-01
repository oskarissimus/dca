terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.38.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = "europe-central2"
}

resource "google_pubsub_topic" "buy_market" {
  name = "buy_market"
}

resource "google_cloud_scheduler_job" "buy_snp500_every_minute" {
  name      = "buy_snp500_every_minute"
  schedule  = "* * * * *"
  time_zone = "Europe/Warsaw"
  paused    = true
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_snp500_command_file)
  }
}
