from mytools import wallet
import mytools
import requests
import time
from web3 import Web3, HTTPProvider
import sha3
import eth_abi


contact_addr = '0x7573933eB12Fa15D5557b74fDafF845B3BaF0ba2'

# 'address': (昵称随便写, 猫咪编号)
catDic = {
}

def getPramHex(paramsTypes, params):
    code = eth_abi.encode(paramsTypes, params)
    return code.hex()


# 方法签名，前四个字节
def getMethodSig(name, paramsTypes):
    result = sha3.keccak_256()
    inputt = name + '('
    for i, t in enumerate(paramsTypes):
        inputt = inputt + t
        if i == len(paramsTypes) - 1:
            inputt = inputt + ')'
        else:
            inputt = inputt + ','

    result.update(inputt.encode('ascii'))
    a = result.hexdigest()[0:8]
    return a


def feed(wallet, tokenID):
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('feedCat', ['uint256'])
    tx = mytools.call_method(wallet, contact_addr, 0,
                             methodSig + paramsHex, 0, 300000)
    print(tx)


def levelup(wallet, tokenID):
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('levelUp', ['uint256'])
    tx = mytools.call_method(wallet, contact_addr, 0,
                             methodSig + paramsHex, 0, 300000)
    print(tx)


def clean(wallet, tokenID):
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('cleanCat', ['uint256'])
    tx = mytools.call_method(wallet, contact_addr, 0,
                             methodSig + paramsHex, 0, 300000)
    print(tx)


def acceptPlayDate(wallet, tokenID, inviteTokenID):
    methodSig = getMethodSig('acceptPlayDate', ['uint256', 'uint256'])
    paramsHex = getPramHex(['uint256', 'uint256'], [tokenID, inviteTokenID])
    tx = mytools.call_method(wallet, contact_addr, 0,
                             methodSig + paramsHex, 0, 300000)
    print(tx)


def inviteCatForPlaying(wallet, tokenID, inviteeTokenID):
    methodSig = getMethodSig('inviteCatForPlaying', ['uint256', 'uint256'])
    paramsHex = getPramHex(['uint256', 'uint256'], [tokenID, inviteeTokenID])
    tx = mytools.call_method(wallet, contact_addr, 0,
                             methodSig + paramsHex, 0, 300000)
    print(tx)


def canClean(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('canClean', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    int_val = int.from_bytes(res, "big")
    return int_val


def canFeed(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('canFeed', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    int_val = int.from_bytes(res, "big")
    return int_val


def canLevelUp(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('canLevelUp', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    int_val = int.from_bytes(res, "big")
    return int_val


def canPlay(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('canPlay', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    int_val = int.from_bytes(res, "big")
    return int_val


def isFullLevel(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('getLevel', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    int_val = int.from_bytes(res, "big")
    return int_val >= 20


# 找到pair的ID，忽略其他人的邀请；这个调用返回结果是个数组，没看明白怎么编码成byte的；就简单匹配猫咪id了
def getPlayInviteIds(tokenID, targetInviteID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('getPlayInviteIds', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    # int_val = int.from_bytes(res, "big")

    hexStr = res.hex()
    # print(hexStr)

    isIn: bool = False
    # 从后往前找，一次找64个字符
    cursor = 0

    while(cursor < len(hexStr)):
        if cursor == 0:
            sub = hexStr[-cursor - 64:]
        else:
            sub = hexStr[-cursor - 64:-cursor]
        # print(sub)
        try:
            num = int(sub, 16)
        except:
            # print('err')
            isIn = isIn or False
        else:
            # print(num)
            if num == targetInviteID:
                isIn = True
                break
        cursor += 64
    return isIn


def getPendingInvitesList(tokenID):
    w3 = mytools.getWeb3Solidy()
    paramsHex = getPramHex(['uint256'], [tokenID])
    methodSig = getMethodSig('getPendingInvitesList', ['uint256'])
    res = w3.eth.call({'value': 0, 'gas': 3000000, 'maxFeePerGas': 200000000000, 'maxPriorityFeePerGas': 1000000000,
                       'to': contact_addr, 'data': methodSig + paramsHex})
    # int_val = int.from_bytes(res, "big")

    hexStr = res.hex()
    return len(hexStr) > 200


def handleCat(wallet, myToken, pairToken, Name):
    canDoAnyThing = False
    print("开始处理" + Name + "小猫")
    if isFullLevel(myToken) == True:
        print(Name + "小猫满级了")
        return canDoAnyThing
    if canLevelUp(myToken) == 1:
        print("开始升级猫：" + Name)
        canDoAnyThing = True
        levelup(wallet, myToken)
        time.sleep(2)
    if canPlay(myToken) == 1:
        print("小猫" + Name + "可以玩")
        if getPlayInviteIds(myToken, pairToken) == True:
            print("收到朋友的邀请")
            canDoAnyThing = True
            acceptPlayDate(wallet, myToken, pairToken)
            print("和朋友玩")
            time.sleep(2)
        elif getPendingInvitesList(myToken) == False:
            print("没有在邀请别人")
            canDoAnyThing = True
            inviteCatForPlaying(wallet, myToken, pairToken)
            print("邀请朋友")
            time.sleep(2)
    if canFeed(myToken) == 1:
        print("开始喂猫：" + Name)
        canDoAnyThing = True
        feed(wallet, myToken)
        time.sleep(2)
    if canClean(myToken) == 1:
        print("开始洗澡：" + Name)
        canDoAnyThing = True
        clean(wallet, myToken)
        time.sleep(2)

    return canDoAnyThing


if __name__ == '__main__':
    walletList = []
    # 读取地址和私钥
    with open('your_wallet_file', 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            tuple = line.split('\t')
            w = wallet(tuple[0], tuple[1])
            # print(tuple[1])
            walletList.append(w)
    rpc = 'https://rpc.ankr.com/polygon'
    mytools.createWeb3(rpc)

    # # 两个小猫为一对，分别遍历两个小猫，
    # # 按照顺序，levelup accpectinvite invite feed clean 来回遍历
    # # 如果有能做的就执行，如果两个小猫都么有任何能做的就结束
    # # 没找到小猫的tokenid是从哪读的，所以先写死

    while(True):
        for i, k in enumerate(walletList):
            if i % 2 == 0:
                walletA = k
                walletB = walletList[i + 1]
                # 没有地址跳过
                if not walletA.address in catDic:
                    continue
                tokenIDA = catDic[walletA.address][1]
                tokenIDB = catDic[walletB.address][1]
                NameA = catDic[walletA.address][0]
                NameB = catDic[walletB.address][0]

                canDoAnyThing = True

                while(canDoAnyThing):
                    canDoAnyThing = False
                    canDoAnyThing = handleCat(
                        walletA, tokenIDA, tokenIDB, NameA)
                    canDoAnyThing = handleCat(
                        walletB, tokenIDB, tokenIDA, NameB) or canDoAnyThing
