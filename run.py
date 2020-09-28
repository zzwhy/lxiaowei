
from threading import Thread
from LinkCrawl import DownLink
from ImageCrawl import DownImage
import time

def main():

    for j in range(2):
        Thread(target=DownLink().run).start()
    time.sleep(5)

    for i in range(5):
        x = Thread(target=DownImage().run)
        x.start()


if __name__ == '__main__':
    main()