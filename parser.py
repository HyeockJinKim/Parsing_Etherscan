import ssl
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

ETHERSCAN_URL = 'https://etherscan.io/txs?block='


def set_request(url):
    refer_head = 'http://www.google.com/'
    connection_head = 'keep-alive'
    user_head = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome'

    context = ssl._create_unverified_context()
    request = Request(url)
    request.add_header('User-Agent', user_head)
    request.add_header('referer', refer_head)
    request.add_header('Connection', connection_head)

    response = urlopen(request, context=context).read()
    html = BeautifulSoup(response, 'html.parser')
    return html


def parse_html(html):
    body = html.find(attrs={'class': 'table-hover'}).find('tbody')
    txs = body.find_all('tr')
    tx_fee = [tx.find_all('td')[-1].text for tx in txs]

    return tx_fee


def crawl_etherscan(block_num, block_range):
    blocks_tx_fee = []
    for i in range(block_num, block_num-block_range, -1):
        tx_fees = []
        for j in range(1, 100, 1):
            try:
                url = ETHERSCAN_URL+str(i)+'&p='+str(j)
                html = set_request(url)
                fee = parse_html(html)
                tx_fees += fee
            except:
                break
        blocks_tx_fee.append(tx_fees)

    return blocks_tx_fee


if __name__ == '__main__':
    blocks_fee = crawl_etherscan(7265262, 5)
    print(blocks_fee)
