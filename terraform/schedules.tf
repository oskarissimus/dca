resource "google_cloud_scheduler_job" "buy_snp500_every_minute" {
  name      = "buy_snp500_every_minute"
  schedule  = "* * * * *"
  time_zone = "Europe/Warsaw"
  paused    = true
  region    = var.region
  pubsub_target {
    topic_name = google_pubsub_topic.buy_market.id
    data       = filebase64(var.buy_snp500_command_file)
  }
}
