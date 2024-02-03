variable "default_location" {
  type = string
  default = "uksouth"
  description = "The location I will use for all resources"
}

resource "random_password" "password" {
  length = 30
  special = true
  override_special = "!#$%&*()_=+^<>:?"
}