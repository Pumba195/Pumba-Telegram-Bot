from rates.rates_of_currency import Currency
from rates.rates_of_crypto import Currency_bit
from rates.rates_of_fuel import Currency_pat
from config.config import bot
import requests


# Rates of currency
async def send_rates(event):
    currency = Currency()

    try:
        eu = currency.check_currency_euro()
        usd = currency.check_currency_dol()
        pln = currency.check_currency_pln()
        rub = currency.check_currency_rub()
    except requests.RequestException:
        await bot.send_message(
            event.chat.id,
            '⚠️ Не вдалося отримати курси валют. Спробуйте пізніше.',
            parse_mode='html'
        )
        return

    text = (
        f'<b>💰Курс валют(НБУ)💰\n\n'
        f'💶Євро</b> — <i>{eu}₴</i>\n'
        f'<b>💵Долар</b> — <i>{usd}₴</i>\n'
        f'<b>🪙Злотий</b> — <i>{pln}₴</i>\n'
        f'<b>💩Срубль</b> — <i>{rub}₴</i>'
    )

    await bot.send_message(event.chat.id, text, parse_mode='html')

# Rates of crypto
async def send_crypto(event):
    currency = Currency_bit()

    try:
        btc = currency.check_currency_btc()
        eth = currency.check_currency_eth()
        bnb = currency.check_currency_bnb()
        ton = currency.check_currency_ton()
        xrp = currency.check_currency_xrp()
        ada = currency.check_currency_ada()
        doge = currency.check_currency_doge()
        sol = currency.check_currency_sol()
    except requests.RequestException:
        await bot.send_message(
            event.chat.id,
            '⚠️ Не вдалося отримати курси криптовалют. Спробуйте пізніше.',
            parse_mode='html'
        )
        return

    text = (
        f'<b>💎Курс криптовалюти💎\n\n'
        f'₿itcoin</b>(BTC) — <i>{btc}$</i>\n'
        f'<b>Ξthereum</b>(ETH) — <i>{eth}$</i>\n'
        f'<b>BNB</b>(BNB) — <i>{bnb}$</i>\n'
        f'<b>Solana</b>(SOL) — <i>{sol}$</i>\n'
        f'<b>Toncoin</b>(TON) — <i>{ton}$</i>\n'
        f'<b>XRP</b>(XRP) — <i>{xrp}$</i>\n'
        f'<b>Cardano</b>(ADA) — <i>{ada}$</i>\n'
        f'<b>Dogecoin</b>(DOGE) — <i>{doge}$</i>'
    )

    await bot.send_message(event.chat.id, text, parse_mode='html')

# Rates of fuel
async def send_petrol(event):
    currency = Currency_pat()

    try:
        pat95prem = currency.check_currency_pat95prem()
        pat95 = currency.check_currency_pat95()
        pat92 = currency.check_currency_pat92()
        dis = currency.check_currency_dis()
        gas = currency.check_currency_gas()
    except requests.RequestException:
        await bot.send_message(
            event.chat.id,
            '⚠️ Не вдалося отримати ціни на пальне. Спробуйте пізніше.',
            parse_mode='html'
        )
        return

    text = (
        f'<b>⛽️Середні ціни на пальне по Україні⛽️\n\n'
        f'Бензин А-95+</b> — <i>{pat95prem}₴</i>\n'
        f'<b>Бензин А-95</b> — <i>{pat95}₴</i>\n'
        f'<b>Бензин А-92</b> — <i>{pat92}₴</i>\n'
        f'<b>Дизель</b> — <i>{dis}₴</i>\n'
        f'<b>Газ</b> — <i>{gas}₴</i>'
    )

    await bot.send_message(event.chat.id, text, parse_mode='html')