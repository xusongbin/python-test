
import autopy
from time import sleep


if __name__ == '__main__':
    autopy.mouse.smooth_move(100, 100)
    sleep(1)
    autopy.mouse.smooth_move(200, 200)
    sleep(1)
    autopy.mouse.smooth_move(300, 300)
    sleep(1)
    autopy.mouse.smooth_move(400, 400)
    sleep(1)