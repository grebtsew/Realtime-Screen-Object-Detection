import time
import threading

def start_server(name):
    import subprocess
    subprocess.run(["python", name+".py"])

if __name__ == '__main__':
    """
    COPYRIGHT @ Grebtsew 2019

    This file starts the demo mode where all servers and clients run on local pc!
    """

    threading.Thread(target=start_server, args=("QtServer",)).start()
    time.sleep(2)
    threading.Thread(target=start_server, args=("TfServer",)).start()
    time.sleep(5)
    threading.Thread(target=start_server, args=("MssClient",)).start()
