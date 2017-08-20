"""
   (Unofficial) Poloniex.com API written in Python 3, supports Streaming, and API calls. (https://github.com/a904guy/poloniex-python3)
   Author: Andy Hawkins
   Website: (http://hawkins.tech)

 _   _                _    _           _____         _
| | | |              | |  (_)         |_   _|       | |
| |_| | __ ___      _| | ___ _ __  ___  | | ___  ___| |__
|  _  |/ _` \ \ /\ / / |/ / | '_ \/ __| | |/ _ \/ __| '_ \
| | | | (_| |\ V  V /|   <| | | | \__ \_| |  __/ (__| | | |
\_| |_/\__,_| \_/\_/ |_|\_\_|_| |_|___(_)_/\___|\___|_| |_|

   ANDY@HAWKINS.TECH   -  HAWKINS.TECH
   November, 7th 2016

   Tested:
   Ubuntu 16.10, Python 3.5.2
   See README.md for instructions

   Documentation: https://poloniex.com/support/api/
"""

import hashlib
import hmac
import json
import time
import sys
import urllib

import requests
from autobahn.twisted.component import Component, run
from requests.auth import AuthBase
from ratelimiter import RateLimiter
from twisted.internet.defer import inlineCallbacks
from twisted.internet.ssl import CertificateOptions

from src.utils import retry_on_status_code


PUBLIC_TOPICS = ['returnTicker', 'return24Volume', 'returnOrderBook', 'returnTradeHistory',
                 'returnChartData', 'returnCurrencies', 'returnLoanOrders']


class PoloniexException(Exception):
    pass


class API:
    # http
    public_url = "https://poloniex.com/public"
    private_url = "https://poloniex.com/tradingApi"
    topic = None
    limiter = None
    max_calls = 6
    max_period = 60
    secrets = None

    # wamp
    ws_uri = "wss://api.poloniex.com"
    ws_realm = "realm1"
    runner = None
    callback = None

    class PoloniexAuth(AuthBase):

        def __init__(self, apikey: str, secret: str):
            self.apikey = apikey
            self.secret = secret

        def __call__(self, request):
            signature = hmac.new(self.secret, request.body.encode(), hashlib.sha512).hexdigest()
            request.headers['Key'] = self.apikey
            request.headers['Sign'] = signature
            return request

    def __init__(self, apikey: str, secret: str):
        self.auth = self.PoloniexAuth(apikey, secret)
        self.limiter = RateLimiter(max_calls=self.max_calls, period=self.max_period)

    # WAMP Streaming API

    def subscribe(self, topic: str, callback: callable):
        self.wamp = Component(
            realm='realm1',
            transports=[{
                'endpoint': {
                    'type': 'tcp',
                    'host': 'api.poloniex.com',
                    'port': 443,
                    'tls': CertificateOptions()
                },
                'type': 'websocket',
                'url': 'wss://api.poloniex.com',
                'options': {
                    'open_handshake_timeout': 60.0
                }
            }]
        )

        @self.wamp.on_join
        @inlineCallbacks
        def join(session, details):
            yield session.subscribe(callback, topic)

        run(self.wamp)

    # Public HTTP API, no credentials needed.

    def returnTicker(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def return24Volume(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnOrderBook(self, currencyPair: str = 'BTC_NXT', depth: int = 10):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnTradeHistory(self, currencyPair: str = 'BTC_NXT', start: int = 1410158341, end: int = 9999999999):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnChartData(self, currencyPair: str = 'BTC_NXT', start: int = 1405699200, end: int = 9999999999, period: int = 14400):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnCurrencies(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnLoanOrders(self, currency: str = 'BTC'):
        return self._call(sys._getframe().f_code.co_name, locals())

    # Private HTTP API Methods, Require API Key, and Secret on INIT

    def returnBalances(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnCompleteBalances(self, account: str = 'all'):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnDepositAddresses(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def generateNewAddress(self, currency: str = 'BTC'):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnDepositsWithdrawals(self, start: int = 1410158341, end: int = 1410499372):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnOpenOrders(self, currencyPair: str = 'BTC_XCP'):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnOrderTrades(self, orderNumber: int = None):
        return self._call(sys._getframe().f_code.co_name, locals())

    def buy(self, rate: float, amount: float, currencyPair: str, fillOrKill: int, immediateOrCancel: int, postOnly: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def sell(self, rate: float, amount: float, currencyPair: str, fillOrKill: int, immediateOrCancel: int, postOnly: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def cancelOrder(self, orderNumber: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def moveOrder(self, orderNumber: int, rate: float, amount: float, immediateOrCancel: int, postOnly: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def withdraw(self, currency: str, amount: float, address: str, paymentId: str):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnFeeInfo(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnAvailableAccountBalances(self, account: str = 'all'):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnTradableBalances(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def transferBalance(self, currency: str, amount: float, fromAccount: str, toAccount: str):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnMarginAccountSummary(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def marginBuy(self, currencyPair: str, rate: float, amount: float):
        return self._call(sys._getframe().f_code.co_name, locals())

    def marginSell(self, currencyPair: str, rate: float, amount: float):
        return self._call(sys._getframe().f_code.co_name, locals())

    def getMarginPosition(self, currencyPair: str):
        return self._call(sys._getframe().f_code.co_name, locals())

    def closeMarginPosition(self, currencyPair: str):
        return self._call(sys._getframe().f_code.co_name, locals())

    def createLoanOffer(self, currency: str, amount: float, duration: int, autoRenew: int, lendingRate: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def cancelLoanOffer(self, orderNumber: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def returnOpenLoanOffers(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnActiveLoans(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def returnLendingHistory(self):
        return self._call(sys._getframe().f_code.co_name, {})

    def toggleAutoRenew(self, orderNumber: int):
        return self._call(sys._getframe().f_code.co_name, locals())

    def _call(self, topic: str, args: dict = {}):
        args.pop('self', None)

        is_public = topic in PUBLIC_TOPICS
        url = self.public_url if is_public else self.private_url
        method = 'GET' if is_public else 'POST'

        @retry_on_status_code([500, 502, 503, 504])
        def __call(data):
            data['command'] = topic
            if is_public:
                request_kwargs = {
                    'params': data
                }
            else:
                data['nonce'] = int(time.time() * 1000)
                request_kwargs = {
                    'auth': self.auth,
                    'data': data
                }

            return requests.request(method, url, **request_kwargs)

        with self.limiter:
            resp =  __call(args)

        resp_content = resp.json()
        if 'error' in resp_content:
            raise PoloniexException(resp_content.get('error'))
        resp.raise_for_status()

        return resp_content
