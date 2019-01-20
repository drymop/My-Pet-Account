

class Account:
    name = None
    acctnumber = None
    money = None

    def __init__(self, name='blob-dude', acctnumber=0, money=float('-inf')):
        self.name = name
        self.acctnumber = acctnumber
        self.money = money

    def __str__(self):
        info = '\tname: {}\n\tif: {}\n\tbalance: {}'.format(self.name,
                                                            self.acctnumber,
                                                            self.money)
        return info

if __name__ == '__main__':

    a = Account()
    print(a)
