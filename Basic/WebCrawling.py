# # %% test
# print('홍길동')
# print('저팔계')
#
# # %% test
# print('홍길동2')
# print('저팔계2')


# data1 = 10
# data2 = "%d" % 100  # data2는 문자열 타입임.
# print(data1, data2)
# print(type(data2))
#
# # %% format test2
# # "문자열값".format()
# data1 = 10
# data2 = 10.4231
# data3 = 'A'
# data4 = "ABC"
# print("data : {}".format(data1))
# print("data1 : {}\ndata2 : {}".format(data1, data2))
# print("data3 : %s" % data3)
# print("data3 : %c" % data3)
# print("data : %c" % 65)
# print("data4 : %s" % data4)
# print("data4 : {}".format(data4))

# %% 웹 크롤링하기
import requests
from bs4 import BeautifulSoup

respo = requests.get(
    'http://203.247.66.82/weather/observation/currentweather.jsp?auto_man=m&stn=0&type=t99&reg=109&tm=2021.10.07.14%3A00&x=19&y=6')
soup = BeautifulSoup(respo.content, 'html.parser')
table = soup.find('table', {'class': 'table_develop3'})
data = []
for tr in table.find_all('tr'):
    # print(tr)
    tds = list(tr.find_all('td'))
    for td in tds:
        if td.find('a'):
            point = td.find('a').text
            temperature = tds[5].text
            humidity = tds[9].text
            data.append([point, temperature, humidity])
print(data)
