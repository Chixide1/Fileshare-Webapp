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

resource "azurerm_postgresql_server" "example" {
  name                = "ck-django-db"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku_name = "B_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "chik"
  administrator_login_password = random_password.db_pass.result
  version                      = "9.5"
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_database" "example" {
  name                = "main"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.example.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}