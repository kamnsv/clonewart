import os
os.chdir('/home/c/cu99893/clonewar')
import requests
import sys
import datetime

def load(url, user):

    dname = f'imgs/{user}'
    name = f"{datetime.datetime.now():%Y%m%d-%H%M%S}"
    fname = os.path.join(dname, f'{name}.jpg')
    
    if not os.path.exists(fname):
        if url is None: return 
        r = requests.get(url, stream=True)
        if r.status_code != 200: return
        with open(fname, 'wb') as f:
            for chunk in r:
                f.write(chunk)
                
    return fname       

if __name__=='__main__':
    
    
    x = 'Enter url and id user'
    
    if len(sys.argv) == 3:
        x = load(sys.argv[1], sys.argv[2])
   
    print(x)      