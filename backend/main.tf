# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.91.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "fileshare-webapp"
  location = var.default_location
}

resource "azuread_application" "fileshareapp-name" {
  display_name = "Fileshare-Webapp"
}

resource "azuread_service_principal" "fileshareapp-sp" {
  client_id = azuread_application.fileshareapp-name.client_id
}

resource "azuread_service_principal_password" "client_secret" {
  service_principal_id = azuread_service_principal.fileshareapp-sp.object_id
}

resource "azurerm_storage_account" "sa" {
  name                     = "chikfilesharewebappsa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.default_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                  = "upload"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "azurerm_key_vault" "kv" {
  name = "chik-fileshare-key-vault"
  location = var.default_location
  resource_group_name = azurerm_resource_group.rg.name
  sku_name = "standard"
  tenant_id = "380c0008-0574-46d2-8938-093fa0b5de50"
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Set",
      "Get",
      "Delete",
      "Purge",
      "Recover"
    ]
  }

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azuread_service_principal.fileshareapp-sp.object_id
    
    secret_permissions = [
      "Get"
    ]
  }
}

resource "azurerm_key_vault_secret" "kv-sakey" {
  name         = "fileshare-sa-key"
  value        = azurerm_storage_account.sa.primary_access_key
  key_vault_id = azurerm_key_vault.kv.id
}

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
  }
}

resource "azurerm_app_service_source_control" "code_source" {
  app_id   = azurerm_linux_web_app.linux-wa.id
  repo_url = "https://github.com/Chixide1/Fileshare-Webapp"
  branch   = "main"
  use_manual_integration = true
}

resource "azurerm_storage_management_policy" "purgepol" {
  storage_account_id = azurerm_storage_account.sa.id

  rule {
    name    = "uploadpurge"
    enabled = true
    filters {
      blob_types   = ["blockBlob"]
      prefix_match = ["upload/"]
    }
    actions {
        base_blob {
          delete_after_days_since_creation_greater_than = 2
        }
      }
    }
}

resource "azurerm_log_analytics_workspace" "log_workspace" {
  name                = "fileshare-workspace"
  location            = var.default_location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_monitor_diagnostic_setting" "storage_logs" {
  name               = "storage_logs"
  target_resource_id = "${azurerm_storage_account.sa.id}/blobServices/default/"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_workspace.id

  enabled_log {
    category_group = "alllogs"
  }
}