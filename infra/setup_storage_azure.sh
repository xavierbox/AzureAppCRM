#!/usr/bin/env bash


set -a 
source .env 
set +a 
RESOURCE_GROUP="rg-launcher-uksouth"
LOCATION="uksouth"
STORAGE_ACCOUNT="launcherstacc899"   # must be globally unique
#CONTAINER_NAME="data"
QUEUE_NAME="queue-launcher-uksouth" 
UPLOAD_QUEUE_NAME2="process-uploads-queue"

 


#az group create \
#  --name "$RESOURCE_GROUP" \
#  --location "$LOCATION"


#az storage account create \
#  --name "$STORAGE_ACCOUNT" \

#  --resource-group "$RESOURCE_GROUP" \
#  --location "$LOCATION" \
#  --sku Standard_LRS

#az storage container create \
#  --account-name "$STORAGE_ACCOUNT" \
#  --name "$CONTAINER_NAME" \
#  --auth-mode login


 

#SUBSCRIPTION_ID="c36500b2-3b71-4639-8f0e-5d4814910cf4"
#az account set --subscription "$SUBSCRIPTION_ID"

#USER_UPN=$(az account show --query user.name -o tsv)
#USER_OBJECT_ID=$(az ad signed-in-user show --query id) 
#az role assignment create --role "Storage Blob Data Contributor" \
#--assignee-principal-type User \
#--assignee-object-id "$USER_OBJECT_ID" --scope "$STORAGE_ACCOUNT"   


#az storage queue create --account-name "$STORAGE_ACCOUNT" --name "$QUEUE_NAME" --auth-mode login 
#az storage queue create --account-name "$STORAGE_ACCOUNT" --name "$QUEUE_NAME" --auth-mode login 
az storage queue create --account-name "$STORAGE_ACCOUNT" --name "$UPLOAD_QUEUE_NAME" --auth-mode login
