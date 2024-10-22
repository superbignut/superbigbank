import multiprocessing
import os
import threading
import subprocess
import time
import signal

from superbigshow.api import show_process
from data_test import show
from superbigshow.app import showw

if __name__ == '__main__':
    print(os.path.join(os.path.dirname(__file__),"app.py"))