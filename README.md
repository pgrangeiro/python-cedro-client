# Python Cedro Client
[![Build Status](https://travis-ci.org/pgrangeiro/python-cedro-client.svg?branch=master)](https://travis-ci.org/pgrangeiro/python-cedro-client)

A Python library to connect with [Cedro Web Feeder API](http://markets.cedrotech.com/market-data/#web-feeder).

# Install
```
    pip install git+https://github.com/pgrangeiro/python-cedro-client.git
```

# Tests
```
tox
```

# Usage
```
    from cedro.clients import CedroClient

    client = CedroClient()
    client.quotes.login('username', 'password')
    quotes = list(client.quotes.get(['VALE3', 'BRFS3']))
    print(quotes)
>>> [{'symbol': 'vale3', 'timeUpdate': '...
```

## Get tickers latest quotes
    Returns an iterator with the latest quotations for tickers passed by parameters.
```
    client.quotes.get(['VALE3'])
```

## Get currencies latest quotes
    Returns an iterator with the latest quotations for currencies passed by parameters.
```
    client.currencies.get(['dolcm', 'eurcm'])
```

## Parsing response data from Cedro Web Feeder API
    You can create your own parser with your _parse_ class method.
```
    from cedro.clients import CedroClient


    class MyParser:

        @classmethod
        def parse(cls, data):
            return {
                'ticker': data['symbol'].upper(),
                'day_min_value': data['low'],
                'day_max_value': data['high'],
                'previous_close_value': data['previous'],
                'open_value': data['open'],
                'last_value': data['lastTrade'],
            }


    client = CedroClient(MyParser)
    client.quotes.login('username', 'password')
    quotes = client.quotes.get(['VALE3', 'BRFS3'])
```
