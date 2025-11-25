import array
import os
import pickle
from enums import broad, SigText, FileSig

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
    def __init__(self, folder, hash, content):
        self.folder = folder
        self.hash = hash
        self.content = content
        self.type = getType(content[:80])
    
    def save(self):
        global cache
        write(os.path.join(cache, self.folder,self.hash),self.content)

def view(file):
    data = exatract(file)[1]
    filename = "temp."+str(SigText[file.type.name].value)
    path = os.path.join(os.getcwd(),filename)
    write(path, data)
    os.startfile(path)

def dump(file):
    data = exatract(file)[1]
    name = f'[{file.folder}]{file.hash}'
    filename = name+"."+str(SigText[file.type.name].value)
    path = os.path.join(os.getcwd(),broad[file.type.name],filename)
    write(path, data)

def dumpAll():
    global cache_files
    for file in cache_files:
        dump(file)

def getType(data: bytes):
    for sig in SigText:
        if sig.name.encode('utf-8', 'ignore') in data:
            return sig
    
    return SigText.Other

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
    
    cache_files.append(cacheT(folder_name,file_name,bytes))
    print(f"[+] File:{file_name} folder:{folder_name} type:{type[0]} sig:{type}")

def init():
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

if os.path.exists("cache.pkl"):
    # dose exist
    print("[+] Loading cache files from memmory")
    cache_files = pickle.load(open("cache.pkl", 'rb'))
else:
    init()
    print("[+] Dumping cache files to disk")
    pickle.dump(cache_files,open("cache.pkl",'wb'))

if __name__ == "__main__":
    while True:
        os.system("cls")
        print("""\n
1. dump all  4. exit
2. re-fetch  5. patch
3. re-load
        """)
        prompt = input("option > ")
        match prompt:
            case "1":
                print('fuckyou')
            case "4":
                exit(0)
        os.system("pause")
