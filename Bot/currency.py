from urllib.request import urlopen, Request

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


class Currency:
    def __init__(self):
        self.urls = [('https://www.melhorcambio.com/dolar-hoje', 'Dolar'),
                     ('https://www.melhorcambio.com/euro-hoje', 'Euro'),
                     ('https://www.melhorcambio.com/libra-hoje', 'Libra'),
                     ('https://www.melhorcambio.com/dolar-australiano-hoje', 'Dolar Australiano'),
                     ('https://www.melhorcambio.com/dolar-canadense-hoje', 'Dolar Canadense')
                     ]
        self.find = 'class="text-verde"'

    def fetch(self, index):
        req = Request(self.urls[index][0], headers=HEADERS)
        content = str(urlopen(req).read())
        pos = int(content.index(self.find) + len(self.find))
        return f'{self.urls[index][1]} = ' + str(content[pos - 25: pos - 19]).replace('\"', '')


if __name__ == '__main__':
    pass
