import requests

def search_mozilla_extensions(search_term):
    url = f"https://addons.mozilla.org/api/v5/addons/search/?q={search_term}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching Mozilla Add-ons: {e}")
        return []

def extract_json_data(guid):
    url = f"https://addons.mozilla.org/api/v5/addons/addon/{guid}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving JSON data for {guid}: {e}")
        return None

def main():
    search_term = input("Enter the search term for Mozilla extensions: ")
    results = search_mozilla_extensions(search_term)

    if results:
        top_results = results[:3]
        for result in top_results:
            guid = result.get("slug")
            name = result.get("name", {}).get("en-US", "Unknown")
            print(f"Extension: {name}, GUID: {guid}")

            json_data = extract_json_data(guid)
            if json_data:
                edit_url = json_data.get('edit_url')
                print(f"  Edit URL: {edit_url}")
                has_eula = json_data.get('has_eula')
                print(f"  Has EULA: {has_eula}")
                has_privacy_policy = json_data.get('has_privacy_policy')
                print(f"  Has Privacy Policy: {has_privacy_policy}")
                print("-------------------------------------------------------------")
            else:
                print("  Could not retrieve JSON data")
    else:
        print("No extensions found.")

if __name__ == "__main__":
    main()
