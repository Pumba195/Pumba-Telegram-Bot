import requests
from bs4 import BeautifulSoup
import re

class Currency:
    NBU_API = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json'
    RUB_FALLBACK_URL = 'https://minfin.com.ua/ua/currency/nbu/rub/'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    def __init__(self):
        self._rates_cache = None

    def _fetch_rates(self):
        if self._rates_cache is None:
            resp = requests.get(self.NBU_API, headers=self.headers, timeout=10)
            resp.raise_for_status()
            self._rates_cache = {item['cc']: item['rate'] for item in resp.json()}
        return self._rates_cache

    def _format_rate(self, cc_code):
        rates = self._fetch_rates()
        rate = rates.get(cc_code)
        if rate is None:
            return None
        return f'{rate:.2f}'.replace(',', '.')

    def check_currency_dol(self):
        return self._format_rate('USD') or '00.00'

    def check_currency_euro(self):
        return self._format_rate('EUR') or '00.00'

    def check_currency_pln(self):
        return self._format_rate('PLN') or '00.00'



    def check_currency_rub(self):
        rate = self._format_rate('RUB')
        if rate:
            return rate
        return self._get_rub_from_minfin() or '00.00'

    def _get_rub_from_minfin(self):
        try:
            resp = requests.get(self.RUB_FALLBACK_URL, headers=self.headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException:
            return None

        soup = BeautifulSoup(resp.content, 'html.parser')

        for row in soup.select('table tr'):
            cells = row.find_all('td')
            if not cells:
                continue
            row_text = row.get_text(' ', strip=True)
            if 'RUB' in row_text.split():
                rate_text = cells[-1].get_text(strip=True)
                match = re.match(r'(\d+,\d+)', rate_text)
                if match:
                    rate_value = float(match.group(1).replace(',', '.'))
                    return f'{rate_value:.2f}'
                return None

        return None
    

	
"""
#Holiday
	def get_price_holiday(self):
		full_page_holiday = requests.get(self.holiday)
		soup_holiday = BeautifulSoup(full_page_holiday.content, 'html.parser')
		#convert_holiday = [header.get_text() for header in soup_holiday.find_all("span", {"response-success": "true", "class": "article__content"})]
		convert_holiday = soup_holiday.find_all("div", {"response-success": "true", "class": "article__content"})
		print("convert_holiday:", convert_holiday)
		return convert_holiday
    # Проверка изменения валюты
	def check_currency_holiday(self):
		currency = self.get_price_holiday()
		print("currency:", currency)
		return str(currency)
"""
#Currenc = Currency()
#print(Currenc.check_currency_holiday())