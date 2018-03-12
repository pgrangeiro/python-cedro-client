import requests
from abc import ABC

from cedro.parsers import NullableParser
from cedro.exceptions import (
    ImprorpelyCalledError, HttpAuthenticationError, ResponseConnectionError,
)


class BaseClient(ABC):

    BASE_URL = 'http://webfeeder.cedrofinances.com.br'
    PATH_URL = ''

    def __init__(self, parser=None):
        self.parser = parser or NullableParser
        self._request = None

    def login(self, username, password):
        session = requests.Session()

        request = requests.Request(
            'POST',
            f'{self.BASE_URL}/SignIn',
            params={
                'login': username,
                'password': password,
            }
        )
        request = request.prepare()
        response = session.send(request, timeout=7000)
        logged = response.json()

        if not response.ok or not logged:
            raise HttpAuthenticationError(
                f'Cedro API responded with {response.status_code} HTTP status code.'
            )
        self._request = session

    @property
    def url(self):
        return f'{self.BASE_URL}{self.PATH_URL}'

    def get(self, tickers):
        if not tickers:
            raise ImprorpelyCalledError('Tickers can not be a empty list.')

        if not self._request:
            raise ImprorpelyCalledError('You must be logged first to perform this action.')

        url = self.build_url(tickers)
        response = self._request.get(url)

        if not response.ok:
            raise ResponseConnectionError(
                f'Cedro API responded with {response.status_code} HTTP status code when trying to get URL {url}.'
            )

        data = response.json()
        if not isinstance(data, list):
            data = [data]

        for item in data:
            try:
                yield(self.parser.parse(item))
            except Exception as parser_exception:
                raise parser_exception
        response.close()

    def build_params(self, tickers):
        return '/'.join([f'{t.lower()}' for t in tickers])

    def build_url(self, tickers):
        params = self.build_params(tickers)
        return f'{self.url}/{params}'


class QuotesClient(BaseClient):

    PATH_URL = '/services/quotes/quote'


class CurrenciesClient(BaseClient):

    PATH_URL = '/services/quotes-money/quote'


class CedroClient:

    def __init__(self, parser=None):
        self.quotes = QuotesClient(parser)
        self.currencies = CurrenciesClient(parser)
