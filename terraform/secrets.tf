# xtb_user_id
resource "google_secret_manager_secret" "xtb_user_id" {
  depends_on = [google_project_service.secretmanager]
  secret_id  = "xtb_user_id"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "xtb_user_id" {
  depends_on  = [google_project_service.secretmanager]
  secret      = google_secret_manager_secret.xtb_user_id.id
  secret_data = var.xtb_user_id
}

# xtb_password
resource "google_secret_manager_secret" "xtb_password" {
  depends_on = [google_project_service.secretmanager]
  secret_id  = "xtb_password"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "xtb_password" {
  depends_on  = [google_project_service.secretmanager]
  secret      = google_secret_manager_secret.xtb_password.id
  secret_data = var.xtb_password
}

# zonda_api_key
resource "google_secret_manager_secret" "zonda_api_key" {
  depends_on = [google_project_service.secretmanager]
  secret_id  = "zonda_api_key"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "zonda_api_key" {
  depends_on  = [google_project_service.secretmanager]
  secret      = google_secret_manager_secret.zonda_api_key.id
  secret_data = var.zonda_api_key
}

# zonda_api_secret
resource "google_secret_manager_secret" "zonda_api_secret" {
  depends_on = [google_project_service.secretmanager]
  secret_id  = "zonda_api_secret"

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "zonda_api_secret" {
  depends_on  = [google_project_service.secretmanager]
  secret      = google_secret_manager_secret.zonda_api_secret.id
  secret_data = var.zonda_api_secret
}
