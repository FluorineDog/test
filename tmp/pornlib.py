import http.client, urllib.request, urllib.parse, urllib.error
import os
import json
import time.time()
import errno
import copy
import socket
#
#
# params = urllib.parse.urlencode({
#     # Request parameters
#     'visualFeatures': 'All',
# })

filename = ".screenshot.jpg"


class PornDetector:
    def __init__(self):
        self._conn = http.client.HTTPSConnection('api.microsoftmoderator.com/', timeout = 5)
        self._img_bin = None
        self._is_developer_mode = False
        self.headers = {"Ocp-Apim-Subscription-Key" : 'bc9c8e246b8843999f10ecba8f63856c'}
        self._cacheID = None
    def porn_detector(self, enable_picture = True, enable_text = True, is_developer_mode = True):
        is_porn = "OK"
        self._is_developer_mode = is_developer_mode

        if enable_picture:
            is_porn = self._porn_image()
        if enable_text:
            is_porn |= self.porn_text()
        if is_porn:
            return

    def update_photo(self):
        os.system("scrot " + filename)
        img_bin = open(filename, 'rb').read()
        headers = self.headers_gen({"Content-Type" : "image/jpeg"} )
        params = self.params_gen()
        self._conn.request("POST", "/Image/Cache/&%s" % params, img_bin, headers)
        data = self._conn.getresponse().read()
        print(data)
        self._cacheID = data["CacheId"]
    def remove_photo(self):
        headers = self.headers_gen()
        params = self.params_gen(CacheID=self._cacheID)
        self._conn.request("DELETE", "/Image/Cache/&%s" % params, img_bin, headers)

    def headers_gen(self, dic):
        headers = self.headers.copy()
        headers.update(dic)
        return headers

    def params_gen(self, **kwargs):
        params = dict(**kwargs)
        params = urllib.parse.urlencode(params)
        return params

    def porn_text(self):
        pass

    def porn_image(self)
        params =
        try:
            self._conn.request("POST", "/vision/v1/analyses?%s" % params, self._img_bin, headers)
        except socket.timeout  as e:
            print(e)
        except socket.gaierror as e:
            print(e)
            print(e)

            response = self._conn.getresponse()
            data = response.read()
            data = json.loads(data.decode())

            print(data)

            if data["adult"]["isAdultContent"]:
                return "PRON_DETECTED"

            print(data["color"])


    def __del__(self):
        self._conn.close()

def exe():
    init_time = time_time()
    pder = PornDetector()
    print(time.time() - init_time)
    print("ARE YOU OK?")
    while True
        pder.porn_detector(True, False)
        print(time.time() - init_time)

if __name__ == "__main__":
    exe()