from web3 import Web3, HTTPProvider
from eth_account.messages import encode_defunct


class wallet:
    def __init__(self, address, private):
        self.address = address
        self.private = private


web3 = Web3()
chain_id = ''
# 注意对于自定义合约，需要手动设置gas_limit


def getWeb3Solidy():
    return web3


def sign(msg, private_key):
    signed_message = web3.eth.account.sign_message(encode_defunct(
        text=msg),
        private_key=private_key)
    # print(signed_message)
    return signed_message.signature.hex()


def getBalanceInEth(address):
    balance = web3.from_wei(web3.eth.get_balance(
        Web3.to_checksum_address(address)), "ether")
    return balance


def to_checksum_address(address):
    return Web3.to_checksum_address(address)


# 对于某些gas_price不固定的网络，实时获取gas_price
def call_method(wal, target_address, amount, data='', fix_gas_price=0, gas_limit=21000):
    address = Web3.to_checksum_address(wal.address)
    private_key = wal.private
    if (fix_gas_price > 0):
        gas_price = web3.to_wei(fix_gas_price, 'gwei')
    else:
        gas_price = web3.eth.gas_price
        print("当前gas:%d" % gas_price)
        gas_price = int(gas_price * 1.0)

    nonce = web3.eth.get_transaction_count(address)
    # print(nonce)
    # print(chain_id)

    params = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(target_address),
        'value': web3.to_wei(amount, 'ether'),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': chain_id,
        'data': data,
        'from': address, }

    # print(params)

    signed_tx = web3.eth.account.sign_transaction(
        params, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=500)
    # print(tx_receipt)
    return tx_hash.hex()


def transfer_eth(wal, target_address, amount):
    call_method(wal, target_address, amount, '', 0, 21000)


def readAddressList(curAddress, fileName):
    addressList = []
    curAddress = curAddress.lower()
    with open(fileName, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if curAddress != line.lower():
                # print(line)
                addressList.append(line)
    return addressList


def createWeb3(rpc):
    global web3
    global chain_id
    web3 = Web3(HTTPProvider(rpc, request_kwargs={'timeout': 300}))
    HTTPProvider
    chain_id = web3.eth.chain_id
