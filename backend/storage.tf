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