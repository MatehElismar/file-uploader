import os
count = 0
tabs = ''

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
            