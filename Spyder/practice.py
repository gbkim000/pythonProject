# (방법1)
# import 문의 마지막은 항상 모듈이나, 패키지만 올 수 있음
# 즉, from ~ import문을 사용할 때처럼, 클래스나 함수를 직접 임포트 할 수 없음.
# import travel.thailand
# trip1 = travel.thailand.ThailandPackage()    # 객체 생성
# trip1.detail()

# (방법2)
# 다음과 같이 from ~ import 함수명 형식을 사용할 수도 있음.
# from travel.thailand import *   # thailand 모듈의 모든 함수, 클래스 import
# trip1 = ThailandPackage()       # 객체 생성
# trip1.detail()

# (방법3)
# from travel.thailand import ThailandPackage  # thailand 모듈의 해당 클래스 import
# trip1 = ThailandPackage()       # 객체 생성
# trip1.detail()

# (방법4)
# from travel import vietnam      # travel 패키지의 vietnam 모듈을 import 함
# trip2 = vietnam.VietnamPackage()
# trip2.detail()

# (방법5)
# 모듈의 import할 모듈 설정하기
# 아래 문장을 사용할 경우 travel 패키지의 __init__에서 import할 모듈을 설정해야 함.
# (예시) __all__ = ["vietnam"]
# from travel import *    # travel 패키지의 모든 모듈을 import
# trip2 = vietnam.VietnamPackage()
# trip2.detail()
# trip1 = thailand.ThailandPackage()
# trip1.detail()

# 모듈의 위치 확인하기
import inspect
import random
from travel import vietnam
print(inspect.getfile(random))
print(inspect.getfile(vietnam))

# 파이썬 패키지 색인 사이트(python package index)
# https://pypi.org/
# pip install 패키지
# pip uninstall 패키지
# pip install --upgrade 패키지
# pip show 패키지
# soup = BeautifulSoup("html 코드")
# print(soup.prettify)  # 코드를 보기 좋게 정려해 줌

# print(dir())    # 사용가능한 함수들을 보여줌
# import random
# print(dir())    # random 모듈이 추가로 출력됨
# import pickle
# print(dir())    # random 모듈이 추가로 출력됨

lst = [1, 2, 3]
print(dir(lst)) # 리스트 객체를 대상으로 사용할 수 있는 메소드 출력

name = "James"
print(dir(name)) # 문자열 객체를 대상으로 사용할 수 있는 메소드

# 내장 함수(구글 검색) : list of python builtins
# --> https://docs.python.org/3/library/functions.html

# 외장 함수(구글 검색) : list of python modules
# --> https://docs.python.org/3/py-modindex.html

# glob : 경로 내의 폴더/파일 목록 조회(윈도 dir)
import glob
print(glob.glob(("*.py")))  # 현재 폴더에서 확장자가 .py인 파일 목록

import os
print(os.getcwd())          # 현재 디렉토리 출력

folder = "sample_dir"

if os.path.exists(folder):
    print("이미 존재하는 폴더입니다.")
    os.rmdir(folder)
    print(folder, "폴더를 삭제하였습니다.")
else:
    os.makedirs(folder)
    print(folder, "폴더를 생성하였습니다.")

print(os.listdir()) # 현재 디렉토리의 파일, 폴더를 출력

import time
print(time.localtime())
print(time.strftime("%Y-%m-%d %H:%M:%S"))

import datetime
print("오늘 날짜는 : ", datetime.date.today())
today = datetime.date.today()
td = datetime.timedelta(days=100)
print("우리가 만난지 100일째 되는 날은 : ", today+td, "입니다.")
