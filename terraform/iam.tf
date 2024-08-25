resource "google_service_account" "function" {
  account_id = "function"
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

resource "google_service_account_iam_member" "gce-default-account-iam" {
  service_account_id = data.google_service_account.terraform.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.function.email}"
}

data "google_service_account" "terraform" {
  account_id = "terraform"
}

data "google_compute_default_service_account" "default" {}
