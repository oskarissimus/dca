resource "google_project_service" "secretmanager" {
  provider = google
  service  = "secretmanager.googleapis.com"
}

resource "google_project_service" "cloudfunctions" {
  provider = google
  service  = "cloudfunctions.googleapis.com"
}

resource "google_project_service" "cloudbuild" {
  provider = google
  service  = "cloudbuild.googleapis.com"
}

resource "google_project_service" "iam" {
  provider = google
  service  = "iam.googleapis.com"
}

resource "google_project_service" "containerregistry" {
  provider = google
  service  = "containerregistry.googleapis.com"
}

resource "google_project_service" "cloudscheduler" {
  provider = google
  service  = "cloudscheduler.googleapis.com"
}

resource "google_project_service" "pubsub" {
  provider = google
  service  = "pubsub.googleapis.com"
}

resource "google_project_service" "logging" {
  provider = google
  service  = "logging.googleapis.com"
}

resource "google_project_service" "cloudapis" {
  provider = google
  service  = "cloudapis.googleapis.com"
}

resource "google_project_service" "cloudresourcemanager" {
  provider = google
  service  = "cloudresourcemanager.googleapis.com"
}
