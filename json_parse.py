#coding:utf-8

import json

#f = open('response.json', 'r')

jsonData = {'labelAnnotations':[{'mid': '/m/0j_s4', 'score': 0.9744065, 'description': 'metropolitan area'}, {'mid': '/m/01fdzj', 'score': 0.9628799, 'description': 'tower'}, {'mid': '/m/05_5t0l', 'score': 0.9585877, 'description': 'landmark'}, {'mid': '/m/039jbq', 'score': 0.91049033, 'description': 'urban area'}, {'mid': '/m/01bqvp', 'score': 0.89956427, 'description': 'sky'}]}

#jsonの中身を確かめたいときは、このコメントを外せばよい
jd = json.dumps(jsonData, indent = 2)
print(jd)

#print(jsonData["labelAnnotations"][0:1])
result1 = jsonData["labelAnnotations"][0:1]
print(type(result1))
print(result1)
print(dict(result1))
print(result1['mid'])

f.close()
