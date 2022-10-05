variable "project" {}
variable "region" {}
variable "credentials_file" {}
variable "xtb_user_id" {}
variable "xtb_password" {}
variable "xtb_api_port" {}
variable "zonda_api_key" {}
variable "zonda_api_secret" {}
variable "buy_snp500_command_file" {}
variable "buy_usa_bonds_command_file" {}
variable "buy_btc_command_file" {}
variable "buy_eth_command_file" {}
variable "buy_ltc_command_file" {}
variable "schedules_paused" {
  type    = bool
  default = true
}
