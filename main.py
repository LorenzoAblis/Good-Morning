import threading
import requests
from bs4 import BeautifulSoup as bs
import customtkinter as ctk
import webbrowser


class Scraper:
    @staticmethod
    def scrape_cnn_articles():
        try:
            url = "https://www.cnn.com/world"
            response = requests.get(url)
            html_content = response.content
            soup = bs(html_content, 'html.parser')
            limit = 10
            counter = 0
            scraped_articles = []

            divs = soup.find_all(
                'div',
                {
                    'class': 'card container__item container__item--type-section container_lead-plus-headlines__item container_lead-plus-headlines__item--type-section'
                },
            )

            for div in divs:
                if counter >= limit:
                    break

                headline = div.find('span', {'data-editable': 'headline'})
                link = div.find('a', {'class': 'container__link container_lead-plus-headlines__link'})

                if link is not None and headline is not None:
                    article = {'headline': headline.text.strip(), 'link': link['href']}
                    scraped_articles.append(article)
                    counter += 1

            return scraped_articles
        except Exception as e:
            print(f"An error occured while scraping for CNN articles: {str(e)}")
            return []

    @staticmethod
    def scrape_weather():
        try:
            url = "https://weather.com/weather/today/l/4b807770f7a9a68ab3236c14beec03d4f8471b97c32e6e9e972a36533e58559b"
            response = requests.get(url)
            html_content = response.content
            soup = bs(html_content, 'html.parser')

            temperature = soup.find('span', {'data-testid': 'TemperatureValue'})
            visibility = soup.find('div', {'data-testid': 'wxPhrase'})
            rain_chance_div = soup.find('a', {'class': 'Column--innerWrapper--3ocxD Button--default--2gfm1'})
            rain_chance = rain_chance_div.find('span', {'class': 'Column--precip--3JCDO'}).text.strip().replace(
                'Chance of Rain', ''
            )
            air_quality = soup.find('text', {'data-testid': 'DonutChartValue'})
            air_quality_category = soup.find('span', {'data-testid': 'AirQualityCategory'})
            highlow = soup.find('div', {'class': 'WeatherDetailsListItem--wxData--kK35q'})

            weather_data = {
                'Temperature': temperature.text.strip(),
                'Visibility': visibility.text.strip(),
                'Rain Chance': rain_chance,
                'Air Quality': f"{air_quality.text.strip()}, {air_quality_category.text.strip()}",
                'High/Low': highlow.text.strip(),
            }

            return weather_data
        except Exception as e:
            print(f"An error occured while scraping for weather: {str(e)}")
            return {}

    @staticmethod
    def scrape_forecast():
        try:
            url = "https://weather.com/weather/tenday/l/4b807770f7a9a68ab3236c14beec03d4f8471b97c32e6e9e972a36533e58559b"
            response = requests.get(url)
            html_content = response.content
            soup = bs(html_content, 'html.parser')

            details = soup.find_all(
                'details', {'class': 'DaypartDetails--DayPartDetail--2XOOV Disclosure--themeList--1Dz21'}
            )
            limit = 10
            counter = 0

            forecast_data = []

            for detail in details:
                if counter >= limit:
                    break

                day = detail.find('h3', {'data-testid': 'daypartName'}).text.strip()
                highlow = detail.find('div', {'class': 'DetailsSummary--temperature--1kVVp'}).text.strip()
                rain_chance = detail.find('span', {'data-testid': 'PercentageValue'}).text.strip()

                if day != "Today" or day != "Tonight":
                    forecast = {'day': day, 'highlow': highlow, 'rain_chance': rain_chance}
                    forecast_data.append(forecast)
                    counter += 1

            return forecast_data
        except Exception as e:
            print(f"An error occured while scraping for the forecast: {str(e)}")
            return []


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Good Morning!")
        self.geometry("1440x720")

        self.weather_frame = ctk.CTkFrame(self, width=100, height=100)
        self.weather_frame.pack(side="left", padx=15, anchor='n')

        self.news_frame = ctk.CTkFrame(self)
        self.news_frame.pack(side="left", padx=20, anchor='n')

        self.forecast_frame = ctk.CTkFrame(self)
        self.forecast_frame.pack(side="right", padx=20, anchor='n')

        self.weather_data = {}
        self.forecast_data = []
        self.articles = []

        threading.Thread(target=self.scrape_data).start()

    def scrape_data(self):
        self.articles = Scraper.scrape_cnn_articles()
        self.weather_data = Scraper.scrape_weather()
        self.forecast_data = Scraper.scrape_forecast()

        self.create_weather_widgets()
        self.create_article_widgets()
        self.create_forecast_widgets()

    def create_weather_widgets(self):
        weather_label = ctk.CTkLabel(self.weather_frame, text="Current Weather", anchor='w', font=("Arial", 35))
        weather_label.pack(pady=5, padx=5)

        items = ["Temperature", "Visibility", "Rain Chance", "Air Quality", "High/Low"]

        for item in items:
            item_label = ctk.CTkLabel(
                self.weather_frame, text=f"{item}: {self.weather_data.get(item, '')}", anchor='w', font=("Arial", 15)
            )
            item_label.pack(pady=5, padx=5)

    def create_article_widgets(self):
        article_label = ctk.CTkLabel(self.news_frame, text="Top Stories", font=("Arial", 35))
        article_label.pack(pady=5)

        for article in self.articles:
            headline = article['headline']
            link = "https://www.cnn.com" + article['link']
            article_button = ctk.CTkButton(
                self.news_frame, text=headline, command=lambda url=link: webbrowser.open(url), font=("Arial", 15)
            )
            article_button.pack(pady=5, padx=5, anchor='w')

    def create_forecast_widgets(self):
        forecast_label = ctk.CTkLabel(self.forecast_frame, text="Weekly Forecast", font=("Arial", 35))
        forecast_label.pack(pady=5, padx=15)

        for day in self.forecast_data:
            day_name = day['day']
            highlow = day['highlow']
            rain_chance = day['rain_chance']
            day_label = ctk.CTkLabel(
                self.forecast_frame,
                text=f"{day_name}, Temperature: {highlow}, Precipitation: {rain_chance}",
                anchor='w',
                font=("Arial", 15),
            )
            day_label.pack(pady=5, padx=15, anchor='w')


app = App()
app.mainloop()
