import pyautogui

print(pyautogui.size())
#print(pyautogui.position())
#pyautogui.moveTo(100, 200)
print('press ctrl-c to quit')
try:
    while True:
        x,y = pyautogui.position()
        positionStr = 'X:'+str(x).rjust(4)+'Y:'+str(y).rjust(4)
        print(positionStr)
        pass
except KeyboardInterrupt:
    print('\nDone.')