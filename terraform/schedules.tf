resource "google_cloud_scheduler_job" "schedule" {
  for_each  = var.schedules
  name      = each.key
  schedule  = each.value.schedule
  time_zone = "Europe/Warsaw"
  paused    = var.schedules_paused
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data = base64encode(jsonencode({
      exchange_name     = each.value.exchange_name
      symbol            = each.value.symbol
      desired_value_pln = each.value.desired_value_pln
    }))
  }
}

