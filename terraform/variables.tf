variable "region" { default = "europe-central2" }
variable "xtb_user_id" {}
variable "xtb_password" {}
variable "xtb_api_port" {}
variable "zonda_api_key" {}
variable "zonda_api_secret" {}
variable "schedules_paused" {
  type    = bool
  default = true
}
variable "schedules" {
  type = map(object({
    exchange_name     = string
    symbol            = string
    desired_value_pln = number
    schedule          = string
  }))

  default = {
    buy_btc_twice_a_day = {
      exchange_name     = "zonda"
      symbol            = "BTC-PLN"
      desired_value_pln = 6
      schedule          = "0 10,22 * * *"
    }
  }
}
