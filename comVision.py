import http.client, urllib.request, urllib.parse, urllib.error, base64
from os import listdir
from os.path import join
import os
import json
import time
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '5149efd4a1ad42c68e93b89e5294e87d',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'All',
})

filename = ".screenshot.jpg"


class PornDetector:
    def __init__(self):
        self.conn = http.client.HTTPSConnection('api.projectoxford.ai')
    def run(self):
        try:
            os.system(r"scrot " + filename)
            img_bin = open(filename, 'rb').read()
            self.conn.request("POST", "/vision/v1/analyses?%s" % params, img_bin, headers)
            response = self.conn.getresponse()
            data = response.read()
            print(data)
            data = json.loads(data.decode())
            print(data["color"])
        except:
            pass
    def __del__(self):
        self.conn.close()