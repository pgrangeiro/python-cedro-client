import vcr
from unittest import TestCase
from unittest.mock import patch, Mock

from cedro.clients import BaseClient, CedroClient, QuotesClient, CurrenciesClient
from cedro.parsers import NullableParser
from cedro.exceptions import HttpAuthenticationError


class BaseClientTestCase(TestCase):

    def setUp(self):
        self.stub_client_class = type('StubClass', (BaseClient, ), {})
        self.client = self.stub_client_class()
        self.fixtures_path = f'cedro/tests/fixtures'

    def test_login_succesfully(self):
        with vcr.use_cassette(f'{self.fixtures_path}/login.json'):
            self.client.login('user', 'password')

    def test_initializes_instance_correctly(self):
        self.assertEqual(NullableParser, self.client.parser)

    def test_initializes_instance_with_parser_correctly(self):
        client = self.stub_client_class('parser')
        self.assertEqual('parser', client.parser)

    def test_login_raises_exception_when_response_not_ok(self):
        with vcr.use_cassette(f'{self.fixtures_path}/login-error.json'):
            self.assertRaises(HttpAuthenticationError, self.client.login, 'xpto', 'passwd')

    def test_url_returns_correct_data(self):
        self.client.PATH_URL = '/XABLAU'

        self.assertEqual(
            'http://webfeeder.cedrofinances.com.br/XABLAU',
            self.client.url
        )


class QuotesClientTestCase(TestCase):

    def setUp(self):
        self.client = QuotesClient()
        self.fixtures_path = f'cedro/tests/fixtures'

    def test_initializes_instance_correctly(self):
        self.assertTrue(isinstance(self.client, BaseClient))
        self.assertEqual('/services/quotes/quote', self.client.PATH_URL)

    def test_build_url_params_correctly(self):
        tickers = ['XPTO', 'PXTO']

        params = self.client.build_params(tickers)
        self.assertEqual('xpto/pxto', params)

    def test_build_url_with_params_correctly(self):
        tickers = ['XPTO', 'PXTO']

        url = self.client.build_url(tickers)
        self.assertEqual('http://webfeeder.cedrofinances.com.br/services/quotes/quote/xpto/pxto', url)

    def test_get_returns_response_data_correctly(self):
        request = Mock()
        first, second = Mock(), Mock()
        request.get().json.return_value = (first, second)
        self.client._request = request

        tickers = ['XPTO', 'PXTO']
        expected_url = 'http://webfeeder.cedrofinances.com.br/services/quotes/quote/xpto/pxto'

        data = list(self.client.get(tickers))

        request.get.assert_called_with(expected_url)
        self.assertTrue(request.get().close.called)

    def test_get_returns_parsed_data_correctly(self):
        request = Mock()
        first, second = Mock(), Mock()
        request.get().json.return_value = [first, second]
        self.client._request = request

        parser = Mock()
        p_first, p_second = Mock(), Mock()
        parser.parse.side_effect = (p_first, p_second)
        self.client.parser = parser

        tickers = ['XPTO', 'PXTO']
        data = list(self.client.get(tickers))

        self.assertEqual(2, parser.parse.call_count)
        parser.parse.assert_any_call(first)
        parser.parse.assert_any_call(second)
        self.assertEqual([p_first, p_second], data)


class CurrenciesClientTestCase(TestCase):

    def setUp(self):
        self.client = CurrenciesClient()

    def test_initializes_instance_correctly(self):
        self.assertTrue(isinstance(self.client, BaseClient))
        self.assertEqual('/services/quotes-money/quote', self.client.PATH_URL)


class CedroClientTestCase(TestCase):

    def setUp(self):
        self.client = CedroClient()

    def test_initializes_instance_correctly(self):
        self.assertTrue(isinstance(self.client.quotes, QuotesClient))
        self.assertTrue(isinstance(self.client.currencies, CurrenciesClient))

    def test_initializes_instance_with_parser_correctly(self):
        client = CedroClient('parser')
        self.assertEqual('parser', client.quotes.parser)
        self.assertEqual('parser', client.currencies.parser)
