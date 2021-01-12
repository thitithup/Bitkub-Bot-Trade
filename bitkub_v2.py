# -*- coding: utf-8 -*-
# !/usr/bin/python3

import hashlib
import hmac
import json
import requests

try:
    import thread
except:
    import _thread as thread

API_HOST = 'https://api.bitkub.com'
API_KEY = 'เปลี่ยน API Key ที่ได้จาก Bitkub ตรงนี้'
API_SECRET = b'เปลี่ยน API Secret ที่ได้จาก Bitkub ตรงนี้'


def json_encode(data):
    return json.dumps(data, separators=(',', ':'), sort_keys=True)


def sign(data):
    j = json_encode(data)
    h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
    return h.hexdigest()


class BitKub(object):

    def get_servertime(self):
        response = requests.get(API_HOST + '/api/servertime')
        return response.text

    def get_symbols(self):
        response = requests.get(API_HOST + '/api/market/symbols')
        data = response.json()
        if data['error'] == 0:
            result = data['result']
            for value in result:
                print(value)

    def get_status(self):
        response = requests.get(API_HOST + '/api/status')
        values = response.json()
        for value in values:
            print(value)

    def list_wallet(self):
        result = []
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/wallet', headers=header, data=json_encode(data))
        data = response.json()
        if data['error'] == 0:
            for value in data['result']:
                if data['result'][value]:
                    result.append({value: data['result'][value]})
        return result

    def get_wallet(self, symbol):
        result = 0.0
        wallets = self.list_wallet()
        for wallet in wallets:
            if symbol in wallet:
                result = wallet[symbol]
        return result

    def list_bids(self, symbol, target=0.00, limit=10):
        # List sell orders อยากขายราคาตรงนี้
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.get(API_HOST + '/api/market/bids', params={'sym': 'THB_' + symbol.upper(), 'lmt': limit})
        data = response.json()
        total = 0.00
        qty = 0.00
        if data['error'] == 0:
            result = data['result']
            for value in result:
                total = total + (value[3] * value[4])
                qty += value[4]
        return round(total, 2), round(total / qty, 4), round(qty, 7)

    def list_asks(self, symbol, target=0.00, limit=10):
        # List buy orders อยากซื้อราคาตรงนี้
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.get(API_HOST + '/api/market/asks', params={'sym': 'THB_' + symbol.upper(), 'lmt': limit})
        data = response.json()
        total = 0.00
        qty = 0.00
        if data['error'] == 0:
            result = data['result']
            for value in result:
                total = total + (value[3] * value[4])
                qty += value[4]
        return round(total, 2), round(total / qty, 4), round(qty, 7)

    def list_balances(self):
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json_encode(data))
        data = response.json()
        result = []
        if data['error'] == 0:
            for value in data['result']:
                if data['result'][value]['available']:
                    result.append({value: data['result'][value]['available']})
        return result

    def get_balance(self, symbol):
        result = 0.0
        wallets = self.list_balances()
        for wallet in wallets:
            if symbol in wallet:
                result = wallet[symbol]
        return result

    def list_orders(self, symbol):
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'ts': ts,
            'sym': 'THB_' + symbol.upper(),
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/my-open-orders', headers=header, data=json_encode(data))
        data = response.json()
        result = []
        if data['error'] == 0:
            for value in data['result']:
                result.append(value)
        return result

    def cancel_order(self, symbol, id, hash, side):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        ts = int(self.get_servertime())
        data = {
            'ts': ts,
            'sym': 'THB_' + symbol.upper(),
            'id': id,
            'hash': hash,
            'side': side,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/cancel-order', headers=header, data=json_encode(data))
        data = response.json()
        return data

    def buy(self, symbol, rate, amount, typ='limit'):  # market
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'sym': 'THB_' + symbol.upper(),
            'amt': amount,  # THB amount you want to spend
            'rat': rate,
            'typ': typ,
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/place-bid', headers=header, data=json_encode(data))
        return response.json()

    def sell(self, symbol, rate, amount, typ='limit'):  # market
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'sym': 'THB_' + symbol.upper(),
            'amt': amount,  # BTC amount you want to sell
            'rat': rate,
            'typ': typ,
            'ts': ts,
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/place-ask', headers=header, data=json_encode(data))
        return response.json()

    def my_history(self, symbol, limit=1):
        ts = int(self.get_servertime())
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': API_KEY,
        }
        data = {
            'sym': 'THB_' + symbol.upper(),
            'ts': ts,
            'lmt': limit
        }
        signature = sign(data)
        data['sig'] = signature
        response = requests.post(API_HOST + '/api/market/my-order-history', headers=header, data=json_encode(data))
        return response.json()['result']
