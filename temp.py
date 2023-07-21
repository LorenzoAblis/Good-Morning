import requests

latitude = 42.0664
longitude = -87.9373

api_url = f"https://api.weather.gov/points/{latitude},{longitude}"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        current_temp = forecast_data['properties']['periods'][0]['temperature']
        # print(f"Current Temperature: {current_temp} °F")
        print(forecast_data['properties']['periods'][0])
    else:
        print(f"Failed to retrieve forecast with status code {forecast_response.status_code}")
else:
    print(f"Failed to retrieve point information with status code {response.status_code}")
