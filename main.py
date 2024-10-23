import signal,sys

def handleInt(sign,no):
    print("interrupted")
    # sys.exit()

signal.signal(signal.SIGINT, handleInt)    # exception raised is IOError

a = sys.stdin.read(1)
try:
   pass
except IOError:
    print("io interrupt")
else:
    # else is executed only if no exception was raised
    print("done")