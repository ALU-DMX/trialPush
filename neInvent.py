# Libraries
###########
from prettytable import PrettyTable
import telnetlib
import time
import re
import sys
import datetime

tcPass1 = 1

# Save logs in a file
######################
#sys.stdout=open("C:\\Users\\vairavels\\Desktop\\tCsuite.txt","w")

# Functions
###########
def ANSI(host):
    try:
        global tn
        tn=telnetlib.Telnet(host,port)
        time.sleep(1)
        tn.write(b";")
        tn.read_until(b"session not active ",5)
        tn.write(b'ACT-USER::user1:::Ansi_svt1;')
        tn.read_until(b"COMPLD",5)
        tn.read_until(b';')
    except:
        print ("\nLogin to the ANSI user denied...!")
        exit()

def FLC(ip):
    global tn
    tn=telnetlib.Telnet(ip,port)
    tn.set_debuglevel(10)
    tn.read_until(b"login:",5)
    tn.write(b"appl\n")
    tn.read_until(b"password: ",5)
    tn.write(b"1678mcc\n")
    tn.read_until(b"appl@emserv:~$",5)
    tn.write(b'bash\n')

# Get the node ip from user
###########################
#NE = input("Enter the Node ip address:")
#port = input("Enter the port number Ansi/FLC:")
NE="10.10.189.158"
port=3083

def neInventory():
    print("\nExecution started")
    now = datetime.datetime.now()
    #print ("Current date and time : ")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))

    if port==3083:
        #print("you are logging into TL1 command mode:\n")
        ANSI(NE)
        tn.write(b'RTRV-COND-ALL:::;')
        output1 = tn.read_until(b';', timeout=5)
        #print (output1.decode('ascii'))
        tn.write(b'RTRV-EQPT::ALL;')
        output2 = tn.read_until(b';', timeout=5)
        output2 = (output2.decode('ascii'))
        #print(output2)
        str_op2 = output2.split('\n')
        #print('----------------------------------------')
        print('\n           Available Boards and SFPs in 1678MCC NE\n')
        #print('----------------------------------------\n')
        t = PrettyTable(['Board/port no ', 'CardType','XFP Prov-Actual','State/alarm'])
        for line in str_op2:
            line = line.strip()
            if re.match(r'("P2XGE|"P16S16|"MX320GA|"MX640GA|"P16S1S4|"ES64SC|"P4S64X|"P2S64X|"FLCCONGI|"FLCSERVA|"P8S16|"P4S16|"P2S64M|"P4S64M|"P16GE|"LAX40|"LAX20|"LAC40)', line):
                op = re.search(r'(.*)\-(\d+)\-(\d+)\-(\d+)\::(\w+)\=(\w+)\,(\w+)\=(\w+)\,(\w+)\=(\w+)\:(\w+)',line)
                t.add_row([op.group(4),op.group(1)+'"','',op.group(11)])
            elif re.match(r'("SFP|"XFP)', line):
                op = re.search(r'(\w+)\-(\d+)\-(\d+)\-(\d+)\-(\d+)::(\w+)\=(\w+)\,(\w+)\=(\w+)\,(\w+)\=(\w+)\:(\w+)',line)
                t.add_row([op.group(4)+'-'+op.group(5),' ',op.group(7)+'-'+op.group(9),op.group(12)])
        t.align="l"
        print(t)
        
        return tcPass1
    
          
        tn.write(b"CANC-USER;")
    
    
    elif port==23:
        print("you are login into FLC mode")
        FLC(NE)
    
    else:
        print("Please enter the correct port number")
    
    print("Execution Completed")
    print("*****************************************************************")
    #sys.stdout.close()

#neInventory()