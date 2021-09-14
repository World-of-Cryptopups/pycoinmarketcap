from pycoinmarketcap import CoinMarketCap
import os


cmc = CoinMarketCap(os.environ["API_KEY"])

btc = cmc.crypto_quotes_latest("1", convert="PHP")
print(btc.data)
