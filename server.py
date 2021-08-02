import hashlib as hasher
import datetime as date
import os
import time
import json
import threading
from flask import Flask

block_base="blocks/"

address="guocf-addr"
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.version = 1
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.trans="a"
        coinbase={}
        coinbase["sender"]="mining"
        coinbase["receiver"]="guocf-addr"
        coinbase["value"]=1
        self.transactions=coinbase
        self.hash = self.hash_block()
        self.write_block_file()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.transactions)).encode('utf-8'))
        return sha.hexdigest()

    def create_genesis_block():
# Manually construct a block with
# index zero and arbitrary previous hash
        return Block(0, date.datetime.now(), "guocf-2021-7-30", "0")

    def next_block(last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = "Hey! I'm block " + str(this_index)
        this_hash = last_block.hash
        return Block(this_index, this_timestamp, this_data, this_hash)

    def block2json(self):
        dic={}
        dic["index"] = self.index
        dic["time"] = str(self.timestamp)
        dic["data"] = str(self.data)
        dic["prev_hash"]=self.previous_hash
        dic["hash"]=self.hash
        dic["tran"]=self.transactions
        js = json.dumps(dic)
        print(js)
        return js
    def write_block_file(self):
        with open(block_base+str(self.index), "w") as f:
            f.write(self.block2json())

class BlockChain:
      blockchain=[]

      def __init__(self, filename):
          ret=os.access(filename, os.W_OK)  
          if ret == False:
              BlockChain.blockchain=[Block.create_genesis_block()]
          else:
              pass

      def get_prev_block():
          return BlockChain.blockchain[-1]

      def add(self, block):
          BlockChain.blockchain.append(block)
      def print_blocks(self):
          for i in BlockChain.blockchain:
              i.block2json()

#blockchain = [Block.create_genesis_block()]
#previous_block = blockchain[0]

blockchain = BlockChain("coin.db")
def mining_thread():
    print("starting mining thread\n")
    while True:
        print("mining...\n")
        time.sleep(2)
        prev=BlockChain.get_prev_block()
        new_block=Block.next_block(prev)
        blockchain.add(new_block)
        blockchain.print_blocks()
	
def rpc_thread():
    while True:
        print("rpc_thread\n")
        time.sleep(5)

mining_t=threading.Thread(target=mining_thread, name="mining thread")
mining_t.start()

rpc_t=threading.Thread(target=rpc_thread, name="rpc_thread")
rpc_t.start()

app =Flask(__name__)

@app.route("/")
def getblockheight():
    return str(len(BlockChain.blockchain))

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/lastblock')
def getlastblock():
    return BlockChain.get_prev_block().block2json()

def rest_thread():
    app.run(debug=True, use_reloader=False)


rest_t=threading.Thread(target=rest_thread)
rest_t.start()

import asyncio
import datetime
import random
import websockets

async def websocket_time(websocket, path):
    while True:
        #now = datetime.datetime.utcnow().isoformat() + "Z"
        now = BlockChain.get_prev_block().block2json()
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)


def websocket_thread():
    new_loop= asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)   
    start_server = websockets.serve(websocket_time, "127.0.0.1", 5678)
    new_loop.run_until_complete(start_server)
    new_loop.run_forever()

main_websocket_t = threading.Thread(target=websocket_thread)
main_websocket_t.start()

