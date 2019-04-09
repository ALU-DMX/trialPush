import telnetlib
import time
import re


tcPass4 = 1

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
        tn.write(b'ACT-USER::ALCATEL:::Ansi_4GX1;')
        tn.read_until(b"COMPLD",5)
        tn.read_until(b';')
    except:
        print ("\nLogin to the ANSI user denied...!")
        exit()
        
def logFLC():
    tn=telnetlib.Telnet(host,port)
    tn.set_debuglevel(10)
    tn.read_until(b"login:",5)
    tn.write(b"appl\n")
    tn.read_until(b"password: ",5)
    tn.write(b"1678mcc\n")
    tn.read_until(b"appl@emserv:~$",5)

def groupstate():
    global mxact1
    tn.write(b"RTRV-DX-EQPT::ALL;")
    out=tn.read_until(b"RTRV-DX-EQPT::ALL",5)
    ### Finding Active matrix slot ###
    out = (out.decode('ascii'))
    str_out = out.split('\n')
    #print(out)
    for out in str_out:
        out = out.strip()
        if re.match('("MX640GA)', out):
            op = re.search(r'"(\w+\-\d+\-\d+\-\d+\,\w+\-\d+\-\d+\-\d+)\::(\w+\=\w+\-\d+\-\d+\-\d+),(\w+=\w+)"',out)
            mxact1=op.group(2)
            print(op.group(0))
            print(mxact1)
            grpst = op.group(3)
            #print(grpst)
            if grpst ==  "GROUPSTATE=NOREQ" :
                print('checking Matrix noreq condition...')
                print(grpst)
                time.sleep(60)
                print ('checked noreq condition')
            elif grpst == "GROUPSTATE=DEGRADED" :
                print('checking Matrix degrade condition...')
                print(grpst)
                time.sleep(500)
            elif grpst == "GROUPSTATE=NOREQ" :
                print('checking noreq condition...')
                print(grpst)
                time.sleep(30)
                print ('checked noreq condition')
            elif grpst == "GROUPSTATE=DEGRADED" :
                print( 'matrix switch not happen with in 17 mins of time')
                time.sleep(50)
                print(grpst)
            else:
                print ('Matrix switch not succesful')
        
def mx_sw():
    tn.write(b"RTRV-DX-EQPT::ALL;")
    line=tn.read_until(b"RTRV-DX-EQPT::ALL",5)
    ### Finding Active matrix slot ###
    line = (line.decode('ascii'))
    str_op2 = line.split('\n')
    #print(line)
    for line in str_op2:
        line = line.strip()
        if re.match(r'("MX640GA|"MX320GA|"MX160GA)', line):
            op = re.search(r'"(\w+\-\d+\-\d+\-\d+\,\w+\-\d+\-\d+\-\d+)\::(\w+\=\w+\-\d+\-\d+\-\d+),(\w+=\w+)"',line)
            mxact=op.group(2)
            #print(mxact)
    ### Execute matrix switch command on active matrix ###
            if mxact == "ACTIVE=MX640GA-1-3-10" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX640GA-1-3-10;")
                print("\n---------------------------------------")
                print("         matrix switch started           ")
                print("---------------------------------------\n")
                print("\nWaiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("        matrix switch successful       ")
                print("---------------------------------------\n")
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
             
            elif mxact == "ACTIVE=MX320GA-1-3-10" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX320GA-1-3-10;")
                print("\n---------------------------------------")
                print("           matrix switch started         ")
                print("---------------------------------------\n")
                print("\nWaiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("        matrix switch successful       ")
                print("---------------------------------------\n")  
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
            
            elif mxact == "ACTIVE=MX160GA-1-3-10" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX160GA-1-3-10;")
                print("\n---------------------------------------")
                print("        matrix switch started.....     ")
                print("---------------------------------------\n")
                print("Waiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("        matrix switch successful       ")
                print("---------------------------------------\n") 
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
                                
            elif mxact == "ACTIVE=MX640GA-1-3-11" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX640GA-1-3-11;")
                print("\n---------------------------------------")
                print("        matrix switch started.....     ")
                print("---------------------------------------\n")
                print("Waiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("         matrix switch successful      ")
                print("---------------------------------------\n")
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
                
            elif mxact == "ACTIVE=MX320GA-1-3-11" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX320GA-1-3-11;")
                print("\n---------------------------------------")
                print("        matrix switch started.....     ")
                print("---------------------------------------\n")
                print("Waiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("         matrix switch successful      ")
                print("---------------------------------------\n")
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
#                 
            elif mxact == "ACTIVE=MX160GA-1-3-11" :
                print(line)
                print(mxact)
                tn.write(b"SW-DX-EQPT::MX160GA-1-3-11;")
                print("\n---------------------------------------")
                print("        matrix switch started.....     ")
                print("---------------------------------------\n")
                print("Waiting for matrix switch time about 15+ mins")
                time.sleep(600)
                tn.write(b"CANC-USER;")
                time.sleep(5)
                logTL()
                groupstate()
                tn.write(b"CANC-USER;")
                print("\n---------------------------------------")
                print("         matrix switch successful     ")
                print("---------------------------------------\n")
                print("\nActive Matrix before switch:",mxact)
                print("Active Matrix after switch :",mxact1)
                
            else:
                print("matrix switch not successful")
                        
    tn.write(b"CANC-USER;")

def mxswitch():
    
    if port==3083:
        #print("you are login into TL1 command mode")
        x= range(1,2)
        for i in x:
            logTL()
            mx_sw()
            #print ('number of times switch executed is : ',x)
            #print(i)
    
    elif port==23:
        print("you are login into FLC mode")
        logFLC()
    
    else:
        print("Please enter the correct port number")
        
    return tcPass4
#sys.stdout.close()
 
#mxswitch()   
