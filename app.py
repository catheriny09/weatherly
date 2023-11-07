import requests
import openai
import tools
import time

# Put this on a timer with a ui that refreshes every minute?

def app():
    openai_key, weather_key = tools.fetchKeys()

    city = input('Enter city name: ')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}'
    openai.api_key = openai_key


    while(True):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            temp = temp - 273.15
            temp = "{0:.2f}".format(temp)
            
            desc = data['weather'][0]['description']
            print(f'Temperature: {temp} C')
            print(f'Description: {desc}\n')
            
            prompt = f'Temperature: {temp} C Description: {desc}\n'
            
            response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"What should I wear in this weather?:\n:{prompt}",
                    max_tokens=1024,
                    temperature=0.5,
                )
            
            output = response.choices[0].text
            print(output)
            print('\n')
            
            time.sleep(60)
            
        else:
            print('Error fetching weather data')
        
app()