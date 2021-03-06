import requests, json
from consts import URL

cookies = ''
def login(response):
    r = requests.post(URL+'/account/login', {"email": "matematicoelismar@gmail.com", "pass": "1234"})
    resp = r.json()
    print("login", r.status_code, resp)
    response['logs'].append({'method': 'login', 'status': r.status_code, 'data': resp})
    global cookies
    cookies = r.cookies

def uploadVisits(response, pdv):
    images = {}
    for imageName, values in pdv['imagenes'].items():  
        if values["ext"] == '.ini':
            continue
        images[imageName] = open(values['path'], 'rb')


    del pdv['imagenes'] 
    r = requests.post(URL+'/points-of-sale/visits/', pdv, files=images, cookies=cookies)
    if r.status_code != 200:
        status = 'false'
        response['logs'].append({'method': 'add-visit',  'status': status, 'data': r.text, 'pdv': pdv})
        response['errors'].append({'method': 'add-visit',  'status': status, 'data': r.text, 'pdv': pdv})
    else:
        status = r.status_code
        response['logs'].append({'method': 'add-visit', 'status': status, 'data': r.json(), 'pdv': pdv})
        data = r.json()
        if data['ok']:
            response['uploadedVisits'].append(pdv)
        else:
            response['errors'].append({'method': 'add-visit',  'status': status, 'data': r.text, 'pdv': pdv})
    print("add-visit", r.status_code, r.text)

def uploadColmados(response, colmado):
    files = []
 
    for imageName, values in colmado['imagenes'].items():  
        if values["ext"] == '.ini':
            continue
        files.append(('images',  open(values['path'], 'rb')))

    del colmado["imagenes"] 
    r = requests.put(URL+'/api/colmados/'+ colmado['codigo'], {}, files=files, cookies=cookies)
    if r.status_code != 200:
        status = 'false'
        response['logs'].append({'method': 'add-colmado-images',  'status': status, 'data': r.text, 'colmado': colmado})
        response['errors'].append({'method': 'add-colmado-images',  'status': status, 'data': r.text, 'colmado': colmado})
    else:
        status = r.status_code
        response['logs'].append({'method': 'add-colmado-images', 'status': status, 'data': r.json(), 'colmado': colmado})
        data = r.json()
        if data['ok']:
            response['uploadedVisits'].append(colmado)
        else:
            response['errors'].append({'method': 'add-colmado-images',  'status': status, 'data': r.text, 'colmado': colmado})
    print("add-colmado-images", r.status_code, r.text)


def addPOSImage(response, pdv):
    image = open(pdv['imageInfo']['path'], 'rb')
    r = requests.put(URL+'/points-of-sale/'+pdv['codigoPOS'], data={}, files={'image': image}, cookies=cookies)
    if r.status_code != 200:
        status = 'error'
        response['logs'].append({'method': 'addPOSImage',  'status': status, 'data': r.text, 'pdv': pdv})
    else:
        status = r.status_code
        response['logs'].append({'method': 'addPOSImage', 'status': status, 'data': r.json()})
    print("Add-POS-Image", r.status_code, r.text)
