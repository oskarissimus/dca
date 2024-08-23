resource "google_service_account" "function" {
  account_id = "function"
  depends_on = [google_project_service.iam]
}

resource "google_secret_manager_secret_iam_binding" "function_xtb_user_id" {
  secret_id = google_secret_manager_secret.xtb_user_id.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members   = ["serviceAccount:${google_service_account.function.email}"]
}

resource "google_secret_manager_secret_iam_binding" "function_xtb_password" {
  secret_id = google_secret_manager_secret.xtb_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members   = ["serviceAccount:${google_service_account.function.email}"]
}

resource "google_secret_manager_secret_iam_binding" "function_zonda_api_key" {
  secret_id = google_secret_manager_secret.zonda_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members   = ["serviceAccount:${google_service_account.function.email}"]
}

resource "google_secret_manager_secret_iam_binding" "function_zonda_api_secret" {
  secret_id = google_secret_manager_secret.zonda_api_secret.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members   = ["serviceAccount:${google_service_account.function.email}"]
}
