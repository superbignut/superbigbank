import multiprocessing
import os


def consumer(pipe):
    conn1, conn2 = pipe
    print('consumer conn1 id', id(conn1))
    print('consumer conn2 id', id(conn2))
    print("process consumer id", os.getpid())

    conn2.close()  # input pipe close 1
    while True:
        try:
            item = conn1.recv()
        except EOFError:
            print('EOFError')
            break
        print(item)
    print('consumer done')


def producer(listArr, conn2):
    for item in listArr:
        conn2.send(item)


if __name__ == '__main__':
    (conn1, conn2) = multiprocessing.Pipe()
    cons_p = multiprocessing.Process(target=consumer, args=((conn1, conn2),))
    cons_p.start()

    conn1.close()  # output pipe clsoe 1

    arr = [1, 2, 3, 4, 5]
    producer(arr, conn2)
    print('main conn1 id', id(conn1))
    print('main conn2 id', id(conn2))
    conn2.close()  # 这行如果不注释掉的话， 子进程由于 收不到 EOF 导致结束关不掉

    cons_p.join()