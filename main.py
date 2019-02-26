from parser import crawl_etherscan
from visualizer import histogram

if __name__ == '__main__':
    blocks_fee = crawl_etherscan(7266470, 100)
    print(blocks_fee)
    print(min(blocks_fee))
    histogram(blocks_fee)
