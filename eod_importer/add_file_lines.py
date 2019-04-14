import os, sys
import redis
from mpipe import Pipeline, UnorderedStage
IMPORT_KEY="market:%s:import:files:%s"
IMPORT_QUEUE_KEY = "market:import:queue"
ROOT_PATH="/datadrive/eod/IN"
REDIS_HOST = 'lepot_01'
REDIS_PORT = '32769'
MARKETS = ["NYSE",'NASDAQ']

def get_file_lines(path):
    with open(path, 'r') as fp:
        return fp.readlines()

def get_files(path,containing):
    files= os.listdir(path)
    return [f for f in files if containing in f]

def redis_connection(host=None,port=None):
    rc = redis.Redis(host=host or REDIS_HOST,port=port or REDIS_PORT)
    return rc

def store_file_lines(path, key):
    idx = 1
    rc= redis_connection(REDIS_HOST, REDIS_PORT)
    f_lines = get_file_lines(path)
    pipe = rc.pipeline()
    for l in f_lines[1:]:
        pipe.zadd(key, {l:idx})
        idx += 1
    pipe.sadd(IMPORT_QUEUE_KEY, key)
    result = pipe.execute()

def process_markets():
    for market in MARKETS:
        l_files =get_files(ROOT_PATH,market)
        for f in l_files[0:1000]:
            file_path = os.path.join(ROOT_PATH,f)
            out_path = os.path.join(ROOT_PATH.replace("IN","OUT"),f)
            
            store_file_lines(file_path, IMPORT_KEY % (market,f))
            os.rename(file_path,out_path)
            print("Moved imported file to %s" % f.replace("IN","OUT") )
        print("%s complete" % IMPORT_KEY % (market,f))

if "__main__" in __name__:
    process_markets()






