# Electricity prices

*Work in progress*

Individual exercise using Azure Function App and publishing infrastructure to Azure using Terraform and Github Actions. 

Hourly electricity market prices are fetched from an API and uploaded to Azure Storage Container.

## Azure Functions

### UploadPricesToStorageContainer
A timer trigger function that fetches prices from an [API](https://api.porssisahko.net/v1/latest-prices.json) every day at 14:00 when they are updated. Uploads prices to storage container called `prices` in Azure Storage Account.

### FetchAveragePrice

A HTTP trigger function that fetches an average of prices within a given time period. `START_TIME` and `END_TIME` are given as query parameters.