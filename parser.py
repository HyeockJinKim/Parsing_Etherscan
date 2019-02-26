import ssl
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

ETHERSCAN_BASE_URL = 'https://etherscan.io'
ETHERSCAN_BLOCKS_URL = ETHERSCAN_BASE_URL+'/txs?block='


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


def get_tx_info(tx_link):
    url = ETHERSCAN_BASE_URL + tx_link.find('a')['href']
    html = set_request(url)
    gas_fee = html.find(attrs={'id': 'ContentPlaceHolder1_spanGasUsedByTxn'}).text.split('(')[0].replace(',', '')
    return int(gas_fee)


def parse_html(html):
    body = html.find(attrs={'class': 'table-hover'}).find('tbody')
    txs = body.find_all('tr')
    tx_fee = [get_tx_info(tx.find_all('td')[0]) for tx in txs]
    return tx_fee


def crawl_etherscan(block_num, block_range):
    blocks_tx_fee = []
    for i in range(block_num, block_num-block_range, -1):
        tx_fees = []
        for j in range(1, 100, 1):
            try:
                url = ETHERSCAN_BLOCKS_URL + str(i) + '&p=' + str(j)
                html = set_request(url)
                fee = parse_html(html)
                tx_fees += fee
            except:
                break
        blocks_tx_fee += tx_fees

    return blocks_tx_fee
