import psutil
import time
import logging
import threading
import os
import sys


timeOut = int(sys.argv[1])

cont = True

def aguardarEnter():
    global cont
    #input("\n*** Pressione ENTER para parar! ***\n")
    time.sleep(timeOut)
    cont = False

def monitorar():
    global cont
    num = 0
    inicioentradaNET = psutil.net_io_counters()[0]
    iniciosaidaNET = psutil.net_io_counters()[1]
    inicioUsoDisco = psutil.disk_usage('/')[1]
    logMonitor = logging.getLogger('logCPU_MEM')
    logMonitor.info("horario,memoria(%),cpu(%),Block-use(bytes),Net-in(bytes),Net-out(bytes),TimeStamp")

    while(cont == True):
        #CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
        cpu=psutil.cpu_percent()
        mem = psutil.virtual_memory()[2]
        entradaNET = psutil.net_io_counters()[0] - inicioentradaNET
        saidaNET = psutil.net_io_counters()[1] - iniciosaidaNET
        usoDisco = psutil.disk_usage('/')[1] - inicioUsoDisco
        valor = str(mem) + "," + str(cpu) +"," + str(usoDisco)+ "," +str(entradaNET)+ "," + str(saidaNET)+ ","+str(int(time.time()))
        logMonitor = logging.getLogger('logCPU_MEM')
        logMonitor.info(valor)
        num+=1
        print(num,'-',valor )
        time.sleep(1)

#print(psutil.virtual_memory())  # physical memory usage
#print('memory % used:', psutil.virtual_memory()[2])
def setup_logger(logger_name, log_file):
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s,%(message)s', datefmt='%H:%M:%S')
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_file)
    fileHandler = logging.FileHandler(filename, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(logging.INFO)
    log_setup.addHandler(fileHandler)


# -- MAIN -- #
setup_logger('logCPU_MEM', 'TxMonitor.csv')
print("Monitorando")
print("indice,memoria(%),cpu(%),Block-use(bytes),Net-in(bytes),Net-out(bytes),TimeStamp")

t1 = threading.Thread(target=aguardarEnter)
t2 = threading.Thread(target=monitorar)
t1.start()
t2.start()

t2.join()
