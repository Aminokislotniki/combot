import time
import threading


def arhiv(time_):
    while True:
        print("q")
        time.sleep(time_)


t = threading.Thread(target=arhiv, args=(10,))  # 100 время на которое функция засыпает
t.start()