import requests
import json

proxy=[]
r = requests.get('http://107.172.188.221:8000/?types=0&count=10&country=国内')
ip_ports = json.loads(r.text)
for i in range (0,10):
    str1 = "http://"+ip_ports[i][0]+r":"+str(ip_ports[i][1])
    #print(str)
    proxy.append(str1)
print(proxy)