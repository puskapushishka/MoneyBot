import requests
import json
from config import ApiKey, val


class ConvertionException(Exception):
    pass


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

        api_url = f'https://www.amdoren.com/api/currency.php?api_key={ApiKey}&from={have_}&to={want_}&amount={amount}'
        response = requests.get(api_url)
        res = json.loads(response.content)
        if res['error'] == 0:
            result = float(res['amount'])
            return round(result, 6)
        else:
            print(f"Error: {res['error']} {res['error_message']}")
            raise Exception(f"Error: {res['error']}\n{res['error_message']}")
