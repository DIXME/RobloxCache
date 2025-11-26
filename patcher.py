import array
import os
import pickle
from enums import broad, SigText, FileSig
from get import get, folders

loco = os.getcwd()

#import yaml
#config = yaml.safe_load(open(os.path.join(loco,"config.yaml")))

cache_loco = "cache"
cache = os.path.join(loco,cache_loco)
list_of_folders_in_cache = os.listdir(cache)

cache_files = []

print(f"[+] Starting with cache:{cache_loco} #folders:{len(list_of_folders_in_cache)}")

def write(path, bytes):
    with open(path,'wb') as f:
        f.write(bytes)
        f.flush()
        f.close()

class cacheT:
    def __init__(self, folder, hash):
        self.folder = folder
        self.hash = hash
        self.type = getType(content[:80])
    
    def save(self):
        # bytes are being written but the value is not saving
        # whyyyyy
        data = exatract(self)
        path = os.path.join(folders,self.folder,self.hash)
        try:
            old = exatract(cacheT(self.folder,self.hash))
        except:
            print("[-] File removed from roblox cache!")
            return
        content = data[0] + data[1]
        if old != content:
            print(f"[+] Patching [{self.folder}] [{self.hash}] [{self.type.name}]")
            write(os.path.join(folders,self.folder,self.hash), content)

def view(file):
    filename = "temp."+str(SigText[file.type.name].value)
    path = os.path.join(os.getcwd(),filename)
    write(path, file.exa[1])
    os.startfile(path)

def dump(file):
    name = f'[{file.folder}]{file.hash}'
    filename = name+"."+str(SigText[file.type.name].value)
    path = os.path.join(os.getcwd(),"dumps",broad[file.type],filename)
    print(f"[+] Dumping File:{filename} @{path}")
    write(path, exatract(file)[1])

def dumpAll():
    global cache_files
    for file in cache_files:
        dump(file)

def parseDumpName(name):
    # parse the data out of the file & the name
    folder = name[name.find("[")+1:name.find("]")]
    hash = name[name.find("]")+1:name.find(".")]
    ext = name[name.find(".")+1:len(name)]
    return folder, hash, ext

def loadDumps():
    # take dumps files from folder
    # turn into roblox cache file
    # reload & save to disk
    folders_path = os.path.join(os.getcwd(),"dumps")
    folders = os.listdir(folders_path)
    changes = 0
    for folder in folders:
        files = os.listdir(os.path.join(folders_path,folder))
        for file in files:
            file_path = os.path.join(folders_path,folder,file)
            rblx_folder, hash, ext = parseDumpName(file)
            content = open(file_path,'rb').read()
            fileT = find(hash)
            try:
                data = exatract(fileT)
                if data[1] != content:
                    changes+=1
                    data[1] = content
                    print(f"[+] Updating file from dump folder:{rblx_folder} hash:{hash} ext:{ext}")
            except Exception as e:
                print("[-] File not found!",e)
                
    if changes >= 1:
        saveToDisk()
   

def patch():
    # take loaded files in cache_files
    # and write them to roblox cache folder
    # will it work?
    for file in cache_files:
        file.save()

def getType(data: bytes) -> SigText:
    for sig in SigText:
        if sig.name.encode('utf-8', 'ignore') in data:
            return sig
    
    return SigText.other

def exatract(file):
    # takes all of the file in bytes, and gets real file (remove roblox metadata)
    head = file.content[:80]
    sig = FileSig[file.type.value].value
    if sig == b'other':
        return [file.content, file.content]
    index = file.content.find(sig) # starts at
    if index == -1:
        return 'not found'
    roblox_stuff = file.content[:index]
    raw_filedata = file.content[index:]
    return [roblox_stuff, raw_filedata]

def load(folder_name, file_name):
    bytes = open(os.path.join(cache,folder_name,file_name), 'rb').read()
    head = bytes[:80]
    tail = bytes[len(bytes)-8:]
    type = broad[getType(head)]
    
    cache_files.append(cacheT(folder_name,file_name))
    file = cache_files[len(cache_files)-1]
    print(f"[+] Loading File [{file.folder}] [{file.hash}] [{file.type}]")

def loadFiles():
    global list_of_folders_in_cache, cache
    for folder_name in list_of_folders_in_cache:
        folder_path = os.path.join(cache, folder_name)
        for file_name in os.listdir(folder_path):
            load(folder_name, file_name)

def find(hash) -> cacheT | str:
    for file in cache_files:
        if file.hash == hash:
            return file
    return 'not found'

def saveToDisk():
    print("[+] Dumping cache files to disk")
    pickle.dump(cache_files,open("cache.pkl",'wb'))

def init():
    global cache_files
    if os.path.exists("cache.pkl"):
        # dose exist
        print("[+] Loading cache files from memmory")
        try:
            cache_files = pickle.load(open("cache.pkl", 'rb'))
        except:
            print("[-] Failed to load pkl file, remaking!")
            loadFiles()
            saveToDisk()
    else:
        loadFiles()
        saveToDisk()
        

if __name__ == "__main__":
    init()
    while True:
        os.system("cls")
        print(f"""\n
# of folders:{len(list_of_folders_in_cache)} @{cache} \n# of cache:{len(cache_files)}

1. dump all cache              4. exit
2. download cache from roblox  5. patch cache (from dump)
3. reload & save cache to disk 6. update from dumps (before patching)
        """)
        # simple CLI
        try:
            prompt = int(input("option > "))
        except:
            prompt = "a" # make it a str so it will go back to defualt

        match prompt:
            case 1:
                dumpAll()
            case 2:
                get()
            case 3:
                os.remove("cache.pkl")
                init()
            case 4:
                exit(0)
            case 5:
                patch()
            case 6:
                loadDumps()
            case _:
                print("[-] Invalid Input")
        os.system("pause")
    else:
        # called from other file
        init()
