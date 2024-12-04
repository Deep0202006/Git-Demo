import requests

def get_weather(api_key, city):
    """Fetch the weather data for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None

def display_weather(weather_data):
    """Display the weather information."""
    if weather_data:
        city = weather_data['name']
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        
        print(f"\nWeather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Condition: {weather_description.capitalize()}")
    else:
        print("No weather data available.")

def main():
    """Main function to run the weather forecast application."""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key

    while True:
        city = input("\nEnter a city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            print("Exiting the Weather Forecast Application.")
            break
        
        weather_data = get_weather(api_key, city)
        display_weather(weather_data)

if __name__ == "__main__":
    main()