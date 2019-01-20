from collections import namedtuple
import requests
from datetime import datetime

API_KEY = 'd7d2263e1acab85c1f6020b064745864'
DEFAULT_ACCOUNT_ID = '5c43b4ca322fa06b677943fc'

ACCOUNT_URL = 'http://api.reimaginebanking.com/accounts/{id}'

Delta = namedtuple('Delta', 'date ammount')

class Account:
    def __init__(self, account_id):
        self._id = account_id
        self.acc_url = ACCOUNT_URL.format(id=self._id)

    def _get_account_info(self):
        data = requests.get(self.acc_url, params={'key': API_KEY}).json()
        return data

    def get_deposits(self):
        data = requests.get(self.acc_url + '/deposits', params={'key': API_KEY}).json()
        return data

    def get_purchases(self):
        data = requests.get(self.acc_url + '/purchases', params={'key': API_KEY}).json()
        purchases = []
        for x in data:
            if x['status'] != 'cancelled':
                date = self._str2date(x['purchase_date'])
                ammount = x['amount']
                purchases.append(Delta(date, ammount))
        return purchases

    def _str2date(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%d') #yyyy-mm-dd










    def __str__(self):
        info = '\tname: {}\n\tif: {}\n\tbalance: {}'.format(self.name,
                                                            self.acctnumber,
                                                            self.money)

acc = Account(DEFAULT_ACCOUNT_ID)
purs = acc.get_purchases()
