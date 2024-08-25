resource "google_service_account" "function" {
  account_id = "function"
}

resource "google_secret_manager_secret_iam_binding" "bindings" {
  for_each  = google_secret_manager_secret.secrets
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    data.google_compute_default_service_account.default.member,
    google_service_account.function.member
  ]
}



data "google_compute_default_service_account" "default" {}
output "dupa" {
  value = google_secret_manager_secret_iam_binding.bindings

}
