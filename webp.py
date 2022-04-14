from PIL import Image
import sys

def webp(arr, fname):
  jpg = Image.fromarray(arr)
  jpg = jpg.resize((160,160), Image.ANTIALIAS)
  jpg.save(fname, format="webp")
  
if __name__=='__main__':
    
    if len(sys.argv) > 1:
        savewebp(sys.argv[1])
        