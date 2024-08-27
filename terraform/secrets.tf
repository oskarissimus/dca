resource "google_secret_manager_secret" "xtb_user_id" {
  secret_id = "xtb_user_id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "xtb_user_id" {
  secret      = google_secret_manager_secret.xtb_user_id.id
  secret_data = var.xtb_user_id
}

resource "google_secret_manager_secret" "xtb_password" {
  secret_id = "xtb_password"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "xtb_password" {
  secret      = google_secret_manager_secret.xtb_password.id
  secret_data = var.xtb_password
}

resource "google_secret_manager_secret" "zonda_api_key" {
  secret_id = "zonda_api_key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "zonda_api_key" {
  secret      = google_secret_manager_secret.zonda_api_key.id
  secret_data = var.zonda_api_key
}

resource "google_secret_manager_secret" "zonda_api_secret" {
  secret_id = "zonda_api_secret"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "zonda_api_secret" {
  secret      = google_secret_manager_secret.zonda_api_secret.id
  secret_data = var.zonda_api_secret
}
