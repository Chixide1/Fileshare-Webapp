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

resource "random_password" "db_pass" {
  length = 10
  special = true
  override_special = "!#$%&*()_=+^<>:?"
}

resource "local_file" "env_file" {
  content = <<EOF
    AZURE_CLIENT_ID = ${azuread_service_principal.fileshareapp-sp.client_id}
    AZURE_CLIENT_SECRET = ${azuread_service_principal_password.client_secret.value}
    AZURE_TENANT_ID = ${data.azurerm_client_config.current.tenant_id}
    KV_URI = ${azurerm_key_vault.kv.vault_uri}
    DJANGO_SECRET_KEY = ${random_password.password.result}
    ACCOUNT_URL = ${azurerm_storage_account.sa.primary_blob_endpoint}
    DB_PASS = ${random_password.db_pass.result}
  EOF

  filename = "../.env"
}