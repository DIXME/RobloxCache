# retrive cahce files
# from normal roblox
import os

def get():
    # can change path here
    # has to use rbx-storage folder!
    copy = os.path.join(os.getcwd(),"cache")
    folders = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox","rbx-storage")
    print(f'[+] copyDir:{copy} foldersDir:{folders}')
    for folder in os.listdir(folders):
        path = os.path.join(copy,folder)
        print(f'[+] Copying path:{path} folder:{folder}')
        try:
            os.mkdir(path)
        except:
            #print('[!] Folder Already Exists')
            pass
        files = os.listdir(os.path.join(folders,folder))
        for file in files:
            open(os.path.join(path,file), "wb").write(open(os.path.join(folders,folder,file), 'rb').read())

if __name__ == "__main__":
    get()