# pycoinmarketcap

A simple API Wrapper for the **CoinMarketCap API** (https://coinmarketcap.com/api/documentation/v1)

## Installation

```
pip3 install pycoinmarketcap
```

## Usage

```python
from pycoinmarketcap import CoinMarketCap

c = CoinMarketCap("YOUR API KEY")

airdropData = c.crypto_airdrop("airdrop-id")
print(airdropData)
```

##

#### &copy; 2021 | World of Cryptopups | TheBoringDude
