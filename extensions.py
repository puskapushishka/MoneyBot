import requests
import json
from config import ApiKey, val


# user error handling class
class ConvertionException(Exception):
    pass


# currency conversion using the API and error handling
class CryptoConverter:
    @staticmethod
    def convert(have: str, want: str, amount: str):

        try:
            have_ = val[have]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{have}"')

        try:
            want_ = val[want]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{want}"')

        if have == want:
            raise ConvertionException(f'Невозможно перевести одинаковые вылюты "{want}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'"{amount}" не является числом.')

        api_url = f'http://apilayer.net/api/convert?access_key={ApiKey}&from={have_}&to={want_}&amount={amount}'
        response = requests.get(api_url)
        res = json.loads(response.content)

        if res['success']:
            result = float(res['result'])
            return round(result, 6)
        else:
            print(f"Error: {res['error']['code']} {res['error']['info']}")
            raise Exception(f"Error: {res['error']['code']}\n{res['error']['info']}")
