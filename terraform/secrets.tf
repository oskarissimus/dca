variable "secrets" {
  type = set(string)
  default = [
    "xtb_user_id",
    "xtb_password",
    "zonda_api_key",
    "zonda_api_secret"
  ]
}

resource "google_secret_manager_secret" "secrets" {
  for_each  = var.secrets
  secret_id = each.key

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "versions" {
  for_each    = google_secret_manager_secret.secrets
  secret      = each.value.id
  secret_data = var.xtb_user_id
}

