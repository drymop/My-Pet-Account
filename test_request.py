import requests
from pprint import pprint as pp

API_KEY = 'd7d2263e1acab85c1f6020b064745864'




r = requests.get('http://api.reimaginebanking.com/accounts', params={'key': API_KEY})
data = r.json()

account = data[0]

# update account with 