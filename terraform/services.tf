resource "google_project_service" "secretmanager" {
  provider           = google
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudfunctions" {
  provider           = google
  service            = "cloudfunctions.googleapis.com"
  depends_on         = [google_project_service.logging]
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  provider           = google
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam" {
  provider           = google
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "containerregistry" {
  provider           = google
  service            = "containerregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudscheduler" {
  provider           = google
  service            = "cloudscheduler.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "pubsub" {
  provider           = google
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "logging" {
  provider           = google
  service            = "logging.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudapis" {
  provider           = google
  service            = "cloudapis.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute" {
  provider           = google
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudresourcemanager" {
  provider           = google
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "serviceusage" {
  provider           = google
  service            = "serviceusage.googleapis.com"
  disable_on_destroy = false
}

