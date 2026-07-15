import requests
from bs4 import BeautifulSoup


class Currency_pat:
    ALL_URL = 'https://index.minfin.com.ua/markets/fuel/'

    FUEL_INDEX = {
        'pat95prem': 0,
        'pat95': 3,
        'pat92': 6,
        'dis': 9,
        'gas': 12,
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    def __init__(self):
        self._prices_cache = None

    def _fetch_prices(self):
        if self._prices_cache is None:
            resp = requests.get(self.ALL_URL, headers=self.headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')
            self._prices_cache = soup.findAll('td', {'align': 'right'})
        return self._prices_cache

    def _get_price(self, fuel_key):
        cells = self._fetch_prices()
        index = self.FUEL_INDEX[fuel_key]
        return cells[index].text.replace(',', '.')

    def check_currency_pat95prem(self):
        return self._get_price('pat95prem') or '00.00'

    def check_currency_pat95(self):
        return self._get_price('pat95') or '00.00'

    def check_currency_pat92(self):
        return self._get_price('pat92') or '00.00' 

    def check_currency_dis(self):
        return self._get_price('dis') or '00.00'

    def check_currency_gas(self):
        return self._get_price('gas') or '00.00'