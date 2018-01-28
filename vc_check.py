import urllib, json, requests

URL_HEAD = 'https://api.coinmarketcap.com/v1/ticker/'
#other source is https://www.cryptocompare.com
#https://coinmarketcap.com/api/

#to standardize make the currency lower case
#replace spaces with dashes


def speech_to_currency(speech):
    speech_currency = {
        'bitcoin': 'bitcoin',
        'ethereum': 'ethereum',
        'ripple': 'ripple',
        'bitcoin cash': 'bitcoin-cash',
        'cardano': 'cardano',
        'stellar': 'stellar',
        'litecoin': 'litecoin',
        'neo': 'neo',
        'nem': 'nem',
        'iota': 'iota',
        'dash': 'dash',
        'monero': 'monero',
        'bitcoin gold': 'bitcoin-gold',
        'v chain': 'vechain',
        'qtum': 'qtum',
        'etherium classic': 'etherium-classic',
        'lisk': 'lisk',
        'rai Blocks': 'raiblocks',
        'steem': 'steem',
        'zcash': 'zcash',
        'bytecoin': 'bytecoin'
    }
    if speech in speech_currency:
        return speech_currency[speech]
    return None
    
def call_api(currency):
    url = URL_HEAD + currency
    try:
        r = requests.get(url)
        return r.json()[0]
    except:
        print url
        print 'Error occurred when retrieving data'
        return None





'''
Sample response

[
    {
        "id": "bitcoin", 
        "name": "Bitcoin", 
        "symbol": "BTC", 
        "rank": "1", 
        "price_usd": "11129.0", 
        "price_btc": "1.0", 
        "24h_volume_usd": "8170750000.0", 
        "market_cap_usd": "187267816548", 
        "available_supply": "16827012.0", 
        "total_supply": "16827012.0", 
        "max_supply": "21000000.0", 
        "percent_change_1h": "-2.65", 
        "percent_change_24h": "-3.06", 
        "percent_change_7d": "-4.43", 
        "last_updated": "1516954166"
    }
]
'''
