import json
import requests
from config import currency_list

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = currency_list[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = currency_list[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Одинаковя валюта стоит одинаково :)')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=f390b600dca7472d0dd52d9bb4115729')
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        return  round(new_price)