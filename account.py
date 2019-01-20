import requests

API_KEY = 'd7d2263e1acab85c1f6020b064745864'
DEFAULT_ACCOUNT_ID = '5c43b4ca322fa06b677943fc'

ACCOUNT_URL = 'http://api.reimaginebanking.com/accounts/{id}'

class Account:
    data = None

    def __init__(self, account_id):
        self._id = account_id
        self.acc_url = ACCOUNT_URL.format(id=self._id)
        # self.data = dict()

        # for attr in ['deposits', 'withdrawals', 'purchases']:
        #     self.data[attr] = self[attr]

    def _get_account_info(self):
        data = requests.get(self.acc_url, params={'key': API_KEY}).json()
        return data

    def _get(self, what):
        data = requests.get(self.acc_url + '/{}'.format(what), params={'key': API_KEY}).json()
        return data

    def __getitem__(self, key):
        return self._get(key)

    # def get_deposits(self):
    #     data = requests.get(self.acc_url + '/deposits', params={'key': API_KEY}).json()
    #     return data
    #
    # def get_withdrawals(self):
    #     data = self._get('withdrawals')
    #     return data
    #
    # def get_purchases(self):
    #     return self._get('purchases')


    def __str__(self):
        info = '\tname: {}\n\tif: {}\n\tbalance: {}'.format(self.name,
                                                            self.acctnumber,
                                                            self.money)

if __name__ == '__main__':
    acc = Account(DEFAULT_ACCOUNT_ID)

    pur = acc['purchases']
    wid = acc['withdrawals']
    dep = acc['deposits']

    for what in [pur, wid, dep]:
        try:
            for thing in what:
                print(thing)
        except TypeError:
            raise
        print('\n\n')
