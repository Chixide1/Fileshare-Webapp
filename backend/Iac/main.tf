# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "fileshare-webapp"
  location = var.default_location
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

resource "azurerm_service_plan" "app-sp" {
  name                = "Fileshare-webapp-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.default_location
  os_type             = "Linux"
  sku_name            = "F1"
}

# resource "azurerm_linux_web_app" "linux-wa" {
#   name                = "fileshare-webapp"
#   resource_group_name = azurerm_resource_group.rg.name
#   location            = var.default_location
#   service_plan_id     = azurerm_service_plan.app-sp.id

#   site_config {}
# }