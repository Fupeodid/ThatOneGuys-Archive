import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

SECRET_KEY = "ZF68567XC5PWMASJTWEGO6QY1FUO8JPHBWY7H5T94IP43P1YDZ"
SEGMENT_ID = "4D925F1C89C36B1B"
BASE_URL = "https://FEA18.playfabapi.com/Admin"
MAX_CONCURRENT_REQUESTS = 10

def fetch_players(token):
    url = f"{BASE_URL}/GetPlayersInSegment"
    headers = {
        "Content-Type": "application/json",
        "X-SecretKey": SECRET_KEY
    }
    data = {
        "SegmentId": SEGMENT_ID,
        "ContinuationToken": token
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def delete_player(player_id):
    url = f"{BASE_URL}/DeletePlayer"
    headers = {
        "Content-Type": "application/json",
        "X-SecretKey": SECRET_KEY
    }
    data = {
        "PlayFabId": player_id
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return player_id

def main():
    token = ""
    while token is not None:
        response_data = fetch_players(token)
        player_ids = [player["PlayerId"] for player in response_data["data"]["PlayerProfiles"]]

        for i in range(0, len(player_ids), 100):
            batch = player_ids[i:i + 100]
            print(f"Deleting batch of {len(batch)} players")

            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
                futures = {executor.submit(delete_player, player_id): player_id for player_id in batch}
                for future in as_completed(futures):
                    try:
                        player_id = future.result()
                        print(f"Successfully deleted player: {player_id}")
                    except Exception as e:
                        print(f"Error deleting player: {futures[future]} - {e}")
                        
        token = response_data.get("data", {}).get("ContinuationToken", None)
        if token == "null":
            token = None

if __name__ == "__main__":
    main()
