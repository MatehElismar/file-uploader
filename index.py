import fs, httpClient
import json
httpClient.login()
# FS TEST
pdvs = fs.dirToJSON({}, '.\\visitas')  
for nombre, visitas in pdvs.items():
    index = nombre.index('+')
    codigoPOS = nombre[:index].strip() 
    for fecha, imagenes in visitas.items(): 
        httpClient.uploadVisits({
            'codigoPOS': codigoPOS,
            'imagenes': imagenes,
            'fecha': fecha
            })
    

# HTTPCLIENT TEST
