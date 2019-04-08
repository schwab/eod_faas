import http.client

conn = http.client.HTTPConnection("http://lepot_01:8080")

payload = "{\"command\":\"ls:market:dates\"}"

headers = {
    'cache-control': "no-cache",
    'Postman-Token': "7ebe4501-0c36-4786-96ce-ba82ce0ea544"
    }

conn.request("POST", "function,eod-market", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))