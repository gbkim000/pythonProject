# %% 파일의 경로 및 파일명 출력

import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
from PyQt5 import uic, QtCore
 
def pathPrint():
    
    #os.path.abspath 절대 경로를 반환하지만 인수에서 심볼릭 링크를 확인하지 않습니다.
    #os.path.realpath 먼저 경로의 모든 심볼릭 링크를 확인한 다음 절대 경로를 반환합니다.
    #(예시) file = "shortcut_folder/filename" - 바로가기 폴더
    #os.path.abspath(file) = "C:/Desktop/shortcut_folder/filename"
    #os.path.realpath(file) = "D:/PyCharmProjects/Python1stClass/filename"
    
    print(__file__)            # 파일의 현재 위치 및 파일명, __file__는 전역변수
    print(os.path.realpath(__file__))   # 심볼릭 링크 등의 실제 경로
    print(os.path.abspath(__file__))    # 파일의 절대경로 및 파일명
    print()
    
    print(os.getcwd())                  # 현재 디렉토리
    print(os.path.dirname(__file__))    # 파일의 경로명
    print(os.path.dirname(os.path.realpath(__file__)))  # 파일의 경로명
    
    print()
    os.chdir("C:\\Users\\Administrator\\Spyder")        # 현재 디렉토리 변경
    print(os.getcwd())                                  # 현재 디렉토리
    os.chdir("C:\\Users\\Administrator\\PyQtTest")      # 현재 디렉토리 변경        
    print(os.getcwd())                                  # 현재 디렉토리
    
    #print(os.listdir(os.getcwd()))         # 현재 디렉토리의 파일 리스트
    #print(os.listdir("./"))                # 현재 디렉토리의 파일 리스트
    
    if os.path.exists("./test_dir"):
        print("This dir exists")       
        os.rmdir('test_dir')            # 디렉토리가 비어있을 때 삭제
    os.mkdir('test_dir')
    
    #print(os.listdir())
    #shutil.rmtree('test_dir')          # 디렉토리안의 모든 내용을 삭제
    
    # 현재 실행 파일의 경로명과 파일명을 분리
    path = os.path.realpath(__file__)
    paths = os.path.split(path)     # 튜플(경로명, 파일명)   
    print(paths)
    
    # Path가 디렉토리인지 확인
    if os.path.isdir("./test_dir"):
        print("It's directory")
        
    # Path가 파일인지 확인
    if not os.path.isfile("C:\\Users\\Administrator\\PyQtTest"):
        print("It's not file")
        
    if os.path.isfile("./main.py"):
        print("It's file")

pathPrint()


     
