import http.client, urllib.request, urllib.parse, urllib.error, base64
from os import listdir
from os.path import join
import os
import json

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '5149efd4a1ad42c68e93b89e5294e87d',
}

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'All',
})

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    FOLDER = "images/"
    # os.system(r"scrot tmp/%Y-%m-%d-%T-screenshot.png")
    for filename in listdir(FOLDER):
        print(filename, end=', ')

        full_path = join(FOLDER, filename)
        # print(full_path)
        img_bin = open(full_path, 'rb').read()
        print(len(img_bin))
        conn.request("POST", "/vision/v1/analyses?%s" % params, img_bin, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        data = json.loads(data.decode())
        print(data["color"])
    conn.close()
except Exception as e:
    print(e)    # print("[Errno {0}] {1}".format(e.errno, e.strerror))

