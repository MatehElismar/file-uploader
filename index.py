import fs, httpClient
import json

def log():
   with open('./logs.json', 'w') as f: 
      json.dump(response, f, indent=4, separators=(", ", " : "))


response = []

# FS TEST
def Visits():
   pdvs = fs.dirToJSON({}, 'C:\\Users\\DELL\\Google Drive\\MISTERY DATA\\administracion\\datos\\visitas')  
   for nombre, visitas in pdvs.items():
      print('pdv actual ->', nombre)
      index = nombre.index('+')
      codigoPOS = nombre[:index].strip() 
      for fecha, imagenes in visitas.items(): 
         httpClient.uploadVisits(response, {
               'codigoPOS': codigoPOS,
               'imagenes': imagenes,
               'fecha': fecha+':00:00'#para que no tengan un dia menos
               })
      log()
    
def POSImages():
   images = fs.dirToJSON({}, 'C:\\Users\\DELL\\Google Drive\\MISTERY DATA\\administracion\\datos\\pos_images\\faltantes')  
   for pdvName, imageInfo in images.items():
      print('image actual ->', pdvName)
      index = pdvName.index('+')
      codigoPOS = pdvName[:index].strip() 
      httpClient.addPOSImage(response, {
            'codigoPOS': codigoPOS,
            'imageInfo': imageInfo
            })
      log()


# httpClient.login(response) 

# HTTPCLIENT TEST
