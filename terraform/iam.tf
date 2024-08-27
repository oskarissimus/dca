resource "google_service_account" "function_runner" {
  account_id = "function-runner"
}
resource "google_service_account" "function_builder" {
  account_id = "function-builder"
}

resource "google_secret_manager_secret_iam_binding" "xtb_user_id" {
  secret_id = google_secret_manager_secret.xtb_user_id.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    google_service_account.function_runner.member,
    google_service_account.function_builder.member
  ]
}

resource "google_secret_manager_secret_iam_binding" "xtb_password" {
  secret_id = google_secret_manager_secret.xtb_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    google_service_account.function_runner.member,
    google_service_account.function_builder.member
  ]
}

resource "google_secret_manager_secret_iam_binding" "zonda_api_key" {
  secret_id = google_secret_manager_secret.zonda_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    google_service_account.function_runner.member,
    google_service_account.function_builder.member
  ]
}

resource "google_secret_manager_secret_iam_binding" "zonda_api_secret" {
  secret_id = google_secret_manager_secret.zonda_api_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    google_service_account.function_runner.member,
    google_service_account.function_builder.member
  ]
}

resource "google_project_iam_member" "builder_artifact_registry_writer" {
  project = var.project
  role    = "roles/artifactregistry.writer"
  member  = google_service_account.function_builder.member
}

resource "google_project_iam_member" "builder_storage_object_admin" {
  project = var.project
  role    = "roles/storage.objectAdmin"
  member  = google_service_account.function_builder.member
}

resource "google_project_iam_member" "builder_logging_writer" {
  project = var.project
  role    = "roles/logging.logWriter"
  member  = google_service_account.function_builder.member
}
