import json
import os
import sys
import redis
import hashlib
import traceback
def hash_local(value):
        return hashlib.md5(value.encode('utf-8')).hexdigest()[:200]

def handle(req):
    """
    work_queue handler
    handle a request to the function
    Args:
        req (str): request body
    """
    result = {}
    #for k in os.environ:
    #    result[k] = os.environ[k]
    req_json = None
    if not req:
        result["help"]="Expected a command {ls|add|rm}"
        return result
    if "Http_Content_Type" in os.environ and "text/plain" in os.environ["Http_Content_Type"]:
        req_json = json.loads(req)
    else:
        req_json = json.loads(req)
    if not "command" in req:
       result["help"]="Expected a command {ls|add|rm}"
    else:
        try:
            if  "redis_host" in os.environ and "redis_port" in os.environ:
                rc = redis.Redis(host=os.getenv("redis_host"), port=os.getenv("redis_port"), decode_responses=True)
                if 'ls' in req_json["command"]:
                    if rc.exists("workqueue"):
                        queue={"message":"located workqueu on redis"}
                        if "by" in req_json:
                            by = req_json["by"]
                        else:
                            by="all"
                        if "value" in by:
                            queue = rc.hvals("workqueue")
                        elif "key" in by:
                            queue = rc.hkeys("workqueue")
                        elif "all" in by:
                            queue = rc.hgetall("workqueue")
                        else:
                            result["message"] = "by must be one of key|value|all"
                        
                        result["queue"] =queue
                    else:
                        result["message"] = "no workqueue found"
                elif 'add' in req_json["command"]:
                    if not "queue_item" in req_json:
                        result["message"] = "no queue_item found"
                    else:
                        queue_item = req_json["queue_item"]
                        if not "function" in queue_item:
                            result["message"] = "queue_item must have a function"
                        else:
                            hash_value = hash_local(json.dumps(queue_item))
                            result["message"] = "adding %s" % hash_value
                            s_state = rc.hset('workqueue',hash_value,json.dumps(queue_item))
                            if s_state == 0:
                                result["message"] = "updated workqueue:%s" % hash_value
                            if s_state == 1:
                                result["message"] = "added workqueue:%s" % hash_value

                #result["message"] ="add: not yet implemented"
                elif 'rm' in req_json["command"]:
                    result["message"] = "rm: not yet implemented"
                else:
                    result["message"] = "%s: is not a recognized command" % req_json["command"]
        
            else:
                result["message"] ="redis host or port not set"
            return json.dumps(result)
        except Exception as err:
            sys.stderr.write("Error message: %s" % str(err))
            result["message"] = str(err) 
            traceback.print.exe()
            return result

if __name__ == "__main__":
        lines = sys.stdin.readlines()
        request = " ".join(lines)
        sys.stdout.write(json.dumps(handle(request)))
