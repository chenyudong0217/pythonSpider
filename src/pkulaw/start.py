# encoding: utf-8
import sys
import time
import threading
import loginManage
import Spider


if __name__ == '__main__':
    threading.Thread(target=loginManage.start)
    threading.Thread(target=Spider.)