# -*- coding: utf-8 -*-
# written by junying, 2019-06-11

import os

def getitems(filepath):
    if not os.path.exists(filepath): return []
    items = []
    with open(filepath,'r') as file:
        for line in file: items.append(line.split())
    return items

from tx import transfer,accountinfo
from key import privkey2addr
import threading
import sys
import multiprocessing
from functools import partial
from multiprocessing import Process

def accumulate(toaddr = 'htdf18rudpyaewcku05c87xzgaw4rl8z3e5s6vefu4r',
               privkeyfile = 'htdf.privkey',
               restapi='47.98.194.7:1317', chainid='testchain',
               ndefault_gas=200000,ndefault_fee=20):
    for item in getitems(privkeyfile):
        hrp = item[0].lower()
        fromprivkey = item[2]
        try: frompubkey,fromaddr = privkey2addr(fromprivkey,hrp)
        except: continue
        if fromaddr != item[1] or hrp != fromaddr[:4]: continue
        balance, _, _ = accountinfo(fromaddr,restapi)
        namount = balance * (10**8) - ndefault_fee#以satoshi为单位,    1USDP  = 10^8 satoshi    1HTDF=10^8 satoshi
        if namount < 0: continue
        #try: threading.Thread(target=transfer,args=(hrp,fromprivkey, toaddr, namount, chainid, ndefault_fee, ndefault_gas,restapi)).start()
        try: Process(target=transfer,args=(hrp,fromprivkey, toaddr, namount, chainid, ndefault_fee, ndefault_gas,restapi)).start()
        except: print("Error: unable to start thread")

blk_time=30
def distr(fromprivkey='c9960987611a40cac259f2c989c43a79754df356415f164ad3080fdc10731e65',
          hrp='htdf',privkeyfile = 'htdf.privkey',
          restapi='47.98.194.7:1317', chainid='testchain',
          ndefault_gas=200000,ndefault_fee=20, nAmount = 0.001234 * (10**8)):
    for item in getitems(privkeyfile):
        toaddr=item[1]
        transfer(hrp,fromprivkey, toaddr, nAmount, chainid, ndefault_fee, ndefault_gas,restapi)
        import time
        time.sleep(blk_time)


def report(privkeyfile='htdf.privkey',restapi='47.98.194.7:1317'):
    balance = 0
    params = []
    for item in getitems(privkeyfile):
        addr=item[1]
        params.append(addr)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    prod_x=partial(accountinfo, debug=True)
    prod_y=partial(prod_x, restapi=restapi)
    outputs = pool.map(prod_y,params)
    print(sum(output[0] for output in outputs if output[0]>0))
    
if __name__ == "__main__":
    #getitems('db/htdf.privkey')
    #distr('db/htdf.privkey')
    report('db/htdf.privkey')
    # accumulate(toaddr = 'htdf18rudpyaewcku05c87xzgaw4rl8z3e5s6vefu4r',
    #            privkeyfile = 'htdf.privkey',
    #            restapi='47.98.194.7:1317', chainid='testchain',
    #            ndefault_gas=200000,ndefault_fee=20)