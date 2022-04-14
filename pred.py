import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.chdir('/home/c/cu99893/clonewar')
import matplotlib.image as image
import sys
import numpy as np
from PIL import Image
import hashlib

def extend_img(i, h=320, w=320):
    k = i.size[0]/i.size[1] # разница высоты и ширины
    bg = Image.new('RGB', (i.size[k<1], i.size[k<1]), (0, 0, 0))
    img_w, img_h = i.size
    bg_w, bg_h = bg.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    bg.paste(i, offset)
    i = bg.resize((w, h))
    return np.array(i)
   
def crop_img(i, h=320, w=320):
    k = i.size[0]/i.size[1] # разница высоты и ширины
    i = i.resize((int(w*k) if k > 1 else w, int(h/k) if k < 1 else h))
    x1, y1 = (w + (i.size[0]-w)//2, 0) if k > 1 else (0, h+(i.size[1]-h)//2)
    x2, y2 = ((i.size[0]-w)//2, h) if k > 1 else (w, (i.size[1]-h)//2)
    i = i.crop(([x1,x2][k>1], [y1,y2][k<=1], [x1,x2][k<=1], [y1,y2][k>1]))
    return np.array(i)   

def get_hash_file(fname):

    hash_md5 = hashlib.md5() # вычисление md5
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash_md5.block_size), b""):
            hash_md5.update(chunk)
                
    return hash_md5.hexdigest().upper()
        
def predict(fname):
    
    name, ext = os.path.splitext(fname)
    
    if not os.path.isfile(f'{name}.npy'):
       arr = Image.open(fname)
       arr = arr.convert('RGB')
       k = arr.size[0]/arr.size[1] 
       if k <= 0.9 or k >= 1.1:
           x = crop_img(arr)
       else:
           x = extend_img(arr)
       x = x/255.
       np.save(name, x)
    else:
       x = np.load(f'{name}.npy')
    
    print(x.shape)
    
    path = f'{name}.webp'    
    webp((x * 255).astype(np.uint8), f'{name}.webp') 
    
    process = os.popen(f'./keras2cpp my.model {name}.npy')
    line = process.read()
    process.close()
              
    return line[1:-3].split(','), path, get_hash_file(fname) 


def webp(arr, fname):
  if os.path.isfile(fname): return
  jpg = Image.fromarray(arr)
  jpg = jpg.resize((160,160), Image.ANTIALIAS)
  jpg.save(fname, format="webp")

        
if __name__=='__main__':
    
    
    x = 'Enter path for image'
    
    if len(sys.argv) == 2:
        x = predict(sys.argv[1])
        
    if x is None:
        print('File error')
    
    else:    
        print(x)      