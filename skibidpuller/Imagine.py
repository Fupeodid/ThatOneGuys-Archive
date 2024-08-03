import requests
import json
import playfab
from playfab import PlayFabSettings, PlayFabClientAPI
import random

# Set up a proxy if needed (can be removed if not required)
proxies = {'http': 'http://36.91.68.150:8080'}

# Generate a random ID for the CustomID
randomthing = random.randint(0, 69000)
thing = {"CustomId": f"OCULUS{randomthing}", "CreateAccount": True}

# Prompt user for PlayFab Title ID and Developer Secret Key
PlayFabTitleID = input("Title ID: ")
DeveloperSecretKey = input("Developer Secret Key: ")
PlayFabSettings.TitleId = PlayFabTitleID

def callback(success, failure):
    if success:
        print("Congratulations, you made your first successful API call!")
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure.GenerateErrorReport())

# Perform login with Custom ID
PlayFabClientAPI.LoginWithCustomID(callback=callback, request=thing)

# Endpoint and headers for GetCatalogItems API call
get_catalog_items_endpoint = f"https://{PlayFabTitleID}.playfabapi.com/Client/GetCatalogItems"
headers = {
    "Content-Type": "application/json",
    "X-PlayFabSDK": "PlayFabSDK/2.94.210118",
    "X-Authorization": PlayFabSettings._internalSettings.ClientSessionTicket,
    "X-SecretKey": DeveloperSecretKey
}

# Making the request to GetCatalogItems API
response = requests.post(get_catalog_items_endpoint, json=thing, headers=headers, proxies=proxies)
if response.status_code != 200:
    print(f"Request failed with status code {response.status_code}")
    print(response.content)
else:
    # Parse the response
    response_json = response.json()
    catalog = response_json.get('data', {}).get('Catalog', [])
    print(catalog)
    with open(f"{PlayFabTitleID}_catalog.json", "w") as outfile:
        json.dump(catalog, outfile)

# Additional step to get currency code information
get_currency_endpoint = f"https://{PlayFabTitleID}.playfabapi.com/Server/GetUserInventory"
response = requests.post(get_currency_endpoint, headers=headers, proxies=proxies)
if response.status_code != 200:
    print(f"Currency request failed with status code {response.status_code}")
    print(response.content)
else:
    response_json = response.json()
    currency = response_json.get('data', {}).get('VirtualCurrency', {})
    print(currency)
    with open(f"{PlayFabTitleID}_currency.json", "w") as outfile:
        json.dump(currency, outfile)
