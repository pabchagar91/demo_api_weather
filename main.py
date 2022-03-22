import json
import os
import sys
from datetime import datetime
import argparse
from src.rest_service import RestService


def open_json(file_name):
    data = {}
    print(f"File with name {file_name} to be read")
    if os.path.isfile(file_name):
        f = open(file_name, "r")
        data = json.load(f)
        f.close()
    return data


def req_for_city():
    rest_client.params.update({"q": city})
    rest_client.do_request()
    _result = rest_client.response.json()
    return _result


def get_forecast_weather():
    print(f"Current weather for location: {city}")
    rest_client.url = config_file['forecast_url'] + '{}day/{}'.format(days, loc_key)
    rest_client.clear_params()
    rest_client.params.update({"details": True, "metric": metric})
    rest_client.do_request()
    weather_response = rest_client.response.json()
    if rest_client.status == 401:
        print("This api does not have a license to perform this request")
        sys.exit(2)
    print(f"{os.path.basename(os.path.dirname(sys.modules['__main__'].__file__))} forecast {city},"
          f" {country_code} --days={days}")
    for df in weather_response['DailyForecasts']:
        for k, v in df.items():
            if k == 'EpochDate':
                dtmp = datetime.fromtimestamp(v)
                print(dtmp.strftime("%b %d, %Y"))
            elif k in ['Day', 'Night']:
                print(f"Weather on {k}: {v['IconPhrase']}")
                print("Details: ")
                print(f"--> Description: {v['LongPhrase']}\n"
                      f"--> Precipitation Probability: {v['PrecipitationProbability']}\n"
                      f"--> Thunderstorm Probability: {v['ThunderstormProbability']}\n"
                      f"--> Rain Probability: {v['RainProbability']}\n"
                      f"--> Snow Probability: {v['SnowProbability']}\n"
                      f"--> Ice Probability: {v['IceProbability']}\n")
            elif k == 'Temperature':
                print(f"Min Temperature: {str(v['Minimum']['Value'])+' º'+v['Minimum']['Unit']}")
                print(f"Max Temperature: {str(v['Maximum']['Value'])+' º'+v['Maximum']['Unit']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--CITY', '--c', required=True, type=str, default='Seville', help='City input to show weather')
    parser.add_argument('--COUNTRY_CODE', '--cc', required=True, default='ES', type=str, help='Country code from city')
    parser.add_argument('--days', '--d', required=True, type=int, help='Number of days to get forecast')
    parser.add_argument('--metric', '--m', required=False, default=False, action='store_true',
                        help='Units of measurement in metric or imperial')
    parser.print_help()

    args = parser.parse_args()

    config_file = open_json("config.json")

    city = args.CITY.lower().capitalize()
    country_code = args.COUNTRY_CODE.upper()
    days = args.days
    metric = args.metric
    valid_days = [1, 5, 10, 15]
    while days not in valid_days:
        print(f"Valid days to get forecast are {valid_days}. You can see api reference in:"
              f"\n{config_file['url_forecast_reference']}")
        try:
            days = int(input("Select num of days:\n"))
        except ValueError:
            pass

    rest_client = RestService(method='GET', params={'apikey': config_file['api_key']})
    rest_client.url = config_file['location_url'] + 'cities/autocomplete'
    result = req_for_city()
    if rest_client.status == 401:
        print("This api does not have a license to perform this request")
        sys.exit(2)
    while not result:
        print("City input was not found in weather api")
        city = input("Input a city name: \n").lower().capitalize()
        result = req_for_city()
    admin_areas_f = list(filter(lambda x: x['Country']['ID'] == country_code, result))
    availables_countries = list(map(lambda x: x['Country']['ID'], result))
    if not admin_areas_f:
        while country_code not in availables_countries:
            print(f"City {city} was not found for country code {country_code}")
            country_code = input(f"Available countries for city {city}. Select one:\n{', '.join(availables_countries)}")
            country_code = str(country_code).upper()

    admin_areas_f = list(filter(lambda x: x['Country']['ID'] == country_code, result))
    admin_areas = list(map(lambda x: tuple(x['AdministrativeArea'].values()), admin_areas_f))
    admin_areas_codes = list(map(lambda x: x[0], admin_areas))
    ix = 0
    if len(admin_areas) > 1:
        while True:
            admin_code = input("Whats is the Administrative Area?\n{}"
                               .format("".join([f"{k} ==> {v}\n" for k, v in admin_areas])))
            if admin_code.upper() in admin_areas_codes:
                ix = admin_areas_codes.index(admin_code.upper())
                break
            else:
                print(f"Admin area {admin_code} does not exist in available admin areas list")
    loc_key = result[ix]['Key']
    city = result[ix]['LocalizedName']
    country_code = result[ix]['Country']['ID']
    get_forecast_weather()
