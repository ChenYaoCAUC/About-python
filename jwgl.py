import requests
import time
import threading
from urllib.parse import unquote

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Accept-Encoding': 'gzip, deflate',
#     'Referer': 'http://jwgl.cauc.edu.cn/(qnyvk2m4154m503awoqvtcef)/xsxjs.aspx?xkkh=24184D21F1391C58091ADBED1AA819BA07E2620EBE8671BEE279C1E02C5CD437BBF4B29A177193E1&xh=170341303',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Connection': 'keep-alive',
#     'Cookie': 'UM_distinctid=1664e74847326a-08c97468e779b2-4c312878-e1000-1664e748474311'
# }
#
# data = {
#     '__EVENTTARGET': 'Button1',
#     '__EVENTARGUMENT': '',
#     '__VIEWSTATE': 'dDwxMzg2MzMxOTMyO3Q8cDxsPHp5ZG07eHk7ZHFzemo7UkxYWjt6eW1jO3h6Yjt4bTtzZmJqa2M7Y3hibW1zMTtjeGJtbXMyO2h4d3o7PjtsPDAzNDE76K6h566X5py656eR5a2m5LiO5oqA5pyv5a2m6ZmiOzIwMTc7MTvorqHnrpfmnLrnp5HlrabkuI7mioDmnK87MTcwMzQxQzvpmYjnkbY75ZCmO+WFjeS/rjvph43kv647aTwyPjs+PjtsPGk8MD47PjtsPHQ8O2w8aTwxPjtpPDI+Oz47bDx0PHQ8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs+OztsPGk8MD47Pj47Oz47dDx0PDs7bDxpPDE+Oz4+Ozs+Oz4+Oz4+Oz46Qtyx6I9haf1hAjewIRJKCIQR5g==',
#     'xkkh': '%282018-2019-2%29-90010102-07332-1'
# }


file = open('r.txt', 'r')
firstline = file.readline()
path = firstline[5:-9]
secondline = file.readline()
host = secondline[6:].replace('\r\n', '').replace('\n', '')
url = 'http://'+host+path
headers = {}
while True:
    line = file.readline()
    if line.find(':') == -1:
        break
    header_name = line[:line.find(':')]
    if header_name == 'Content-Length':
        continue
    header_content = line[line.find(':')+2:].replace('\r\n', '').replace('\n', '')
    headers[header_name] = header_content

data = {}
datavalue = file.readline()
parameters = datavalue.split('&')
for parameter in parameters:
    array = parameter.split('=')
    if len(array) == 1:
        data[array[0]] = ''
        continue
    if array[0] == '__VIEWSTATE':
        data[array[0]] = unquote(array[1])
        continue
    data[array[0]] = array[1]

while True:
    time.sleep(0.5)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print('HTTP返回码为：' + str(response.status_code))
        response_text = response.content.decode('gb2312')
        if response_text.find('现在不是选课时间') != -1:
            print('现在不是选课时间')
        elif response_text.find('保存成功') != -1:
            print('选上了~~')
            break
        elif response_text.find('人数超过限制！') != -1:
            print('课程容量不足')
        else:
            print('出错了')

    else:
        print('HTTP返回码为：' + str(response.status_code))
        print(response.content.decode('gb2312'))

