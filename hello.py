# .venv\Scripts\Activate
# flask --app hello run --debug

from flask import Flask, render_template
from flask_caching import Cache
from main import Scraper
import webbrowser
import asyncio

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

async def scrape_data():
    test = Scraper()
    articles = test.scrape_cnn_articles()
    weather_data = test.scrape_weather()
    forecast_data = test.scrape_forecast()
    anime_info = test.get_anime_info()
    return articles, weather_data, forecast_data, anime_info

@app.route("/")
@cache.cached(timeout=50)
def hello_world():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    articles, weather_data, forecast_data, anime_info = loop.run_until_complete(scrape_data())
    loop.close()

    return render_template('index.html', articles=articles, weather_data=weather_data, forecast_data=forecast_data, anime_info=anime_info)

if __name__ == "__main__":
    webbrowser.open_new_tab("http://127.0.0.1:5000")
    app.run()
