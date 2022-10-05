resource "google_cloud_scheduler_job" "buy_snp500_every_tuesday" {
  name      = "buy_snp500_every_tuesday"
  schedule  = "0 15 * * 2"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_snp500_command_file)
  }
}

resource "google_cloud_scheduler_job" "buy_usa_bonds_every_weekday" {
  name      = "buy_usa_bonds_every_weekday"
  schedule  = "0 14 * * 1-5"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_usa_bonds_command_file)
  }
}

resource "google_cloud_scheduler_job" "buy_btc_twice_a_day" {
  name      = "buy_btc_twice_a_day"
  schedule  = "0 10,22 * * *"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_btc_command_file)
  }
}

resource "google_cloud_scheduler_job" "buy_eth_twice_a_day" {
  name      = "buy_eth_twice_a_day"
  schedule  = "30 10,22 * * *"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_eth_command_file)
  }
}

resource "google_cloud_scheduler_job" "buy_ltc_twice_a_day" {
  name      = "buy_ltc_twice_a_day"
  schedule  = "15 10,22 * * *"
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_ltc_command_file)
  }
}
