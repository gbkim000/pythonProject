import requests
from bs4 import BeautifulSoup
respo=requests.get('http://203.247.66.82/weather/observation/currentweather.jsp?auto_man=m&stn=0&type=t99&reg=109&tm=2021.10.07.14%3A00&x=19&y=6')
soup=BeautifulSoup(respo.content, 'html.parser')
table=soup.find('table', {'class': 'table_develop3'})
data=[]
for tr in table.find_all('tr'):
    #print(tr)
    tds=list(tr.find_all('td'))
    for td in tds:
        if td.find('a'):
            point=td.find('a').text
            temperature=tds[5].text
            humidity=tds[9].text
            data.append([point, temperature, humidity])
print(data)
