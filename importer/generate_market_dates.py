import redis
import os,sys
from  dateutil.parser import *
import time
EOD_DATA_PATH = '/datadrive/eod/IN'
REDIS_HOST = 'lepot_01'
REDIS_PORT = '32768'
FAAS_ENDPOINT = 'https://5aa176d5.ngrok.io'
MARKETS = ["NYSE",'NASDAQ']
MARKET_FILES_KEY="market:files:%s"
MARKET_DATES_KEY="market:dates:%s"
MARKET_NAMES_KEY="market:names"
if EOD_DATA_PATH in os.environ:
    EOD_DATA_PATH=os.environ["EOD_DATA_PATH"]

def redis_connection(host=None,port=None):
    rc = redis.Redis(host=host or REDIS_HOST,port=port or REDIS_PORT)
    return rc

def get_files(path,containing):
    files= os.listdir(path)
    return [f for f in files if containing in f]
def date_string(filename):
    if "." in filename:
        name_part = filename.split('.')[0]
        if name_part and "_" in name_part:
            dt_part = name_part.split("_")[1]
            return dt_part
    else: 
        return ""

def get_timestamp_from_dt_string(dt_string):
    parts = dt_string.split('.')
    ts_string = parts[0].split("_")[1] if "_" in parts[0] else None
    if not ts_string:
        print("parse dt failure on %s" % dt_string)
        return None
    return time.mktime(parse(ts_string).timetuple())

rc = redis_connection()
rc.delete(MARKET_NAMES_KEY)
for m in MARKETS:
    market_files_key = MARKET_FILES_KEY % m
    market_dates_key = MARKET_DATES_KEY % m
    rc.delete(market_files_key)
    rc.delete(market_dates_key)
    rc.sadd(MARKET_NAMES_KEY,m)
    all_files = get_files(EOD_DATA_PATH, m)
    print("adding z score for %s timestamps in %s" % (len(all_files),market_files_key)) 
    all_date_strings = list(filter(None,map(date_string, all_files)))
    file_timestamps = list(filter(None,map(get_timestamp_from_dt_string, all_files)))
    for f,t in zip(all_files,file_timestamps):
        rc.zadd(market_files_key, {f:t})
    print("adding  %s market dates to  %s" % (len(all_date_strings), market_dates_key))
    for d,t in zip(all_date_strings, file_timestamps):
        rc.hset(market_dates_key,d, t)

