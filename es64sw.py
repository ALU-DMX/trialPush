import telnetlib
import time
import re


tcPass3 =1

# Save logs in a file
######################
#sys.stdout=open("C:\\Users\\vairavels\\Desktop\\tCsuite.txt","w")

#host=raw_input("Enter the Node ip address:")
#port=input("Enter the Port value: ")
host="10.10.188.14"
port=3083
tn=telnetlib.Telnet(host,port)

def logTL():
    try:
        global tn    
        tn=telnetlib.Telnet(host,port)
        time.sleep(1)
        tn.write(b";")
        tn.read_until(b"session not active ",5)
        tn.write(b'ACT-USER::user2:::Ansi_svt2;')
        tn.read_until(b"COMPLD",5)
        tn.read_until(b';')
    except:
        print ("\nLogin to the ANSI user denied...!")
        exit()                       

def swstatus():
    global esact1
    tn.write(b"RTRV-DX-EQPT::ALL;")
    line1=tn.read_until(b"RTRV-DX-EQPT::ALL",5)
    line1 = (line1.decode('ascii'))
    str_op3 = line1.split('\n')
    #print(line1)
    for line1 in str_op3:
        line1 = line1.strip()
        if re.match(r'("ES64SC)', line1):
            op = re.search(r'(\w+\-\d+\-\d+\-\d+\,\w+\-\d+\-\d+\-\d+)\::((\w+\=)(\w+\-\d+\-\d+\-\d+)),(\w+=\w+)',line1)
            esact1=op.group(2)
            print(esact1)
                        
def es64switch():
    ### Finding Active ES64 slot ###
    tn.write(b"RTRV-DX-EQPT::ALL;")
    line=tn.read_until(b"RTRV-DX-EQPT::ALL",5)
    line = (line.decode('ascii'))
    str_op2 = line.split('\n')
    #print("Printing line:",line)
    for line in str_op2:
        line = line.strip()
        if re.match(r'("ES64SC)', line):
            op = re.search(r'(\w+\-\d+\-\d+\-\d+\,\w+\-\d+\-\d+\-\d+)\::((\w+\=)(\w+\-\d+\-\d+\-\d+)),(\w+=\w+)',line)
            esact=op.group(2)
            print(line)
            print(esact)
        ### Execute ES64 switch command on active matrix ###
            if esact == "ACTIVE=ES64SC-1-3-4" :
                tn.write(b"SW-DX-EQPT::ES64SC-1-3-4;")
                print("---------------------------------------")
                print('       ES64SC switch is started        ')
                print("---------------------------------------")
                time.sleep(100)
                ### Finding Active ES64 slot ###
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                swstatus()
                print("---------------------------------------")
                print('  ES64 switch completed successfully   ')
                print("---------------------------------------")
                print("\nActive ES64SC before switch:",esact)
                print("Active ES64SC after switch :",esact1)
                tn.write(b"CANC-USER;")
            else:                
                tn.write(b"SW-DX-EQPT::ES64SC-1-3-3;")
                print("---------------------------------------")
                print('        ES64SC switch is started       ')
                print("---------------------------------------")
                time.sleep(100)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                swstatus()
                print("---------------------------------------")
                print('  ES64 switch completed successfully   ')
                print("---------------------------------------")
                print("\nActive ES64SC before switch:",esact)
                print("Active ES64SC after switch :",esact1)
                tn.write(b"CANC-USER;")
                
        
tn.write(b"CANC-USER;")

def logFLC():
    tn=telnetlib.Telnet(host,port)
    tn.set_debuglevel(10)
    tn.read_until(b"login:",5)
    tn.write(b"appl\n")
    tn.read_until(b"password: ",5)
    tn.write(b"1678mcc\n")
    tn.read_until(b"appl@emserv:~$",5)

def es64TC():
    if port==3083:
        #print( "you are login into TL1 command mode")
        x= range (1,2)
        for i in x:
            logTL()
            es64switch()
            print ('number of times switch executed is : ',x)
            print(i)
            
    elif port==23:
        print ("you are login into FLC mode")
        logFLC()
    
    else:
        print( "Please enter the correct port number")

    return tcPass3
#sys.stdout.close()

#es64TC()


