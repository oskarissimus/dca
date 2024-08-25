resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project}-function"
  location = var.region
}

resource "google_storage_bucket_iam_member" "builder" {
  bucket = google_storage_bucket.function_bucket.name
  role   = "roles/storage.admin"
  member = google_service_account.function_builder.member
}
