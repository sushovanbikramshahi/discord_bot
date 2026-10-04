import requests

weather_api = "https://api.open-meteo.com/v1/forecast?"
latitude = "28.2096" # default of Pokhara
longitude = "83.9856"

url = f"{weather_api}latitude={latitude}&longitude={longitude}&current_weather=true"

response = requests.get(url)
data = response.json()
print(data)
print (url)

print("\n\n")

print(data["current_weather"]["temperature"])
print(
     f'''
                    Current temp = {data["current_weather"]["temperature"]}
                    Current windspeed = {data["current_weather"]["windspeed"]}
                '''
)
