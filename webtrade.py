#!/usr/bin/python

from flask import Flask, jsonify, request, abort
from bitkub_v2 import BitKub
import json

app = Flask(__name__)


@app.route('/tradingview', methods=['POST'])
def process_tradingview(buy_value=3000):
    input = json.loads(request.data)
    # sym = input['symbol'][:3]
    sym = input['symbol'].replace('THB', '')
    if input['cmd'] == 'sell':
        bk = BitKub()
        sym_balance = bk.get_balance(sym)
        if sym_balance > 0.00:
            sell_response = bk.sell(sym, rate=input['price'], amount=sym_balance, typ='limit')
    elif input['cmd'] == 'buy':
        bk = BitKub()
        thb_balance = bk.get_balance('THB')
        sym_balance = bk.get_balance(sym)
        if buy_value <= thb_balance and sym_balance == 0.00:
            buy_response = bk.buy(sym, rate=input['price'], amount=buy_value, typ='limit')
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8899)
