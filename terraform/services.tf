module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 15.0"

  project_id                  = var.project
  disable_services_on_destroy = false

  activate_apis = [
    "secretmanager.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudscheduler.googleapis.com",
    "pubsub.googleapis.com",
    "logging.googleapis.com",
    "cloudapis.googleapis.com",
    "compute.googleapis.com",
  ]
}
