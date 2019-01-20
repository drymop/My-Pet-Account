from collections import namedtuple
import requests
from datetime import datetime
from pprint import pprint as pp


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