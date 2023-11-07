from flask import Flask, render_template, request
import requests
import arrow

app = Flask(__name__)
api_key = '4a428e3ef52ee4a5deb87ef267ef3b52'

def timestampformat(value):
    # Convert the Unix timestamp to a readable format
    formatted_time = arrow.get(value).format('DD-MM-YYYY HH:mm:ss')
    return formatted_time

app.jinja_env.filters['timestampformat'] = timestampformat

@app.route("/", methods=['GET', 'POST'])
def get_weather():
    city = ""
    weather_data = {}
    if request.method == "POST":
        city = request.form.get('city')
        if city:
            # Construct the API URL
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
                # Construct the URL for the weather icon
                icon_code = weather_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
                # Add the icon URL to the weather_data dictionary
                weather_data['icon_url'] = icon_url

    # Get the current time
    current_time = arrow.now()

    # Pass the current time to the template
    return render_template('index.html', city=city, weather_data=weather_data, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
