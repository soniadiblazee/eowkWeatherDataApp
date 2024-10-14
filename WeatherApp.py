import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ewokWeatherApp")

def getLatLon(city,state):
    loc = geolocator.geocode(f"{city}, {state}")
    if loc:
        return loc.latitude, loc.longitude
    else:
        return None
    
# gets the latitude and longitude via a city and state its in
def getLatLongViaCityState():
    city = input("city name: ")
    state = input("state name (abbreviation): ")
    latLon = getLatLon(city,state)

    if isinstance(latLon,tuple):
        print(f"the latitude and longitude of {city}, {state} are {latLon[0]}, {latLon[1]}.")
    else:
        print("location not found")
getLatLongViaCityState()

# gets weather data
def weatherDataGet(lat,lon):
    baseURL = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        response = requests.get(baseURL)
        response.raise_for_status()
        data = response.json()
        forecastURL = data["properties"]["forecast"]
        forecastResponse = requests.get(forecastURL)
        forecastResponse.raise_for_status()
        return forecastResponse.json()
    except requests.exceptions.HTTPError as err:
        print(f"error getting weather data: {err}")
        return None
    
# dictionary for weather data
ewokWeather = {}

# gather specific data on weather, store it in the 
# dictionary that was just made
def weatherUpdate(city,state,lat,lon,ewokWeather):
    weatherData = weatherDataGet(lat,lon)
    if weatherData:
        ewokWeather[city] = {
            "state":state,
            "currentTemp":weatherData["properties"]["periods"][0]["temperature"],
            "highTemp":weatherData["properties"]["periods"][0]["temperature"],
            "lowTemp":weatherData["properties"]["periods"][0]["temperature"],
            "weatherCons":weatherData["properties"]["periods"][0]["temperature"]["detailedForecast"]
        }
        print(f"weather data for {city}, {state} updated.")
    else:
        print(f"unable to update data for {city}, {state}.")

# print weather data ...
def dataDisplay(city,ewokWeather):
    weather = ewokWeather.get(city)
    if weather:
        print(f"\ncity: {city}, {weather['state']}")
        print(f"current temperature: {weather['currentTemp']}F")
        print(f"high temperature: {weather['highTemp']}F")
        print(f"low temperature: {weather['lowTemp']}F")
        print(f"current weather conditions: {weather['weatherCons']}\n")
    else:
        print(f"no weather data for {city}")