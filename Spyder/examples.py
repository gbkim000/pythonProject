# # -*- coding: utf-8 -*-
# # %% set()함수 사용예제
# numSet = set()
# num=0
# while len(numSet)<5:
#     num=int(input("0~9사이의 정수 : "))
#     numSet.add(num)
#
# print("모두 입력되었습니다.")
# print("입력된 값은 {}입니다.".format(numSet))
#
# # %% min()함수 사용 예제
# # 100점 미만의 점수에 +5점 증가하기.
# exam = [99,78,100,91,81,85,54,100,71,50]
# score = [min(n+5, 100) for n in exam]
#
# print(exam)
# print(score)
#
# # %%
# std = '"김철수", 86'
# name = std.split(",")[0].strip('"')
# #문자열.strip('charset') // charset을 생략하면 '공백문자','\n','\t'를 제거함
# score = std.split(",")[1]
# print("이름: {}, 점수:{} 입니다.".format(name, score))
#
# # %%
# def vending_machine(money):
#     price=700
#     count=money//price
#     change=0
#     for i in range(count):
#         change=money-(i+1) * price
#         print("음료수 = %d개, 잔돈 = %d원" %(i+1, change))
#
# vending_machine(3000)
#
# # %%
# def get_average(marks):
#     # print(marks.values())
#     total=0
#     avg=0.0
#     for i in list(marks.values()):
#         total += i
#     avg=total/len(marks)
#     return avg
#
# marks={'국어' : 90, '영어': 80, '수학': 85}
# print("평균 : %.2f" %get_average(marks))
#
# # %%
# total=0
# wedding={}
# def gift(dic,who,money):
#     global total
#     total += money
#     dic[who] = money
#
# gift(wedding, '영희', 30000)
# gift(wedding, '철수', 50000)
# gift(wedding, '이모', 100000)
#
# print("축의금 명단 : {}".format(wedding))
# print("축의금 총계 : {}".format(total))
#
# # %%
# # 모듈 : .py로 저장되는 파이썬 파일 1개
# # 패키지 : 여러 모듈을 담고 있는 폴더
# # import 모듈명
# # from 모듈 import 함수
# # from 모듈 import 함수1, 함수2
# # from 모듈 import * //(함수 전체)
#
# import random
# import time
# pot = [n for n in range(1,46)]
# jackpot=[]
# for n in range(1,7):
#     random.shuffle(pot)
#     pick = pot.pop()
#     print("{}번째 당첨번호는 {}입니다.".format(n, pick))
#     jackpot.append(pick)
#     time.sleep(1)
#
# jackpot.sort()
# print("이번 주 당첨번호는 {}".format(jackpot))
#
# # %%
# import random as r
# import time
#
# answer = r.randint(1,100)
# print("UpDown 게임 시작...")
# start=time.time()
#
# while True:
#     n=int(input("값을 맞춰보세요?"))
#     if answer == n:
#         print("정답입니다.")
#         break
#     elif answer<n:
#         print('Down')
#     else:
#         print('Up')
#
# end = time.time()
#
# elapse = end - start
# print("%d초 만에 성공!" %elapse)
#
# # %%
# nation=['그리스','아테네','독일','베를린','러시아','모스크바','미국','워싱턴']
# file = open('nation.txt', "wt") # wt:text, wb:binary
# for idx, country in enumerate(nation):
#     if idx %2 ==0:
#         file.write(nation[idx] +'-' + nation[idx+1] + '\n')
# file.close()
#
# # %%
# # -*- coding: utf-8 -*-
# old_file = open("연락처2.txt", "rt", encoding='UTF8')  #CP949/euc-kr/ISO...
# buffer = old_file.read()
# n = buffer.count("011-")
# buffer=buffer.replace("011-", "010-")
# print("총 {}건의 011 데이터를 찾았습니다.".format(n))
# old_file.close()
#
# new_file=open("연락처.txt", "wt", encoding='UTF8')
# new_file.write(buffer)
# new_file.close()
# print("데이터 수정 완료!")
#
# # %%
# fileName=""
# while True:
#     fileName=input("복사할 원본 파일명 : ")
#     extName=fileName[fileName.rfind('.')+1:]
#     if extName != "txt":
#         print("텍스트 파일이 아닙니다.")
#     else:
#         break
#
# with open(fileName, 'rt', encoding="utf-8") as source:
#     with open("복사본-"+fileName, 'wt', encoding='utf-8') as copy:
#         while True:
#             buffer=source.read(1)
#             if not buffer:
#                 break
#             copy.write(buffer)
#
# print("복사본-"+fileName+" 파일이 생성되었습니다.")
#
# # %% 엑셀 csv 파일에서 특정 필드값 처리하기.
# import csv
# fileName="CCTV설치현황(서울)_210731기준.csv"
# with open(fileName) as csvfile:
#     buffer = csv.reader(csvfile, delimiter=",", quotechar='"')
#     total = 0
#     for idx, line in enumerate(buffer):
#         if idx >= 3: # 0~2번 줄의 헤드 데이터는 skip
#             print(line)
#             total += int(line[1].replace(',','')) # 1번 컬럼 데이터가 총계임.
#
# print('CCTV 설치 대수는 총 {}대입니다.'.format(total))
#
# # %% csv 파일을 json 파일로 변환하기(1)
# import json
# import csv
#
# with open('CCTV설치현황(부천)_20210405.csv', 'r') as file_csv:
#     with open('CCTV설치현황(부천)_20210405.json', 'w') as file_json:
#         fieldnames = ("A","B","C","D","E","F","G","H","I","J")
#         reader = csv.DictReader(file_csv, fieldnames)
#         #print(reader.__next__().values())
#
#         # for row in list(reader):
#         #     print(row)
#         #     json.dump(row, file_json,indent=4)
#
#         json.dump(list(reader), file_json, indent=4, ensure_ascii=False)
#         # file_json.write(json.dumps(list(reader), indent=4, ensure_ascii=False))
#
#
# # %% csv 파일을 json 파일로 변환하기(2)
# import csv
# import json
#
# csvfile = open('CCTV설치현황(부천)_20210405.csv','r')
# jsonfile = open(file='CCTV설치현황(부천)_20210405.json',mode='w')
# # fieldNames = ("A","B","C","D","E","F","G","H","I","J")
# fieldNames = ("담당부서","담당부서연락처","설치목적","수량(개소)","작동방식","촬영시간","촬영범위","설치위치","영상정보 보관기간","화상정보 보관(열람)장소")
# reader = csv.DictReader(csvfile, fieldnames=fieldNames)
# data = list(reader)
# #json.dump(data, jsonfile, indent=4, ensure_ascii=False)
# jsonfile.write(json.dumps(data, indent=4, ensure_ascii=False))
# csvfile.close()
# jsonfile.close()
#
#
# # %% json 파일에서 특정 필드값 처리하기.
# import json
# with open('CCTV설치현황(부천)_20210405.json', 'r') as jsonfile:
#     buffer = jsonfile.read()
#     cctv_list =  json.loads(buffer)
#     cctv_purpose = set() # set()형의 자료는 중복을 배제함.
#     for place in cctv_list:
#         cctv_purpose.add(place['설치목적'])
#
# print(sorted(cctv_purpose))
#
# # %%
# class Book:
#     def set_info(self, title, author):
#         self.title=title
#         self.author=author
#
#     def print_info(self):
#         print("책 제목 : "+self.title)
#         print("책 저자 : "+self.author)
#
# book1 = Book()
# book2 = Book()
#
# book1.set_info("파이썬", "민경태")
# book2.set_info("어린왕자", "생택쥐베리")
#
# book1.print_info()
# book2.print_info()
#
# # %%
# class Watch:
#     def set_time(self):
#         now=input("시간을 입력하세요.>>>")
#         hms=now.split(":")
#         self.hour=int(hms[0])
#         self.minute=int(hms[1])
#         self.second=int(hms[2])
#
#     def add_hour(self,hour):
#         if hour<=0:
#             return
#         self.hour += hour
#         self.hour %= 24
#
#     def add_minute(self,minute):
#         if minute<=0:
#             return
#         self.minute += minute
#         self.add_hour(self.minute//60)
#         self.minute %= 60
#
#     def add_second(self,second):
#         if second<=0:
#             return
#         self.second += second
#         self.add_hour(self.minute//60)
#         self.second %= 60
#
#     def see(self):
#         print("계산된 시간은 ", end='')
#         print("{}시 {}분 {}초입니다.".format(self.hour, self.minute, self.second))
#
# w=Watch()
# w.set_time()
# w.see()
# w.add_hour(10)
# w.see()
# w.add_minute(70)
# w.see()
#
# # %%
# class Song:
#     def set_song(self, title, genre):
#         self.title=title
#         self.genre=genre
#
#     def print_song(self):
#         print("노래제목: {}({})".format(self.title, self.genre))
#
#
# class Singer:
#     def set_singer(self, name):
#         self.name=name
#
#     def hit_song(self, song):
#         self.song=song
#
#     def print_singer(self):
#         print("가수이름 : {}".format(self.name))
#         self.song.print_song()
#
# song1=Song()
# song1.set_song("나비야", "동요")
#
# singer1=Singer()
# singer1.set_singer("길동이")
#
# singer1.hit_song(song1)
# singer1.print_singer()
#
# #%% Person 클래스 메소드
# class Person:
#     population=0
#
#     def __init__(self, name):
#         self.name=name
#         Person.population += 1
#         print("{} is born".format(self.name))
#
#     def __del__(self):
#         Person.population -= 1
#         print("{} is dead".format(self.name))
#
#     @classmethod
#     def get_population(cls):
#         return cls.population
#
# man = Person("james")
# woman = Person("emily")
# print("전체 인구수 : {}명".format(Person.get_population()))
# del man
# print("전체 인구수 : {}명".format(Person.get_population()))
# del woman
# print("전체 인구수 : {}명".format(Person.get_population()))
#
# # %% Shop 클래스
# class Shop:
#     total=0
#     menu_list = [{'떡복이':3000},{'순대':3000},{'튀김':500},{'김밥':2000}]
#
#     @classmethod
#     def sales(cls, food, count):
#         for menu in cls.menu_list:
#             if food in menu:
#                 cls.total += menu[food] * count
#
# Shop.sales("떡복이", 1)
# Shop.sales("김밥", 2)
# Shop.sales("튀김", 5)
#
# print("매출 : {}원".format(Shop.total))
#
# # %% class inheritance
# class Car:
#     max_oil = 50
#
#     def __init__(self, oil):
#         self.oil = oil
#
#     def add_oil(self, oil):
#         if oil<=0:
#             return
#         self.oil += oil
#         if self.oil > Car.max_oil :
#             self.oil = Car.max_oil
#
#     def car_info(self):
#         print("현재 주유상태 : {}".format(self.oil))
#
# class Hybrid(Car):
#     max_battery = 30
#
#     def __init__(self, oil, battery):
#         super().__init__(oil)
#         self.battery = battery
#
#     def charge(self, battery):
#         if battery<=0:
#             return
#         self.battery += battery
#         if self.battery > Hybrid.max_battery :
#             self.battery = Hybrid.max_battery
#
#     def hybrid_info(self):
#         super().car_info()
#         print("현재 충전상태 : {}".format(self.battery))
#
#
# car = Hybrid(0,0)
# car.add_oil(100)
# car.charge(30)
# car.charge(20)
# car.hybrid_info()
#
# # %% exception
# class Quiz:
#     # answer = ['경기도','강원도','충청남도','충청북도','전라남도','전라북도','경상남도','경상북도','제주특별자치도']
#     answer = ['경기도','강원도']
#
#     @classmethod
#     def challenge(cls):
#         if not cls.answer:
#             print("모두 맞추었습니다. 성공!")
#             return
#         do = input("정답은?>>> ")
#         if do not in cls.answer:
#             raise Exception("틀렸습니다.")
#
#         # for i, ans in enumerate(cls.answer):
#         #     if do == ans:
#         #         print("정답입니다.")
#         #         cls.answer.pop(i)
#         #         cls.challenge()
#
#         if do in cls.answer:
#             print("정답입니다.")
#             cls.answer.pop(cls.answer.index(do))
#             cls.challenge()
#
# try:
#     print('우리나라 9개도를 맟추는 퀴즈! 하나씩 입력하세요.')
#     Quiz.challenge()
# except Exception as e:
#     print(e)
#
# #%% up down game
# import random
#
# class UpDown:
#
#     def __init__(self):
#         self.answer=random.randint(1,100)
#         self.count=0
#
#     def challenge(self):
#         self.count += 1
#         n = int(input("입력(1~100) >>> "))
#         if n<1 or n>100:
#             raise Exception("1~100 사이의 값만 입력하세요.")
#         return n
#     def play(self):
#         while True:
#             try:
#                 n=self.challenge()
#             except Exception as e:
#                 print(e)
#             else:
#                 # 정상 값 입력 시
#                 if self.answer < n:
#                     print("Down")
#                 elif self.answer>n :
#                     print("Up")
#                 else:
#                     print("%d회수 만에 정답입니다." %self.count)
#                     break
#
# game =UpDown()
# game.play()
#
# # %%
# class BankError(Exception):
#     def __init__(self, message):
#         super().__init__(message)
#
# class BankAccount:
#     def __init__(self, acc_no, balance):
#         self.acc_no=acc_no
#         self.balance = balance
#
#     def deposit(self,money):
#         if money < 0:
#             raise BankError("%d원 입금 불가:" %money)
#         self.balance += money
#
#     def withdraw(self, money):
#         if money <= 0:
#             raise BankError("%d웝 출금 불가" %money)
#         if money > self.balance:
#             raise BankError("잔액부족")
#         self.balance -= money
#         return money
#     def transfer(self, your_acc, money):
#         your_acc.deposit(self.withdraw(money))
#
#     def inquiry(self):
#         print("계좌번호 : %s " %self.acc_no)
#         print("통장잔액 : %s원" %self.balance)
#
# me = BankAccount("1234", 50000)
# you = BankAccount("1111", 50000)
#
# try:
#     #me.deposit(-1000)
#     #me.withdraw(-1000)
#     #me.withdraw(100000)
#     me.transfer(you, 5000)
# except BankError as e:
#     print(e)
# finally:
#     me.inquiry()
#     you.inquiry()
#
# %% (크롤링1) 네이버 영화인 목록 가져오기
from bs4 import BeautifulSoup
import requests

url="https://movie.naver.com/movie/sdb/rank/rpeople.naver"
reponse = requests.get(url)
html = reponse.text
soup = BeautifulSoup(html, 'html.parser')
result_list=soup.find_all('td', class_='title')

movie_in=[]
for result in result_list:
    movie_in.append(result.text.strip())

for person in movie_in:
    print(person)
#
# # %% (크롤링2) 네이버 영화 제목 - 조회수 순으로..
#
# from bs4 import BeautifulSoup
# import requests
#
# url="https://movie.naver.com/movie/sdb/rank/rmovie.naver"
# reponse = requests.get(url)
# html = reponse.text
# soup = BeautifulSoup(html, 'html.parser')
# result_list=soup.find_all('div', class_='tit3')
#
# movie_in=[]
# for result in result_list:
#     movie_in.append(result.text.strip())
#
# for person in movie_in:
#     print(person)
#
# # %% (크롤링3) 네이버 영화 - 순위 상승된 영화
# from bs4 import BeautifulSoup
# import requests
#
# url="https://movie.naver.com/movie/sdb/rank/rmovie.naver"
# reponse = requests.get(url)
# html = reponse.text
# soup = BeautifulSoup(html, 'html.parser')
# movie_list = soup.find_all('tr')
#
# up_list = []
# for movie in movie_list:
#     target_list = movie.find_all('td', class_='ac')
#     if target_list:
#         # up : 순위상승, down: 순위하락, na: 변동없음
#         if target_list[1].find('img', class_='arrow').get('alt') == 'up':
#             up_list.append(movie.find('td', class_='title').text.strip())
#
# for up_movie in up_list:
#     print(up_movie)
#
# # %% 원형그래프 시각화
# import matplotlib.pyplot as plt
# from matplotlib import font_manager, rc
#
# font_path = "c:\Windows\Fonts\malgunsL.ttf"
# font_name = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font_name)
#
# figure = plt.figure()
# axes = figure.add_subplot(111)
#
# data = [0.18, 0.3, 3.33, 3.75,0.38, 25,0.25, 2.75,0.1]
# vitamin = ['비타민A','비타민B1','비타민B2','나이아신','비타민B6','비타민C','비타민D','비타민E','엽산']
#
# axes.pie(data, labels=vitamin, autopct="%0.1f%%")
# plt.axis('equal')
# plt.show()
#
# # %% 막대 그래프
# import random
# import matplotlib.pyplot as plt
#
# figure = plt.figure()
# axes = figure.add_subplot(111)
# x=[n for n in range(101)]
# y1=[]
# y2=[]
#
# for i in range(101):
#     y1.append(random.randint(0, 100))
#     y2.append(random.randint(0, 100))
#
# axes.plot(x, y1, color='r', marker=".")
# axes.bar(x, y2, color='g')
# plt.show()
#
# # %% 주소록 검색 메소드
# class AddressBook:
#     def search(self):
#         print("=== 주소록 검색 ===")
#         name = input("찾을 이름을 입력 >>> ")
#         if not name:
#             print("입력된 이름이 없어 검색을 취소합니다.")
#             return
#         exist = False
#         for person in self.address_list:
#             if name == person.name:
#                 person.info()
#                 exist = True
#         if not exist:
#             print("{}의 정보가 없습니다.".format(name))
#
# # %%
#
#
#
#
