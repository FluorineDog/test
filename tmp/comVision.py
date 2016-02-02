import http.client, urllib.request, urllib.parse, urllib.error
import os
import json
import errno
import socket
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
        self._conn = http.client.HTTPSConnection('api.projectoxford.ai', timeout = 5)
        self._img_bin = None
        self._is_developer_mode = False
    def porn_detector(self, enable_picture = True, enable_text = True, is_developer_mode = True):
        os.system("scrot " + filename)
        self._img_bin = open(filename, 'rb').read()
        self._is_developer_mode = is_developer_mode
        is_porn = "OK"
        if enable_picture:
            is_porn = self._porn_image()
        if enable_text:
            is_porn |= self._porn_text()
        if is_porn:
            return

    def _porn_text(self):
        pass

    def _porn_image(self):
        try:
            print(params)
            print(headers)
            print(len(self._img_bin))
            self._conn.request("POST", "/vision/v1/analyses?%s" % params, self._img_bin, headers)
        except socket.timeout  as e:
            print(e)
        except socket.gaierror as e:
            print(e)
            print(e)

        response = self._conn.getresponse()
        data = response.read()
        print(data.decode())
        data = json.loads(data.decode())

        print(data)

        if data["adult"]["isAdultContent"]:
            return "PRON_DETECTED"

        print(data["color"])


    def __del__(self):
        self._conn.close()

def exe():
    pder = PornDetector()
    print("ARE YOU OK?")
    pder.porn_detector(True, False)

if __name__ == "__main__":
    exe()
'''
    b'{
    "categories":[{"name":"abstract_","score":0.078125},{"name":"others_","score":0.03515625},{"name":"outdoor_","score":0.00390625}]
    ,"adult":{"isAdultContent":false,"isRacyContent":false,"adultScore":0.016986165195703506,"racyScore":0.014871135354042053},
    "requestId":"049d82a0-3297-49e8-9337-460c43ddcb2a",
    "metadata":{"width":1920,"height":1080,"format":"Jpeg"},
    "faces":[],
    "color":{"dominantColorForeground":"Black",
            "dominantColorBackground":"Black",
            "dominantColors":["Black","White"],
            "accentColor":"2C7B9F","isBWImg":false},
    "imageType":{"clipArtType":0,"lineDrawingType":0}}'
'''