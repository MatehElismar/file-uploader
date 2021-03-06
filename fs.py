import os
import sys
count = 0
tabs = ''


json = {'name': 'dirObject'}

def dirToJSON(json,  path):
    look(json, path)
    for prop in list(json):
        parentPath = os.path.join(path, prop)
        isDir = look(json[prop], parentPath)
        if(isDir):
            dirToJSON(json[prop], parentPath)
    return json

def dir(path, x):
    global tabs
    inside = lookInto(path)
    if x:
        tabs +='|   '
    for file in inside:
        print(tabs + file['name'])
        parentPath = os.path.join(path, file['name'])
        file_inside = lookInto(parentPath)
        if(file_inside):
            dir(parentPath, True)
    if x:
        tabs = tabs.replace('|   ', '', 1)

def scanDir(path):
    files = []
    with os.scandir(path) as entries:
        for entry in entries:
            files.append({'name': entry.name, 'stat': entry.stat()})
            if os.path.isdir(os.path.join(path, entry.name)):
                with os.scandir(os.path.join(path, entry.name)) as entry_files:

                    for another_entry in entry_files:
                        files.append({'name': another_entry.name, 'stat': another_entry.stat()})
    return files

def lookInto(path):
    inside = []
    if os.path.isdir(path):
        with os.scandir(path) as dirInside:
           for file in dirInside:
              inside.append({'name': file.name, 'stat': file.stat()})
        return inside

def look(obj, path):
    # Verifica que la ruta pasada es un directorio y si lo es, agrega su interior en el campo de la ruta
    if os.path.isdir(path):
        with os.scandir(path) as dirInside:
           for file in dirInside:
                #The property name will be the fileName witout the extention 
               propName = file.name

               if os.path.isfile(os.path.join(path, file.name)):
                    indexEXT = file.name.rindex('.')
                    propName = file.name[:indexEXT] 
                    
                    slash = ''
                    if sys.platform in ['Windows', 'win32', 'cygwin']: slash = '\\' 
                    elif sys.platform in ['linux', 'linux2']: slash = '/'

                    obj[propName] = {}
                    obj[propName]['path'] = path + slash + file.name
                    obj[propName]['ext'] = file.name[indexEXT:]
                    obj[propName]['originalName'] = file.name
               else:
                    obj[propName] = {}
       
        return obj
