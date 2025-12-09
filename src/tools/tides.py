# src/tools/tides.py

# Create a function called `fetch_tide_data` that:
# 1. Fetches today's predictions from the NOAA API for station 9411340
# 2. Finds the prediction closest to the current time
# 3. Determines if tide is rising or falling (compare to previous reading)
# 4. Returns a dictionary with:
#    - timestamp (string, from the API)
#    - height (float, feet)
#    - rising (boolean, True if rising, False if falling)
#
# Use httpx for the HTTP request.
# You'll need to figure out current time to find the closest prediction.
# Hint: Python's datetime module will help.

import httpx
import datetime

def fetch_tide_data():
    try:
        url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=9411340&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&format=json"
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        current_time = datetime.datetime.now()
        closest_prediction = None
        index_of_closest_prediction = None

        for index, prediction in enumerate(data['predictions']):
            if datetime.datetime.strptime(prediction['t'], "%Y-%m-%d %H:%M") > current_time:
                closest_prediction = prediction
                index_of_closest_prediction = index
                break

        # Handle edge case: no future predictions found (late in day)
        if closest_prediction is None:
            # Use the last prediction of the day
            closest_prediction = data['predictions'][-1]
            index_of_closest_prediction = len(data['predictions']) - 1

        is_rising = float(closest_prediction['v']) < float(data['predictions'][min(index_of_closest_prediction + 1, len(data['predictions']) - 1)]['v'])

        result = {
            'timestamp': closest_prediction['t'],
            'height': float(closest_prediction['v']),
            'rising': is_rising
        }

        print('data: ', result)
        return result
    except Exception as e:
        print(f"Error fetching tide data: {e}")
        return {"error": str(e)}
