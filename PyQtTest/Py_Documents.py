# -*- coding: utf-8 -*-
'''
Qt for Python : 
https://doc.qt.io/qtforpython/api.html


미해결 과제
(1) 실행중인 Thread list 가져오기 및 종료하기
(2) QThread join() 메서드 구현하기
(3) 현재 호출된 클래스의 부모(호출한) 클래스 참조하기
(4) pid = os.getpid() # 현재 스레드의 pid를 반환
    os.kill(pid, signal.SIGINT)
    
======== pyQt6 설치 폴더 설정하기 =========
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
pkgDir = 'C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PySide6\plugins'
pkgDir = 'C:\\ProgramData\\Miniconda3\\envs\\spyder-env\\Lib\\site-packages\\PySide6\\plugins'
pkgDir = 'C:\\Users\\Administrator\\example\\Lib\\site-packages'
QApplication.setLibraryPaths([pkgDir])

======== python 가상환경 만들기 ===========
C:\\Users\\Administrator>python3 -m venv venv
C:\Users\Administrator>call venv/scripts/activate.bat
(venv) C:\Users\Administrator>pip install PyQt5

(venv) python3
>>> from PyQt5.QtWidgets import QApplication, QLabel
>>> app = QApplication([])
>>> label = QLabel('Hello World!')
>>> label.show()
>>> app.exec()

======== <QThread> =======================
- QThread는 스레드가 시작될 때 started() 를, 중지될 때 finished() 신호를 통해 통지하고 
- isFinished() 및 isRunning()을 사용하여 스레드 상태를 알 수 있다.
- 스레드를 중지 할 때는 exit() 또는 quit()를 호출한다. 
- 실행중인 스레드를 강제로 종료하는 terminate() 를 호출 할 수 있지만 그런 상황은 되도록이면 없어야한다.
- exit() 또는 quit()를 호출한 다음에는 스레드가 실행을 완료할 때까지(또는 지정된 시간이 지날 때까지) 
  wait()를 사용하여 호출 스레드를 차단하는 것이 좋다.
- Qt 4.8부터는 finished() 신호를 QObject::deleteLater()에 연결하여 종료 한 스레드 객체를 안전하게 해제 할 수 있다.
- 또한 플랫폼 독립적인 정적 sleep 함수를 제공한다. sleep(), msleep() 및 usleep()은 각각 초, 밀리초 및 마이크로초를 단위의 함수들이다.
- Qt는 이벤트 중심(event-driven) 프레임 워크이므로 일반적으로 wait() 및 sleep() 함수는 필요하지 않을 수 있다. 
- wait() 대신 finished() 시그널을 이용하는 것을 고려하자.

======== <threading module> ===============
- threading.Thread() 함수 호출하여 thread 객체를 얻는다
- thread 객체의 start() 메서드를 호출한다.
- 객체를 생성했다 하더라도 start()를 호출해야만 thread가 시작된다.
- join(timeout) 메서드 : subthread가 종료될때까지 기다려 준다.
- join 메서드의 timeout을 초과해도 예외는 발생하지 않으며, None을 리턴한다.
- is_alive() : 해당 thread가 동작 중인지 확인한다

<Thread(name=, target=, args=, kargs=, *, daemon=)>
- name : thread의 이름, 주지 않아도 괜찮다
- target : thread에서 실행할 함수
- args : target에 넘겨질 인자, 튜플 형식
- kargs : target 이 키워드 인자를 받을 때 딕셔너리로 넘겨준다.
- daemon : 데몬 실행 여부, 이 값을 True로 설정하면 메인 thread가 종료되면 즉시 종료된다.

========== 
#%% 쓰레드를 만드는 세 가지 방법
# http://lvzuufx.blogspot.com/2015/10/qt_21.html

 PyQt QThread 사용법
https://ybworld.tistory.com/39
https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=soldatj&logNo=221223907865
https://coding-groot.tistory.com/103 
https://soooprmx.com/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%98-%EC%8A%A4%EB%A0%88%EB%93%9C-%EC%82%AC%EC%9A%A9%EB%B2%95/
https://wikidocs.net/82581
https://freeprog.tistory.com/351
https://investox.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A9%80%ED%8B%B0%EC%93%B0%EB%A0%88%EB%93%9C-%EC%98%A4%EB%A5%98%EC%97%86%EC%9D%B4-%EC%A2%85%EB%A3%8C%ED%95%98%EA%B8%B0-QThread-GUI
#https://coding-yoon.tistory.com/46
https://haerong22.tistory.com/39 (쓰레딩)

https://wiki.loliot.net/docs/lang/python/libraries/pyside2/pyside2-qthread/
https://wiki.qt.io/Threads_Events_QObjects/ko

# 파이썬(python) - 클래스(class)의 특징
  https://tibetsandfox.tistory.com/40
  
# 41. class 정리 - 클래스 기본적인 사용
  https://wikidocs.net/16071
  
# 6. 클래스 (2) - 클래스 심화 (상속, 메서드 오버라이딩, 추상)
  https://rebro.kr/134
  
'''

# %% dir() / sys.path 명령
'''
- namespace 변수 확인하기 : print(dir())
- 경로설정 출력하기 : sys.path (python interprer 설정에 따라 결과 다름)

- GridLayout 간격 조정하기(stretch 설정)
- https://studyingrabbit.tistory.com/24

'''

# %% 가상환경 만들기
'''
# -----------------------------------------------------
(1) Windows PowerShell 실행(관리자)

(2) 가상환경(example) 생성 및 패키지 설치하기
    > python -m venv example
    > cd example
    > .\Scripts\Activate.bat
    > .\Scripts\Activate.ps1
    > pip install PyQt5
    > pip install PySide6

(3) spyder interpreter 변경
    --> C:\Users\Administrator\example\Scripts>python.exe

(4) path 확인하기
    import sys    
    sys.path

# -----------------------------------------------------    
** 참고 : 가상환경 모듈 만들기2(powerShell 관리자로 실행) **

    > pip install virtualenv    ; Python2 사용시 권장
    > python3 -m venv example   ; Python3 사용시 권장
    > virtualenv example (또는 virtualenv example --python=python3.9)
    > activate.bat   ; 가상환경 진입
    > (example) decativate.bat  ; 가상환경 종료
    
    > rm -rf example            ; 가상환경 삭제(폴더 삭제)

# -----------------------------------------------------    
(base) ------ 가상환경 1
        ㄴ--- 가상환경 2
        ㄴ--- 가상환경 3

conda env list #가상환경 목록 보기
conda activate (가상환경이름) #(가상환경이름으로 들어가서 작업할 수 있음)
conda deactivate #다시 base 전역 환경으로 나올 수 있음
conda pip list #현재 깔린 모듈 볼 수 있음
conda pip freeze #현재 깔린 모듈 볼 수 있음

pip freeze > requirements.txt   (requirments.txt로 바로 현재 환경의 모듈들을 내보낼 수 있음)
pip install -r requirements.txt (바로 requirements.txt에 포함된 버전의 모듈들 설치)
pip uninstall -r requirements.txt (바로 requirements.txt에 포함된 버전의 모듈 제거)

########### 가상환경 패키지 지우고 싶다면
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y       

########### 만약 가상환경을 삭제하려면
conda remove -n .\example\ --all
 
'''
# %% Qt 모듈 documention
'''
All Qt Documentation : https://doc.qt.io/qt.html
Qt for Python Modules : https://doc.qt.io/qtforpython-6/api.html
                        https://doc.qt.io/qtforpython-6/modules.html
'''
# %% 파이썬 실행 파일 만들기(Pyinstaller)
""" 
(1) pyinstaller 설치
    https://www.pyinstaller.org/
    pip install pyinstaller
(2) 실행파일 만들기
    소스파일이 저장된 폴더로 이동 및 실행 파일만들기
    pyinstaller source.py
(3) 서브디렉토리 'dist'로 이동
    source.exe 실행
(4) 콘솔창 출력되지 않도록 하기
    다음과 같이 명령어에 '-w' 또는 '--windowed'를 추가해줍니다.
    pyinstaller -w source.py
(5) 실행파일 하나만 생성하기
    실행파일 하나만 생성하기 위해서는 명령어에 ‘-F’ 또는 ‘–onefile’을 추가합니다.
    pyinstaller -w -F source.py 
    pyinstaller -w -F Memorizing.py
(6) 실행파일 만들기(upx-win64로 용량 줄이기) : pyinstaller --upx-dir ./upx396 -w -F Memorizing.py


[pip 설치/업그레이드, spyder 업그레이드]

    (1) [get-pip.py 다운로드] : curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    (2) [pip install] : python get-pip.py
    (3) [Upgrading pip] : python -m pip install --upgrade pip
    (4) [Updating spyder] : pip install -U spyder
    (5) [Reset preferences] : spyder --reset

<스파이더 실행 오류 해결>
# pip install spyder‑kernels==2.1.*
# 스파이더 설정 초기화 : spyder --reset


[참고한 튜토리얼과 강의]
https://wikidocs.net/book/2165

* PyQt5 공식 문서 (http://pyqt.sourceforge.net/Docs/PyQt5/)
* pythonspot (https://pythonspot.com/gui/)
* zetcode (http://zetcode.com/gui/pyqt5/)
* opentutorials.org (https://opentutorials.org/module/544)
* tutorialspoint (https://www.tutorialspoint.com/pyqt/)
udemy 강의1: Python Desktop Application Development with PyQt
udemy 강의2: Create Simple GUI Applications with Python and Qt

[python pyqt-database]
* https://www.tutorialspoint.com/pyqt/pyqt_database_handling.htm
* https://realpython.com/python-pyqt-database/#using-view-and-model-classes

* wxPython Grid : https://streamls.tistory.com/136


# QTableWidget - https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=anakt&logNo=221834285100
# https://wikidocs.net/book/2165 (PyQt5 Tutorial - 파이썬으로 만드는 나만의 GUI 프로그램)
# https://planet.turbogears.org/1.0/docs/Widgets/DataGrid.html#basic-datagrid-usage
# https://python.hotexamples.com/examples/datagrid.core/DataGrid/-/python-datagrid-class-examples.html

"""
