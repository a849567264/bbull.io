import requests
import time
import hashlib
from collections import OrderedDict


class bbull:
    def __init__(self, apiKey='', secret=''):
        self.base_url = 'https://openapi.bbull.io/exchange-open-api'
        self.apiKey = apiKey
        self.secret = secret

    def __transfer_symbol(self, symbol):
        return ''.join(''.join(symbol.split('/')).split('_')).lower()

    def __sign(self, params):
        params_ordered = OrderedDict()
        keys = sorted(params.keys())
        for k in keys:
            params_ordered[k] = params[k]
        params_str = ''.join([str(key)+str(params_ordered[key]) for key in params_ordered])
        sign = hashlib.md5((params_str + self.secret).encode(encoding='utf-8')).hexdigest()
        return sign

    def __public_GET(self, api_url, **kwargs):
        url = self.base_url + api_url + '?' + '&'.join([str(key) + '=' + str(kwargs[key]) for key in kwargs])
        return requests.get(url).json()

    def __private_GET(self, api_url, **kwargs):
        sign = self.__sign(kwargs)
        url = self.base_url + api_url + '?' + '&'.join([str(key) + '=' + str(kwargs[key]) for key in kwargs]) + '&sign=' + sign
        return requests.get(url).json()

    def __private_POST(self, api_url, **kwargs):
        sign = self.__sign(kwargs)
        url = self.base_url + api_url + '?' + '&'.join([str(key) + '=' + str(kwargs[key]) for key in kwargs]) + '&sign=' + sign
        return requests.post(url).json()

    def get_symbols(self):
        return self.__public_GET('/open/api/common/symbols')

    def get_markets(self):
        return self.__private_GET('/open/api/market', api_key=self.apiKey, time=str(int(time.time())))

    def get_order_list(self, symbol, pageSize=100, page=1):
        symbol = self.__transfer_symbol(symbol)
        return self.__private_GET('/open/api/new_order', symbol=symbol,pageSize=pageSize, page=page,api_key=self.apiKey, time=str(int(time.time())))

    def get_balance(self):
        return self.__private_GET('/open/api/user/account', api_key=self.apiKey, time=str(int(time.time())))

    def get_order_info(self, order_id, symbol):
        symbol = self.__transfer_symbol(symbol)
        return self.__private_GET('/open/api/order_info', order_id=order_id, symbol=symbol, api_key=self.apiKey, time=str(int(time.time())))

    def get_all_trades(self, symbol, pageSize=100, page=1):
        symbol = self.__transfer_symbol(symbol)
        return self.__private_GET('/open/api/all_trade', symbol=symbol, pageSize=pageSize, page=page, api_key=self.apiKey, time=str(int(time.time())))

    def creat_order(self, symbol, side, ordertype, volume, price):
        symbol = self.__transfer_symbol(symbol)
        type = [1, 2][ordertype == 'market']
        price = [price, None][type == 2]
        return self.__private_POST('/open/api/create_order', side=side, type=type, volume=volume, price=price, symbol=symbol, api_key=self.apiKey, time=str(int(time.time())))

    def cancel_order(self, symbol, orderid):
        symbol = self.__transfer_symbol(symbol)
        return self.__private_POST('/open/api/cancel_order', order_id=orderid, symbol=symbol, api_key=self.apiKey, time=str(int(time.time())))

    def cancel_all(self, symbol):
        symbol = self.__transfer_symbol(symbol)
        return self.__private_POST('/open/api/cancel_order_all', symbol=symbol, api_key=self.apiKey, time=str(int(time.time())))

    def get_kline(self, symbol, period):
        symbol = self.__transfer_symbol(symbol)
        return self.__public_GET('/open/api/get_records', symbol=symbol, period=period)

    def get_trades(self, symbol):
        symbol = self.__transfer_symbol(symbol)
        return self.__public_GET('/open/api/get_trades', symbol=symbol)

    def get_ticker(self, symbol):
        symbol = self.__transfer_symbol(symbol)
        return self.__public_GET('/open/api/get_ticker', symbol=symbol)

    def get_depth(self, symbol, type='step0'):
        symbol = self.__transfer_symbol(symbol)
        return self.__public_GET('/open/api/market_dept', symbol=symbol, type=type)
