import certifi
import os
def bundleCerts(path=None):
    if(not path):
        path = os.getenv("CERT_BUNDLER_PATH")
        if(not path):
            print("CERT_BUNDLER_PATH not set")
            return
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.crt'):
                    bundleCerts(os.path.join(root, file))
        return
    
    myPem = certifi.where()
    
    with open(myPem, 'r') as myPemFile:
        myPemContents = myPemFile.read()
    
    with open(path, 'r') as pathFile:
        pathContents = pathFile.read()
    
    if pathContents in myPemContents:
        print(f"${path} already present in ${myPem}")
    else:
        print(f"Appending ${path} to ${myPem}")
        with open(myPem + ".bak", 'w') as backupFile:
            backupFile.write(myPemContents)
        
        with open(myPem, 'a') as myPemFile:
            myPemFile.write(f"\n\n#Label: {path}\n")
            myPemFile.write(pathContents)

bundleCerts()