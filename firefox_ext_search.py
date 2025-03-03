import requests
import subprocess
import json
import re

def search_mozilla_extensions(search_term):
    """Searches Mozilla Add-ons for extensions matching the search term."""
    url = f"https://addons.mozilla.org/api/v5/addons/search/?q={search_term}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching Mozilla Add-ons: {e}")
        return []

def get_extension_header(guid):
    """Fetches the header of an extension using curl."""
    url = f"https://addons.mozilla.org/en-US/firefox/addon/{guid}/"
    try:
        process = subprocess.run(["curl", "-i", url], capture_output=True, text=True, check=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error fetching header for {guid}: {e}")
        return None
    except FileNotFoundError:
        print("curl is not installed. Please install curl.")
        return None

def extract_guid_from_header(header):
    """Extracts the guid from the header using regex."""
    if header:
        match = re.search(r'"guid":"([^"]+)"', header)
        if match:
            return match.group(1)
    return None

def extract_json_data(guid):
    """Extracts the json data related to the addon from the search results."""
    url = f"https://addons.mozilla.org/api/v5/addons/addon/{guid}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving JSON data for {guid}: {e}")
        return None

def main():
    search_term = input("Enter the search term for Mozilla extensions: ")
    results = search_mozilla_extensions(search_term)

    if results:
        top_results = results[:3]  # Limit to the top 3 results
        for result in top_results:
            guid = result.get("slug")
            name = result.get("name", {}).get("en-US", "Unknown")

            print(f"Extension: {name}, GUID: {guid}")
            header = get_extension_header(guid)
            if header:
                extracted_guid = extract_guid_from_header(header)
                if extracted_guid:
                    print(f"  Extracted GUID from header: {extracted_guid}")
                else:
                    print("  GUID not found in header.")

            json_data = extract_json_data(guid)
            if json_data:
                edit_url = json_data.get('edit_url')
                print (f"  Edit URL: {edit_url}")
                has_eula = json_data.get('has_eula')
                print (f"  Has EULA: {has_eula}")
                has_privacy_policy = json_data.get('has_privacy_policy')
                print (f"  Has Privacy Policy: {has_privacy_policy}")
            else:
                print("  Could not retrieve JSON data")

    else:
        print("No extensions found.")

if __name__ == "__main__":
    main()
