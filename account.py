from collections import namedtuple
import requests
from datetime import datetime
from pprint import pprint as pp
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse

API_KEY = 'd7d2263e1acab85c1f6020b064745864'
DEFAULT_ACCOUNT_ID = '5c43b4ca322fa06b677943fc'

ACCOUNT_URL = 'http://api.reimaginebanking.com/accounts/{id}'

Delta = namedtuple('Delta', 'type id date amount')
END_POINTS = ['deposit', 'withdrawal', 'purchase', 'transfer']

class Account:

    def __init__(self, account_id):
        self._id = account_id
        self.acc_url = ACCOUNT_URL.format(id=self._id)
        self.handlers = {
            'deposit': self._get_deposits,
            'withdrawal': self._get_withdrawals,
            'purchase': self._get_purchases,
            'transfer': self._get_transfers,
        }

        self.deltas = {end_point: [] for end_point in self.handlers}

    def update(self):
        new_deltas = {end_point: handler() for end_point, handler in self.handlers.items()}
        self.deltas = new_deltas
        print(self.deltas)
        m, b = self.handle_data(self.deltas)
        return m, b, self._get_account_info()['balance']

    def handle_data(self, deltas):
        concat = [item for sublist in deltas.values() for item in sublist]
        # concat = concat[len(concat)/2:]
        concat.sort(key=lambda item: item.date)
        current = 0
        now = datetime.now().timestamp()
        x, y = [], []
        for item in concat:
            current += item.amount
            x.append((item.date.timestamp()-now)/8e4)
            y.append(float(current))

        x, y = np.array(x).reshape(-1, 1), np.array(y).reshape(-1, 1)

        print(x,y)

        reg = LinearRegression()
        reg.fit(X=x, y=y)

        [[m]], [b] = reg.coef_, reg.intercept_

        return m, b

    def _get_account_info(self):
        data = requests.get(self.acc_url, params={'key': API_KEY}).json()
        return data

    def _get(self, what):
        data = requests.get(self.acc_url + '/{}'.format(what), params={'key': API_KEY}).json()
        return data

    def _get_purchases(self):
        data = self._get('purchases')
        purchases = []
        for x in data:
            try:
                if x['status'] != 'cancelled':
                    date = self._str2date(x['purchase_date'])
                    purchases.append(Delta('purchase', x['_id'], date, -x['amount']))
            except:
                pass
        return purchases

    def _get_deposits(self):
        data = self._get('deposits')
        deposits = []
        for x in data:
            try:
                if x['status'] != 'cancelled':
                    date = self._str2date(x['transaction_date'])
                    deposits.append(Delta('deposit', x['_id'], date, x['amount']))
            except:
                pass
        return deposits

    def _get_withdrawals(self):
        data = self._get('withdrawals')
        withdrawals = []
        for x in data:
            try:
                if x['status'] != 'cancelled':
                    date = self._str2date(x['transaction_date'])
                    withdrawals.append(Delta('withdrawal', x['_id'], date, -x['amount']))
            except:
                pass
        return withdrawals

    def _get_transfers(self):
        data = self._get('transfers')
        transfers = []
        for x in data:
            try:
                if x['status'] != 'cancelled':
                    date = self._str2date(x['transaction_date'])
                    amount = x['amount']
                    if x['payer_id'] == self._id:
                        amount = -amount
                    purchases.append(Delta('transfer', x['_id'], date, amount))
            except:
                pass
        return transfers

    def _str2date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d') #yyyy-mm-dd

    def __str__(self):
        info = '\tname: {}\n\tif: {}\n\tbalance: {}'.format(self.name,
                                                            self.acctnumber,
                                                            self.money)

if __name__ == '__main__':
    acc = Account(DEFAULT_ACCOUNT_ID)

    acc.update()
    pp(acc.deltas)
