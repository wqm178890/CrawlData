TypeList = ['buildings',
            'animals',
            'backgrounds',
            'fashion',
            'transportation',
            'industry',
            'people',
            'health',
            'business',
            'places',
            'religion',
            'education',
            'travel',
            'science',
            'nature',
            'feelings',
            'computer',
            'sports',
            'music',
            'food'
            ]
print len(set(TypeList))

device_dic = {'64': [1920, 1080], #6sp
              '32': [1334, 750],  #6s
              '16': [1136, 640],  #5s
              '5': [960, 640],    #4
              '4': [320, 480],
              '8': [2048, 2048],
              '2': [1024, 1024]}

print device_dic[64][0]
