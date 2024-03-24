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