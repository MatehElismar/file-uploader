import requests, json

cookies = ''
def login():
    r = requests.post('http://localhost/account/login', {"email": "evelyn.marte@cnd.com.do", "pass": "evelynmarte033"})
    print("login", r.status_code, r.json())
    global cookies
    cookies = r.cookies
def uploadVisits(pdv):  
    images = {}
    for imageName, values in pdv['imagenes'].items():
        images[imageName] = open(values['path'], 'rb')
        print(imageName)
    del pdv['imagenes']
    r = requests.post('http://localhost/points-of-sale/visits/', pdv, files=images, cookies=cookies)
    print(r.status_code, r.text)