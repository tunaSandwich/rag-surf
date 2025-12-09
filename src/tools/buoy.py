import httpx
import datetime

# src/tools/buoy.py

# Create a function called `fetch_buoy_data` that:
# 1. Fetches data from https://www.ndbc.noaa.gov/data/realtime2/46218.spec
# 2. Parses the text (skip header rows, split on whitespace)
# 3. Returns the LATEST reading as a dictionary with keys:
#    - timestamp (ISO format string)
#    - wave_height (float, meters)
#    - swell_height (float, meters) 
#    - swell_period (float, seconds)
#    - swell_direction (string, e.g., "NW")
#    - mean_wave_direction (int, degrees)
#
# Use httpx for the HTTP request.
# Handle potential errors gracefully.

def fetch_buoy_data():
    try:
        url = "https://www.ndbc.noaa.gov/data/realtime2/46218.spec"
        response = httpx.get(url)
        response.raise_for_status()
        data = response.text.splitlines()
        data = [line.split() for line in data if not line.startswith('#')]
        timestamp = datetime.datetime(int(data[0][0]), int(data[0][1]), int(data[0][2]), int(data[0][3]), int(data[0][4])).isoformat()

        data = {
            'timestamp': timestamp,
            'wave_height': float(data[0][5]),
            'swell_height': float(data[0][6]),
            'swell_period': float(data[0][7]),
            'swell_direction': data[0][10],
            'mean_wave_direction': float(data[0][14])
        }

        return data
    except Exception as e:
        print(f"Error fetching buoy data: {e}")
        return {"error": str(e)}

