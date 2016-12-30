# -*- coding: utf-8 -*-
import colorsys
from PIL import Image 
import Queue
import os
import math

rgbList = {"red": [(255, 0, 0),(220,20,60),(219,112,147),(199,21,133),(205,92,92),(178,34,34),(139,0,0),(128,0,0)],
           "orange": [(255, 128, 0),(255,165,0),(255,140,0),(255,69,0),(255,99,71)],
           "yellow": [(255, 255, 0),(250,250,210),(255,255,224),(255,250,205),(238,232,170),(240,230,140),(255,215,0),(255,248,220),(218,165,32),(245,222,179),(255,228,181),(255,222,173),(210,180,140),(222,184,135),(255,228,196)],
           "green": [(0, 255, 0),(127,255,170),(0,250,154),(0,255,127),(60,179,113),(46,139,87),(144,238,144),(152,251,152),(143,188,143),(50,205,50),(34,139,34),(0,128,0),(0,100,0),(127,255,0),(124,252,0),(85,107,47),(107,142,35),(173,255,47),(128,128,0),(189,183,107)],
           "teal": [(0, 128, 128),(225,255,255),(175,238,238),(0,255,255),(0,206,209),(47,79,79),(0,139,139),(0,128,128),(72,209,204),(32,178,170),(64,224,208)],
           "blue": [(0, 0, 255),(123,104,238),(0,0,205),(106,90,205),(72,61,139),(25,25,112),(0,0,139),(0,0,128),(65,105,225),(100,149,237),(240,248,255),(70,130,180),(135,206,250),(135,206,235),(0,191,255),(173,216,230),(176,224,230),(95,158,160),(30,144,255)],
           "purple": [(128,0,128),(218,112,214),(221,160,221),(238,130,238),(139,0,139),(186,85,211),(148,0,211),(153,50,204),(75,0,130),(138,43,226),(147,112,219)],
           "pink": [(255, 0, 255),(255,182,193),(255,192,203),(255,105,180),(255,20,147)],
           "white": [(255, 255, 255), (248,248,255),(240,255,255),(240,255,240),(255,255,240),(255,250,240),(253,245,230),(250,235,215),(250,240,230),(255,245,238),(255,228,225),(255,250,250),(245,245,245)],
           "gray": [(128, 128, 128),(216,191,216),(119,136,153),(112,128,144),(220,220,220),(211,211,211),(192,192,192),(169,169,169),(128,128,128),(105,105,105)],
           "brown": [(173, 90, 90),(205,133,63),(139,69,19),(160,82,45),(244,164,96),(210,105,30),(160,82,45),(255,160,122),(255,127,80),(233,150,122),(188,143,143),(165,42,42)],
           "black": [(0,0,0)]
           }

def get_color((r1,g1,b1)):
    dicts = {}
    for (k, v) in rgbList.items():
        dicts[k] = 255
        for (r,g,b) in v:
            u = calc_colors((r1,g1,b1), (r,g,b))
            if dicts[k] > u:
                dicts[k] = u
    # values = dicts.values()
    # values.sort()
    # test = sorted(dicts.iteritems(), key = lambda d:d[1], reverse=False)
    return sort_dict(dicts)

def sort_dict(dict):
    items = dict.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    return str(backitems[0][1])
    #return [backitems[i][1] for i in range(0,len(backitems))]

def calc_colors((r1,g1,b1), (r2, g2, b2)):
    r = abs(r1 - r2)
    g = abs(g1 - g2)
    b = abs(b1 - b2)
    return math.sqrt(math.pow(r,2) + math.pow(g,2) + math.pow(b,2))
    
 
def get_dominant_color(path):
    print path
    image = Image.open(path)
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    info = os.path.split(path)
    
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200,200))
   # image.save("%s/img_%s" % (info[0], info[-1]))
    total_color = image.size[0] * image.size[1]
    print total_color
    max_score = None
    dominant_color = None
    queues = Queue.PriorityQueue(123)
    queues.put(12)
    black = 0
    white = 0
    j = 0
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):

        j += 1
        # 跳过纯黑色
        if ((r <= 64) & (g <= 64) & (b <= 64)):
            black += count
            continue
        
        if ((r >= 180) & (g >= 180) & (b >= 180)):
            white += count
                
        if a == 0:
            black += 1
            continue
        
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
       
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
       
        y = (y - 16.0) / (235 - 16)
        
        # 忽略高亮色
        if y > 0.9:
            continue
        
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
            
    print "black-", black
    print "white-", white
    if black / total_color > 0.48:
        return (0,0,0)
    if white / total_color > 0.4:
        return (255,255,255)

    return dominant_color

def hex2rgb(hexcolor):
    rgb = ((hexcolor >> 16) & 0xff,
        (hexcolor >> 8) & 0xff,
        hexcolor & 0xff
       )
    return rgb

#print hex2rgb(0xFFFFFF)
#该代码片段来自于: http://www.sharejs.com/codes/python/8655

#image = Image.open('E:/HK/20151225_203037.jpg')
#img_path = "E:/HK_IMG/img_20151225_161534.jpg"
#img_path = "d:/blackTest1.jpg"
#print '#%02x%02x%02x' %(get_dominant_color(img_path))
t = get_color((255,200,200))
print str(t)