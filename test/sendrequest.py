#import gevent
#from gevent import monkey
#monkey.patch_all()
import grequests
import requests
import time
import datetime
start = time.time()
# for i in range(8):
#   r = requests.post("http://130.238.29.82:5100/predictions")
#   print(r.status_code)
#   print(r.text)
# r = requests.post("http://130.238.29.82:5100/predictions")
url = "http://130.238.29.82:5100/accuracy"
time1 = datetime.datetime.now()
print("current time:",time1)
req_list = [grequests.post(url) for i in range(1000)]
res_list = grequests.map(req_list)
end = time.time()

print(end - start)
