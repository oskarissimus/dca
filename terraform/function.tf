data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function.zip"
}

resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"

  name   = "src-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
}

resource "google_cloudfunctions_function" "function" {
  name                  = "buy_market"
  runtime               = "python38"
  entry_point           = "buy_market"
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.buy_market.id
  }

  timeout = 120
  timeouts {
    create = "2m"
    update = "2m"
    delete = "2m"
  }

  service_account_email = google_service_account.function.email

  secret_environment_variables {
    key     = "XTB_USER_ID"
    secret  = google_secret_manager_secret.xtb_user_id.secret_id
    version = "latest"
  }

  secret_environment_variables {
    key     = "XTB_PASSWORD"
    secret  = google_secret_manager_secret.xtb_password.secret_id
    version = "latest"
  }

  secret_environment_variables {
    key     = "ZONDA_API_KEY"
    secret  = google_secret_manager_secret.zonda_api_key.secret_id
    version = "latest"
  }

  secret_environment_variables {
    key     = "ZONDA_API_SECRET"
    secret  = google_secret_manager_secret.zonda_api_secret.secret_id
    version = "latest"
  }

  environment_variables = {
    XTB_API_PORT = var.xtb_api_port
  }
  depends_on = [
    google_secret_manager_secret_version.xtb_password,
    google_secret_manager_secret_version.xtb_user_id,
    google_secret_manager_secret_version.zonda_api_key,
    google_secret_manager_secret_version.zonda_api_secret,
    google_secret_manager_secret_iam_binding.function_xtb_password,
    google_secret_manager_secret_iam_binding.function_xtb_user_id,
    google_secret_manager_secret_iam_binding.function_zonda_api_key,
    google_secret_manager_secret_iam_binding.function_zonda_api_secret,
  ]
}

