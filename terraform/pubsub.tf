resource "google_pubsub_topic" "buy_market" {
  depends_on = [google_project_service.pubsub]
  name       = "buy_market"
}
