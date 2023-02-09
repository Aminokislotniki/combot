import os
import time
# path = os.getcwd()
# print(path)


num = 1
x = 2
while x > 1:
    try:
        os.replace(os.getcwd()+'/groups/-839915842',
        os.getcwd()+'/arhive_group/-839915842')
        break
    except PermissionError:
        num = num + 1
        try:
            text = f'({num})'
            os.rename(os.getcwd() + '/groups/-839915842',
                        os.getcwd() + '/arhive_group/-839915842'+str(text))
            time.sleep(2)
            break
        except FileExistsError:
            x = 2
            pass




