import fs, httpClient
import json

def log():
   with open('./logs.json', 'w') as f: 
      json.dump(response['logs'], f, indent=4, separators=(", ", " : "))
   with open('./uploaded.json', 'w') as f: 
      json.dump(response['uploadedVisits'], f, indent=4, separators=(", ", " : "))



totalUploaded = 0
totalSubidas = 0

response = {}
response['logs'] = []
response['uploadedVisits'] = []
uploaded = []
with open('./last-uploaded.json', 'r') as f: 
   uploaded = json.load(f)
# FS TEST
def Visits():
   pdvs = fs.dirToJSON({}, 'C:\\Users\\DELL\\Google Drive\\MISTERY DATA\\administracion\\datos\\visitas') 

   for nombre, visitas in pdvs.items():
      index = nombre.index('+')
      print('pdv actual ->', nombre)
      codigoPOS = nombre[:index].strip() 
      for fecha, imagenes in visitas.items():   
         if not hasbeenUploaded(codigoPOS, fecha+':00:00'): 
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

def hasbeenUploaded(codigoPOS, fecha):
   global totalUploaded
   global totalSubidas
   if {'codigoPOS': codigoPOS, 'fecha': fecha} in uploaded:
      print('already uploaded', codigoPOS, '->', fecha)
      totalUploaded += 1
      return True
   else:
      print('processing', codigoPOS, '->', fecha)
      totalSubidas +=1

# action
httpClient.login(response)
Visits()
print("totalUploaded " + str(totalUploaded))
print("totalSubidas " + str(totalSubidas))