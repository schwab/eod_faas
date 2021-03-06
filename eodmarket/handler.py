import redis
import json
import os
from dateutil.parser import *
MARKET_FILES_KEY="market:files:%s"
MARKET_DATES_KEY="market:dates:%s"
MARKET_NAMES_KEY="market:names"
COMMANDS = ["ls:markets","ls:market:dates","add:market"]
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    result = {}
    req_json = json.loads(req)    
    if not "command" in req_json or not any( req_json['command'].startswith(x) for x in COMMANDS ):
       result["help"]="Expected a command %s" % COMMANDS
       
       return result
    else:
        try:
            if  "redis_host" in os.environ and "redis_port" in os.environ:
                rc = redis.Redis(host=os.getenv("redis_host"), port=os.getenv("redis_port"), decode_responses=True)
                if 'add:market' in req_json["command"]:
                    splits=req_json["command"].split(":")
                    if splits and len(splits) == 3:
                        market = splits[2]
                        return rc.sadd(MARKET_NAMES_KEY, market)
                if 'ls:markets' in req_json["command"]:
                    return rc.smembers(MARKET_NAMES_KEY)
                if 'ls:market:files' in req_json["command"]:
                    parts = req_json["command"].split(":")
                    if len(parts) == 4:
                        market_name = parts[3]
                        return result
                    else:
                        return {"error":"ls:market:files:... expected a valid market name"}

                if 'ls:market:dates:' in req_json["command"]:
                    group_by=None
                    return_values = "all"

                    fx_year = lambda s: parse(s).year
                    def append_year(d, s, r):
                        y = fx_year(s)
                        if not y in d:
                            if 'counts' in r:
                                d[y] = 1
                            else:
                                d[y] = [s]
                        else:
                            if 'counts' in r:
                                d[y] += 1
                            else:
                                d[y].append(s)
                        return d
                    if "group_by" in req_json and req_json["group_by"] in ["year","month"]:
                        group_by = req_json["group_by"]
                    if 'return' in req_json and req_json['return'] in ['counts','all']:
                        return_values = req_json['return']
                    markets=rc.smembers(MARKET_NAMES_KEY)

                    parts = req_json["command"].split(":")
                    #print(parts)
                    if len(parts) == 4 and parts[3] in markets:
                        #print(parts)
                        all_dates = rc.hkeys("market:dates:%s" % parts[3])
                        if not group_by:
                            return {"market_dates":all_dates}
                        elif "year" in group_by:
                            result = {}
                            for s in all_dates:
                                append_year(result, s, return_values)
                            return result
                    else:
                        return {"error":"ls:market:dates:... expected a valid market name"}

        except Exception as err:
            result={"error":err}
            return result
