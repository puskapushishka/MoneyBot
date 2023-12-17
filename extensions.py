import requests
import json
from config import ApiKey, val


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(have: str, want: str, amount: str):

        try:
            have_ticker = val[have]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{have}"')

        try:
            want_ticker = val[want]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{want}"')

        if have == want:
            raise ConvertionException(f'Невозможно перевести одинаковые вылюты "{want}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'"{amount}" не является числом.')

        api_url = f'https://api.api-ninjas.com/v1/convertcurrency?want={want_ticker}&have={have_ticker}&amount={amount}'
        response = requests.get(api_url, headers={'X-Api-Key': f'{ApiKey}'})
        if response.status_code == requests.codes.ok:
            res = json.loads(response.content)['new_amount']
            print(res)
            return res
        else:
            raise Exception(f"Error: {response.status_code} {response.text}")


CryptoConverter.convert('доллар', 'евро', '1')


