import fs, httpClient
import json
import os
import sys
from consts import PDVS_PATH, COLMADOS_PATH

def clear():
   if sys.platform in ['Windows', 'win32', 'cygwin']: os.system('cls') 
   elif sys.platform in ['linux', 'linux2']: os.system('clear')

def log():
   with open('./logs.json', 'w') as f: 
      json.dump(response['logs'], f, indent=4, separators=(", ", " : "))
   with open('./error.json', 'w') as f: 
      json.dump(response['errors'], f, indent=4, separators=(", ", " : "))
   with open('./uploaded.json', 'w') as f: 
      json.dump(response['uploadedVisits'], f, indent=4, separators=(", ", " : "))



totalUploaded = 0
totalSubidas = 0

response = {}
response['logs'] = []
response['errors'] = []
response['uploadedVisits'] = []
uploaded = []
with open('./uploaded.json', 'r') as f: 
   response['uploadedVisits'] = json.load(f)

# FS TEST
def Visits():
   pdvs = fs.dirToJSON({}, PDVS_PATH)  
   for nombre, visitas in pdvs.items():
      index = nombre.find('+')
      if index < 0 : continue
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
     
def Colmados():
   colmados = fs.dirToJSON({}, COLMADOS_PATH)  

   for nombre, imagenes in colmados.items():
      index = nombre.find('+')
      if index < 0 : continue
      print('colmado actual ->', nombre)
      codigo = nombre[:index].strip()   

      # if not hasbeenUploaded(codigo, fecha+':00:00'): 
      httpClient.uploadColmados(response, {
            'codigo': codigo,
            'imagenes': imagenes,
            })
      log()
    

def POSImages():
   images = fs.dirToJSON({}, 'C:\\Users\\DELL\\Google Drive\\MISTERY DATA\\administracion\\datos\\pos_images\\faltantes')  
   for pdvName, imageInfo in images.items():
      print('image actual ->', pdvName)
      index = pdvName.find('+')
      if index < 0 : continue
      codigoPOS = pdvName[:index].strip() 
      httpClient.addPOSImage(response, {
            'codigoPOS': codigoPOS,
            'imageInfo': imageInfo
            })
      log()

def hasbeenUploaded(codigoPOS, fecha):
   global totalUploaded
   global totalSubidas
   global response
   if {'codigoPOS': codigoPOS, 'fecha': fecha} in response['uploadedVisits']:
      print('already uploaded', codigoPOS, '->', fecha)
      totalUploaded += 1
      return True
   else:
      print('processing', codigoPOS, '->', fecha)
      totalSubidas +=1



def exec():
   # action
   httpClient.login(response)
   Visits()
   rint("totalUploaded " + str(totalUploaded))
   print("Total De Intentos De Subir: " + str(totalSubidas))
   # POSImages()

def main():
   global totalUploaded
   global totalSubidas
   print('*** Welcome to Mateh Uploader ***\n')
   while(True):
      print("Collections:")
      print("1- PDVs")
      print("2- COLMADOS")
      print("3- Imagenes de PDVs\n")
      x = input('Choose a collection: ')
      if x == '1': 
         httpClient.login(response)
         Visits()
      elif x == '2': 
         httpClient.login(response)
         Colmados()
      elif x == '3': 
         httpClient.login(response)
         POSImages()
      else:
             print('xxx Unvalid Option xxx') 
      
      print("\ntotalUploaded " + str(totalUploaded))
      print("Total De Intentos De Subir: " + str(totalSubidas))
      input('press any key to start again.')
      clear()

      totalUploaded = 0
      totalSubidas = 0

main()
