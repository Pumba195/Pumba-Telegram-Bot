import requests


class Currency_bit:
    COINGECKO_API = 'https://api.coingecko.com/api/v3/simple/price'

    COINS = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'bnb': 'binancecoin',
        'xrp': 'ripple',
        'ada': 'cardano',
        'doge': 'dogecoin',
        'sol': 'solana',
        'ton': 'the-open-network',
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    def __init__(self):
        self._prices_cache = None

    def _fetch_prices(self):
        if self._prices_cache is None:
            params = {
                'ids': ','.join(self.COINS.values()),
                'vs_currencies': 'usd',
            }
            resp = requests.get(self.COINGECKO_API, params=params, headers=self.headers, timeout=10)
            resp.raise_for_status()
            self._prices_cache = resp.json()
        return self._prices_cache

    def _format_price(self, short_code):
        prices = self._fetch_prices()
        coin_id = self.COINS[short_code]
        data = prices.get(coin_id)
        if not data or 'usd' not in data:
            return None
        price = data['usd']
        if price < 1:
            return f'{price:.4f}'
        return f'{price:.2f}'

    def check_currency_btc(self):
        return self._format_price('btc') or '00.00'

    def check_currency_eth(self):
        return self._format_price('eth') or '00.00'

    def check_currency_bnb(self):
        return self._format_price('bnb') or '00.00'

    def check_currency_xrp(self):
        return self._format_price('xrp') or '00.00'

    def check_currency_ada(self):
        return self._format_price('ada') or '00.00'

    def check_currency_doge(self):
        return self._format_price('doge') or '00.00'

    def check_currency_sol(self):
        return self._format_price('sol') or '00.00'

    def check_currency_ton(self):
        return self._format_price('ton') or '00.00'