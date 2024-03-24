resource "azurerm_service_plan" "app-sp" {
  name                = "Fileshare-webapp-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.default_location
  os_type             = "Linux"
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "linux-wa" {
  name                = "chik-fileshare-webapp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.default_location
  service_plan_id     = azurerm_service_plan.app-sp.id
  https_only = true

  site_config {
    always_on = false

    application_stack {
      python_version = 3.11
    }
  }

  app_settings = {
    AZURE_CLIENT_ID = azuread_service_principal.fileshareapp-sp.client_id
    AZURE_CLIENT_SECRET = azuread_service_principal_password.client_secret.value
    AZURE_TENANT_ID = data.azurerm_client_config.current.tenant_id
    KV_URI = azurerm_key_vault.kv.vault_uri
    DJANGO_SECRET_KEY = random_password.password.result
    ACCOUNT_URL = azurerm_storage_account.sa.primary_blob_endpoint
    DB_PASS = random_password.db_pass.result
  }
}

resource "azurerm_app_service_source_control" "code_source" {
  app_id   = azurerm_linux_web_app.linux-wa.id
  repo_url = "https://github.com/Chixide1/Fileshare-Webapp"
  branch   = "main"
  use_manual_integration = true
}