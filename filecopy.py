#Baolong Nguyen
#Bryan Daroy
#CECS 326 - Project 1
#DUE: 9/30/25

import os
import sys
import multiprocessing as mp
from multiprocessing import Process, Pipe

def parent_process(content, connect):
    try:
        connect.send(content)
    except Exception as e:
        print(f"An error occured: {e}")
        sys.exit(1)
    connect.close()


def child_process(copyfile, connect):
    try:
        received = connect.recv()
        with open(copyfile, 'w') as text:
            text.write(received)
    except Exception as e:
        print(f"An error occured: {e}")
        sys.exit(1)
    connect.close()


def main():
    try: #checks for the 2 arguments
        textfile = sys.argv[1]
        copyfile = sys.argv[2]
    except IndexError:
        print("Please enter the two file names")
        sys.exit(1)

    try:    #opens text file
        with open(textfile, 'r') as text:
            content = text.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)
    except Exception as e:
        print(f"An error occured: {e}")
        sys.exit(1)

    try:    #opens blank text file, if not made yet then make it
        with open(copyfile, 'w') as text:
            text.write(content)
    except Exception as e:
        f = open(copyfile, 'w')
        f.close()

    parent, child = mp.Pipe() #created multiprocessing pipe
    pid = os.fork() #forked the process

    if pid > 0: #parent
        child.close()
        parent_process(content, parent)
        os.waitpid(pid, 0)
    else: #child
        parent.close()
        child_process(copyfile, child)
        os._exit(0)

    print(f"File {textfile} copied to {copyfile}")

if __name__ == "__main__":
    main()