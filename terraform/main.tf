terraform {
  backend "azurerm" {
    resource_group_name  = "tfstates"
    storage_account_name = "tfstates220614"
    container_name       = "tfstate"
    key                  = "tfstate.tfstate"
  }
}

provider "archive" {
  
}

provider "azurerm" {
  features {}
}

locals {
  local_api_zip_name = "electricity-prices-${formatdate("YYYY-MM-DD-hh-mm-ss", timestamp())}.zip"
}

data "archive_file" "zipfile" {
  type = "zip"
  output_path = "../api/${local.local_api_zip_name}"
  source_dir = "../api"
}

resource "azurerm_resource_group" "electricity-prices-rg" {
  name     = "electricity-prices-rg"
  location = "North Europe"
}

resource "azurerm_storage_account" "electricity-prices-sa" {
  name                     = "epstorageaccount220614"
  resource_group_name      = azurerm_resource_group.electricity-prices-rg.name
  location                 = azurerm_resource_group.electricity-prices-rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "ep-app-service-plan" {
  name                     = "ep-app-service-plan"
  resource_group_name      = azurerm_resource_group.electricity-prices-rg.name
  location                 = azurerm_resource_group.electricity-prices-rg.location
  os_type                  = "Linux"
  sku_name                 = "Y1"
}

resource "azurerm_linux_function_app" "electricity-prices-app" {
  name                = "electricity-prices-app-220614"
  resource_group_name      = azurerm_resource_group.electricity-prices-rg.name
  location                 = azurerm_resource_group.electricity-prices-rg.location

  storage_account_name       = azurerm_storage_account.electricity-prices-sa.name
  storage_account_access_key = azurerm_storage_account.electricity-prices-sa.primary_access_key
  service_plan_id            = azurerm_service_plan.ep-app-service-plan.id

  app_settings = {
      "WEBSITE_RUN_FROM_PACKAGE" = "https://${azurerm_storage_account.electricity-prices-sa.name}.blob.core.windows.net/${azurerm_storage_container.api.name}/${azurerm_storage_blob.function_blob.name}${data.azurerm_storage_account_blob_container_sas.blob_container_sas.sas}"
      APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.app-insights.connection_string
      AZURE_STORAGE_CONNECTION_STRING = azurerm_storage_account.electricity-prices-sa.primary_connection_string
    }

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }
}

resource "azurerm_storage_container" "api" {
  name = "api"
  storage_account_name = azurerm_storage_account.electricity-prices-sa.name
}

resource "azurerm_storage_blob" "function_blob" {
  name = local.local_api_zip_name
  storage_account_name = azurerm_storage_account.electricity-prices-sa.name
  storage_container_name = azurerm_storage_container.api.name
  type = "Block"
  source = "../api/${local.local_api_zip_name}"
}

data "azurerm_storage_account_blob_container_sas" "blob_container_sas" {
  connection_string = azurerm_storage_account.electricity-prices-sa.primary_connection_string
  container_name = azurerm_storage_container.api.name

  start = "2023-01-01T00:00:00Z"
  expiry = "2025-01-01T00:00:00Z"

  permissions {
    read = true
    add = false
    create = false
    write = false
    delete = false
    list = false
  }
}

resource "azurerm_log_analytics_workspace" "log-analytics-workspace" {
  name                = "log-analytics-workspace"
  resource_group_name      = azurerm_resource_group.electricity-prices-rg.name
  location                 = azurerm_resource_group.electricity-prices-rg.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "app-insights" {
  name                = "appinsights"
  resource_group_name      = azurerm_resource_group.electricity-prices-rg.name
  location                 = azurerm_resource_group.electricity-prices-rg.location
  workspace_id        = azurerm_log_analytics_workspace.log-analytics-workspace.id
  application_type    = "web"
}
