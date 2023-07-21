import requests
from bs4 import BeautifulSoup as bs
import json
import datetime


class Scraper:
    @staticmethod
    def scrape_cnn_articles():
        api_key = '9c5be3a4-2e03-4ab5-8e3f-8a312e365641'
        endpoint = 'https://content.guardianapis.com/search'
        params = {
            'api-key': api_key,
            'section': 'world',
            'show-fields': 'headline',
        }

        response = requests.get(endpoint, params=params)
        data = response.json()
        scraped_news = []
        counter = 0

        if response.status_code == 200:
            articles = data['response']['results']
            for article in articles:
                if counter <= 10:
                    headline = article['fields']['headline']
                    link = article['webUrl']
                    scraped_news.append({'headline': headline,
                                        'link': link})
            return scraped_news
        else:
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
                'temperature': temperature.text.strip(),
                'visibility': visibility.text.strip(),
                'rain_chance': rain_chance,
                'air_quality': f"{air_quality.text.strip()}, {air_quality_category.text.strip()}",
                'high_low': highlow.text.strip(),
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
                    forecast = {'day': day, 
                                'high_low': highlow, 
                                'rain_chance': rain_chance}
                    forecast_data.append(forecast)
                    counter += 1

            return forecast_data
        except Exception as e:
            print(f"An error occured while scraping for the forecast: {str(e)}")
            return []
    
    @staticmethod
    def get_anime_info():
        anime_data = []
        query = '''
        query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            siteUrl
            title {
            english
            }
            nextAiringEpisode {
            episode
            airingAt
            timeUntilAiring
            }
            coverImage {
            extraLarge
            }
        }
        }
        '''

        show_ids = [163132, 154745, 136484]

        url = 'https://graphql.anilist.co'

        for show_id in show_ids:
            variables = {
                'id': show_id
            }

            response = requests.post(url, json={'query': query, 'variables': variables})
            data = json.loads(response.content)

            title = data['data']['Media']['title']['english']
            anime_url = data['data']['Media']['siteUrl']
            episode = data['data']['Media']['nextAiringEpisode']['episode']
            time_until_airing = data['data']['Media']['nextAiringEpisode']['timeUntilAiring']
            airing_at = data['data']['Media']['nextAiringEpisode']['airingAt']
            cover_image = data['data']['Media']['coverImage']['extraLarge']

            def convert_seconds(seconds):
                duration = datetime.timedelta(seconds=seconds)
                days = duration.days
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                return days, hours, minutes

            def convert_airing_at(timestamp):
                dt = datetime.datetime.fromtimestamp(timestamp)
                formatted_date = dt.strftime("%A, %m/%d/%y")
                return formatted_date

            days, hours, minutes = convert_seconds(time_until_airing)
            formatted_airing_at = convert_airing_at(airing_at)
            formatted_time_until_airing = f"{days}d, {hours}h, {minutes}m"

            anime_info = {'title': title,
                          'anime_url': anime_url,
                          'episode': str(episode),
                          'time_until_airing': formatted_time_until_airing, 
                          'airing_at': formatted_airing_at, 
                          'cover_image': cover_image}
            anime_data.append(anime_info)
        return anime_data
