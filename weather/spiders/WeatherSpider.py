import scrapy
import json
import os


API_KEY = 'YOUR_API_HERE'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WeatherSpider(scrapy.Spider):
    name = "weather"

    def start_requests(self):
        meta = {
            'proxy': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'
        }

        # Get the list of RegionID, Longitude, Latitude from the json file
        with open(os.path.join(BASE_DIR, 'data/regions.json')) as f:
            data = json.load(f)
            list_done = [1000, 1001, 1002, 1003, 1004, 1010, 1015, 1020, 1023, 1025]
            for region in data:
                if region['RegionID'] in list_done:
                    continue
                latitude = region['Latitude']
                longitude = region['Longitude']
                url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=1979-01-01&end_date=2009-12-31&hourly=relative_humidity_2m,wind_speed_10m,soil_temperature_28_to_100cm,soil_moisture_28_to_100cm&daily=temperature_2m_mean,sunshine_duration,precipitation_sum,rain_sum,snowfall_sum&timezone=GMT'
                yield scrapy.Request(url=url, callback=self.parse, meta=meta,
                                     cb_kwargs={'region_id': region['RegionID']})

    def parse(self, response, **kwargs):
        region_id = kwargs['region_id']
        file_path = os.path.join(BASE_DIR, f'data_1979/weather_{region_id}.json')
        with open(file_path, 'w') as f:
            f.write(response.body.decode('utf-8'))
