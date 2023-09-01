import os
import json
import requests
import tarfile

# Directory where you want to extract the contents
output_directory = "output"

def fetch_IANA_time_zone_database(output_directory):
    # API URL for downloading the latest database
    database_api_url = "https://data.iana.org/time-zones/tzdata-latest.tar.gz"

    # Ensure the output directory exists or create it
    os.makedirs(output_directory, exist_ok=True)

    # Fetch the latest database from the API
    print("Fetching latest database from API...")
    response = requests.get(database_api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the downloaded data to a temporary file
        with open("tzdata-latest.tar.gz", "wb") as temp_file:
            temp_file.write(response.content)

        # Extract the downloaded file to the output directory
        with tarfile.open("tzdata-latest.tar.gz", "r:gz") as tar:
            tar.extractall(output_directory)
        
        # Remove the temporary downloaded file
        os.remove("tzdata-latest.tar.gz")

        print("Database extraction completed.")
    else:
        print(f"Failed to fetch the database from the API. Status code: {response.status_code}")
        exit(1)



def create_country_to_time_zone_mapping():
    print("Creating country to timezones mapping...")
    # Path to the zone.tab file
    zone_tab_file = os.path.join(output_directory, "zone1970.tab")

    # Create a dictionary to store the country code to time zones mapping
    country_to_timezones = {}

    # Read the zone.tab file and populate the mapping
    with open(zone_tab_file, "r") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 3:
                    country_code = parts[0]
                    time_zone = parts[2]
                    # Append the time zone to the list for the country code
                    country_to_timezones.setdefault(country_code, []).append(time_zone)
    return country_to_timezones

def dump_time_zone_details(country_to_timezones):
    print("Dumping your file to JSON...")
    # Initialize a dictionary to store timezones for each country
    country_timezones = {}

    # Iterate through the data and group by country code
    for country_codes, timezones in country_to_timezones.items():
        # Split multiple country codes if present
        country_codes = country_codes.split(',')
        for country_code in country_codes:
            country_code = country_code.strip()
            print(country_timezones.get(country_code))
            if(country_timezones.get(country_code) is None):
                country_timezones[country_code] = []
            country_timezones[country_code] += timezones;

    # Define the path to the JSON file where you want to store the mapping
    json_file_path = "country_to_timezones.json"

    # Store the mapping in a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(country_timezones, json_file, indent=2)

    print(f"Mapping saved to {json_file_path}")


fetch_IANA_time_zone_database(output_directory)

dump_time_zone_details(create_country_to_time_zone_mapping())


