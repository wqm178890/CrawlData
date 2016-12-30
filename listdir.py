import os
import Image
import ExtractColor
import time
s = os.sep
_root = 'E:/HK'

def listdir(root):
    for i in os.listdir(root):
        if os.path.isfile(os.path.join(root,i)):
            if os.path.splitext(i)[1] == ".jpg":
                color = ExtractColor.get_dominant_color(root+"/"+i)
                print '#%02x%02x%02x' %(color)
                ExtractColor.get_color(color)
        else:
            listdir(root+"/"+i)
start = time.time()
listdir(_root)
print time.time() - start