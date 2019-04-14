import redis
import os
import requests
REDIS_HOST = 'lepot_01'
REDIS_PORT = '32768'
FAAS_ENDPOINT = 'https://5aa176d5.ngrok.io'
MARKET_FILE_KEY_PAT = "market:%(market)s:import:files:%(market)s_%(ts_day)s.txt"
MARKET_METRIC_KEY_PAT = "metric:%(market)s:%(sym)s:%(metric)s"
FAAS_GET_MARKETS = {"function":"eod-market","command":"ls:markets"}

def parse_eod_line(line):
    split  =  line.split(',')
    d_line = {}
    if split and len(split) > 7:
        d_line["symbol"] = split[0]
        d_line["ts"] = split[2]
        d_line["open"] = float(split[3])
        d_line["high"] = float(split[4])
        d_line["low"] = float(split[5])
        d_line["close"] = float(split[6])
        d_line["vol"] = float(split[7])
        return d_line
    else:
        return None
def append_timeseries(market, tsday):
    f_lines = get_file_lines("market"=market, "ts_day"=tsday)
    metric_key = ""
    for line in f_lines:
        parts = parse_eod_line(line)
        print(parts)

def get_file_lines(**kwargs):
    if not market or not ts_date:
        return None
    redis_key = MARKET_FILE_KEY_PAT % (kwargs)
    print(redis_key)
    return True

def handle(req):
    if 'market' in req:
            
        get_file_lines(market=req["market"])

