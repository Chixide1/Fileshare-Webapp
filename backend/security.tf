resource "azuread_application" "fileshareapp-name" {
  display_name = "Fileshare-Webapp"
}

resource "azuread_service_principal" "fileshareapp-sp" {
  depends_on = [ azuread_application.fileshareapp-name ]
  client_id = azuread_application.fileshareapp-name.client_id
}

resource "azuread_service_principal_password" "client_secret" {
  depends_on = [ azuread_service_principal.fileshareapp-sp ]
  service_principal_id = azuread_service_principal.fileshareapp-sp.object_id
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
