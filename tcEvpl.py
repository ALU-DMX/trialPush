import py_compile
import cmd
import select
import socket
import sys
import time
import datetime
import os
import getopt
import re
from itertools import product

tcPass2 =1
#Save logs in a file 
######################
#sys.stdout=open("C:\\Users\\vairavels\\Desktop\\EVPL_VER4.txt","w")

####################################################### GLOBALS ########################################
host = '10.10.189.158'
port = 3083 # TL1 port
size = 65565

gbeSlot       =  15
es64Slot      =  17
fromXGEport   =  1
toXGEport     =  2
maxVcg        =  3
fromVcg       =  2
toVcg         =  fromVcg+maxVcg-1
maxMbr        =  3
fromEs64InPort  = 2
toEs64InPort    = fromEs64InPort+maxVcg-1
fromEs64OutPort = 130
toEs64OutPort   = fromEs64OutPort+maxVcg-1
vlanIdStart     = 500
etsFlow = 1
NoOfCC = maxVcg * maxMbr
#rollCC = 0
rollTupS = 0
rollTupE = 0

###########################################################################################
rtrv_vcg = b'RTRV-VCG::'
ent_vcg  = b'ENT-VCG::'

eslp = b'ESLP'
gbe10vcg = b'GBE10VCG'
eslpvcg = b'ESLPVCG'
gbe10 = b'GBE10'
gbe = b'GBE'
OC48 = b'OC48'

vcg_type = b'STS1'
es64sc = b'ES64SC'

sts1 = b'STS1'
sts3   = b'STS3'
sts3c = b'STS3C'
sts12c = b'STS12C'
sts48c = b'STS48C'
sts192c = b'STS192C'


##### STS1 USE########
eslpsts1 = b'ESLPSTS1'
gbests1 = b'GBESTS1'
gbe10sts1 = b'GBE10STS1'
OC3sts1 = b'OC3STS1'
OC12sts1 = b'OC12STS1'
OC48sts1 = b'OC48STS1'
OC192sts1 = b'OC192STS1'
oc48sts3c = b'OC48STS3C'
vcgsts1 = b'VCGSTS1'

###### STS3C USE #######
eslpsts3c = b'ESLPSTS3C'
gbests3c = b'GBESTS3C'
gbe10sts3c = b'GBE10STS3C'
OC3sts3c = b'OC3STS3C'
OC12sts3c = b'OC12STS3C'
OC48sts3c = b'OC48STS3C'
OC192sts3c = b'OC192STS3C'
VCGsts3c = b'VCGSTS3C'

###### STS12C USE #######
eslpsts12c = b'ESLPSTS12C'
OC12sts12c = b'OC12STS12C'
OC48sts12c = b'OC48STS12C'
OC192sts12c = b'OC192STS12C'

###### STS48C USE #######
OC48sts48c = b'OC48STS48C'
OC192sts48c = b'OC192STS48C'

###### STS192C USE #######
OC192sts192c = b'OC192STS192C'

#####States#####
################
pstIS  = b'IS'
pstOOS = b'OOS'
negotiationAuto = b'AUTO'
negotiationDisabled = b'DISABLED'
flowControlNoPause = b'NO-PAUSE'
flowControlAssymetricPause = b'ASYMMETRIC-PAUSE'
cmdmde = b"FRCD"

#ErrorCodes

SNVS = 1
IIAC = 2
ENFE = 3
PICC = 4
SARB = 5
SCSN = 6
EQWT = 7
IDNC = 8
IDNV = 9

#rollBack Commands
ent_oc48 = b'ENT_OC48'
ent_crs = b'ENT_CRS'
ent_sts1 = b'ENT_STS1'
ent_gbe10 = b'ENT_GBE10'
ent_vcg = b'ENT_VCG'
ent_eslpvcg = b'ENT_ESLPVCG'
ent_eslp = b'ENT_ESLP'

##GBE 
nopause = b'NO-PAUSE'

#===========================================
################# Functions ################
#===========================================

def CNTRL_VCPATH(input,aid,provmbr):
    #CNTRL-VCPATH::GBE10VCG-1-3-8-2-1::::PROVMBR=3
    cmd=b'CNTRL-VCPATH'
    provmbr = bytes (str(provmbr),"ascii")

    cmd = cmd+ b'::' + aid + b'::::PROVMBR=' + provmbr

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ENT_ESLP(input, aid):
    #ENT-ESLP::ESLP-1-3-17-10::::ESLPTYPE=VCG;
    cmd = b'ENT-ESLP'

    cmd = cmd + b'::' + aid + b'::::' + b'ESLPTYPE=VCG'   

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC
    
def RTRV_ESLP(input, aid):
    cmd = b'RTRV-ESLP'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def DLT_ESLP(input, aid):
    #DLT-ESLP::ESLP-1-3-17-10
    cmd = b'DLT-ESLP'
    cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ENT_VCG(input,aid,maxNbr,vcgType,vlanId):
    #ENT-VCG::GBE10VCG-1-3-8-2-2::::MAXMBR=3,VCGTYPE=STS1,VLANID=101,WANETHERTYPE=CVLAN:IS;
    cmd = b'ENT-VCG'
    maxNum = bytes(str(maxNbr), 'ascii') 
    vlan   = bytes(str(vlanId), 'ascii')
    
    if vlanId == 0:
        cmd = cmd + b'::' + aid + b'::::MAXMBR=' + maxNum + b',' + b'VCGTYPE=' + vcgType
    else:
        cmd = cmd + b'::' + aid + b'::::MAXMBR=' + maxNum + b',' + b'VCGTYPE=' + vcgType + b',' + b'VLANID =' + vlan 
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def RTRV_VCG(input, aid):
    cmd = b'RTRV-VCG'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ED_VCG(input,aid,lcas,maxmbr):
    #ED-VCG::GBE10VCG-1-3-8-2-2::::LCASENABLE=Y
    cmd = b'ED-VCG'
    lcs = bytes(str(lcas), "ascii")
    mxmbr = bytes (str(maxmbr), "ascii")

    cmd = cmd + b'::' +aid + b'::::'+ b'LCASENABLE=' + lcs + b',' + b'MAXMBR=' + mxmbr 
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def DLT_VCG(input,aid):    
    cmd = b'DLT-VCG::'
    cmd = cmd + aid 
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ENT_STS(input, type, aid):
    #ENT-STS1::OC48STS1-1-3-7-13-1-1;
    cmd = b'ENT-' + type
    
    cmd = cmd + b'::' + aid 
    
    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC
    
def DLT_STS(input,type, aid):
    #DLT-STS1::OC48STS1-1-3-5-15-1-2;
    cmd = b'DLT-' + type
    cmd = cmd + b'::' + aid 
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC
        
def RTRV_STS(input,type, aid):
    #RTRV-STS1::OC48STS1-1-3-5-15-1-2;
    cmd = b'RTRV-' + type
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ENT_CRS(input, type, fromAID, toAID):
    #ENT-CRS-STS1::OC48STS1-1-3-5-15-1-1,OC48STS1-1-1-5-16-1-1;
    cmd = b'ENT-CRS'
    cmd = cmd + b'-' + type

    cmd = cmd + b'::' + fromAID + b',' + toAID

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC
    
def DLT_CRS(input, type, fromAID, toAID):
    #ENT-CRS-STS1::OC48STS1-1-3-5-15-1-1,OC48STS1-1-1-5-16-1-1;
    cmd = b'DLT-CRS'
    cmd = cmd + b'-' + type

    cmd = cmd + b'::' + fromAID + b',' + toAID

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC
    
def RTRV_CRS(input, type, aid):
    cmd = b'RTRV-CRS'
    if type == 0:
        cmd = cmd + b'::ALL'        
    else:
        cmd = cmd + b'-' + type
        if aid == 0:
            cmd = cmd + b'::ALL'
        else:
            cmd = cmd + b'::' + aid

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC

def ENT_OC48(input, aid):
    cmd = b'ENT-OC48'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC

def ED_OC48(input, aid, cmdmde, pst):
    cmd = b'ED-OC48'

    cmd = cmd + b'::' + aid + b'::::' + b'CMDMDE=' + cmdmde + b':' + pst
                
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC
              
def RTRV_OC48(input, aid):
    cmd = b'RTRV-OC48'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def DLT_OC48(input, aid):
    cmd = b'DLT-OC48'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC

def ENT_GBE(input, aid):
    #ENT-GBE::GBE-1-3-5-16:::::IS
    cmd = b'ENT-GBE'

    cmd = cmd + b'::' + aid
              
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC   

def ENT_GBE10(input, aid):
    #ENT-GBE::GBE-1-3-5-16:::::IS
    cmd = b'ENT-GBE10'

    cmd = cmd + b'::' + aid           
  
    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input, counter, 1, cmd)
    return rC

def ED_GBE(input,aid,negotn,flowctrl):
    #ED-GBE::GBE-1-3-12-1::::NEGOTN=DISABLED;
    #ED-GBE::GBE-1-3-12-1::::FLOWCONT=NO-PAUSE;
    cmd1 = b'ED-GBE'

    if negotn == negotiationDisabled :        
        cmd = cmd1 + b'::' + aid + b'::::' + b'NEGOTN=' + negotn  
        counter = launchCommand(input,1,cmd)
        rC = mainLoop(input,counter,1,cmd)
        return rC

        cmd = cmd1 + b'::' + aid + b'::::' + b'FLOWCONT='+flowctrl
        counter = launchCommand(input,1,cmd)
        rC = mainLoop(input,counter,1,cmd)
        return rC
    else:
        cmd = cmd1 + b'::' + aid + b'::::' + b'NEGOTN=' + negotn
        counter = launchCommand(input,1,cmd)
        rC = mainLoop(input,counter,1,cmd)
        return rC
  
def RTRV_GBE(input, aid):
    cmd = b'RTRV-GBE'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC
    
def RTRV_GBE10(input, aid):
    cmd = b'RTRV-GBE10'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input, 1, cmd)
    rC = mainLoop(input,counter, 1, cmd)
    return rC

def ED_GBE10(input,aid,flowcont,mxvcg):
    #ED-GBE10::GBE10-1-3-4-1::::FLOWCONT=ASYMMETRIC-PAUSE,MAXVCG=7;
    cmd = b'ED-GBE10'
    maxvcg = bytes(str(mxvcg), 'ascii') 
    flowcont = bytes(str(flowcont), 'ascii')    

    cmd = cmd + b'::' + aid + b'::::'+ b'FLOWCONT=' + flowcont + b',' + b'MAXVCG=' + maxvcg    

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC
  
def DLT_GBE(input, aid):
    #ENT-GBE::GBE-1-3-5-16:::::IS
    cmd = b'DLT-GBE'

    cmd = cmd + b'::' + aid
              
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC 

def DLT_GBE10(input, aid):
    #ENT-GBE::GBE-1-3-5-16:::::IS
    cmd = b'DLT-GBE10'

    cmd = cmd + b'::' + aid
    
    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC    

def RTRV_EQPT(input, aid):
    cmd = b'RTRV-EQPT'
    if aid == 0:
        cmd = cmd + b'::ALL'
    else:
        cmd = cmd + b'::' + aid

    counter = launchCommand(input,1,cmd)
    rC = mainLoop(input,counter,1,cmd)
    return rC
  
def connect(host,port,isES64):
    #connect to server
    s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_conn.connect((host, port))
    #setup the input list: socket and keyboard
    input = [s_conn]
    #read any hello messages from the server:
    data = s_conn.recv(size)
    print(data)

    #==========================================================
    # TL1 authentification phase:
    # we will send the command: "ACT-USER::EML001:::Geheim000;" 
    # to the TL1 server
    #sys.stdout.write("trying to authenthicate to TL1 server")
    #tl1_auth_cmd = b'ACT-USER::ALCATEL:::Ansi_4GX1;'
    #==========================================================
    if isES64 == 0:
        tl1_auth_cmd = b'ACT-USER::user6:::Ansi_svt6;'
    else:
        tl1_auth_cmd = b'ACT-USER::user5:::Ansi_svt5;'
    s_conn.send(tl1_auth_cmd)
    for i in range (1, 3):
        inputready, outputready, exceptready = select.select(input, [], [])
        for s in inputready:
            if s == s_conn:
                #sys.stdout.write('# ')
                # read the socket:
                data = s_conn.recv(size)
                print(data)

    return input

def increaseCounter(data, counter, cmd):
    start=0
    end=len(data)

    if (data.find(b'\\x08', 0, end) == -1):
        if (data.find(b';', 0, end) == -1) :
            return counter


    # search for COMPLDs
    start = data.find(cmd, 0, end)
               
    while(start != -1):
        counter = counter + 1
        start   = data.find(cmd, start + 1, end)

    # search for DENYs
    start = data.find(b'DENY', 0, end)
               
    while(start != -1):
        counter = counter + 1                     
        start   = data.find(b'DENY', start + 1, end)    
                  
    return counter

def launchCommand(input, times, cmd):
    s_conn = input[0]
    counter = 0
                            
    cmd = cmd + b';'
    s_conn.send(cmd)
    return counter
    
def launchCommandES64(input, times, cmd):
    s_conn = input[0]
    counter = 0    
    cmd = cmd + b'\r'
    s_conn.send(cmd)                           
    return counter
    
def mainLoop(input, counter, totalCmds, cmd):
    s_conn = input[0]
    running = 1
    while running:
        if (counter == totalCmds):
            running = 0
            break
        inputready, outputready, exceptready = select.select(input, [], [])
        for s in inputready:
            if s == s_conn:
                # read the socket:
                data = s_conn.recv(size)                
                            
                print(data.decode('ascii'))

                counter = increaseCounter(data, counter, cmd)

                end = len(data)
                if data.find(b'DENY', 0, end):
                    Data = data.decode('ascii')
                    Data = Data.split('\n')                    
                    for line in Data:
                        line = line.strip()
                        if re.match('ENFE', line):
                            print ("\n ***Equipage, Feature Not provided ***")
                            return ENFE;
                        elif re.match('PICC', line):
                            print ("\n*** Privilege, Invalid Command Code ***")
                            return PICC;
                        elif re.match('SARB', line):
                            print ("\n*** System, All Resources Busy ***")
                            return SARB;
                        elif re.match('SCSN', line):
                            print ("\n*** Status, invalid Command SequeNce ***")
                            return SCSN;                        
                        elif re.match('EQWT', line):
                            print ("\n*** Equipage, Wrong Type ***")
                            return EQWT;
                        elif re.match('IDNC', line):
                            print ("\n*** Input, Data Not Consistent ***")
                            return IDNC;
                        elif re.match('IDNV', line):
                            print ("\n*** Input, Data Not Valid ***")
                            return IDNV;                        
                        elif re.match('SNVS', line):
                            print ("\n*** Status, Not in Valid State ***")
                            return SNVS;
                        elif re.match('PIUI', line):
                            print ("\n*** Privilege, Illegal User Identity ***")
                        elif re.match('IIAC', line):
                            return IIAC;
                        elif re.match('Cli', line):
                            return                           
                        else:
                            continue
                            ### print ("\n*** secondary state: DSBLD ***")
                           
        #=======================================================================
        # if (counter >= totalCmds):
        #     running = 0
        #     return counter
        #=======================================================================
    return 0;
  
def createAID(type,rackNo,subRackNo,SlotNo,portNo,augNo,stsNo):
    
    rack = bytes(str(rackNo),"ascii")
    subrack = bytes(str(subRackNo), "ascii")
    slot = bytes(str(SlotNo), "ascii")
    port = bytes(str(portNo), "ascii")
    aug = bytes(str(augNo), 'ascii')
    sts = bytes(str(stsNo), 'ascii')
    
    cmd = type + b'-' + rack + b'-' + subrack + b'-' + slot + b'-' + port
    
    if augNo > 0:
            cmd = cmd + b'-' + aug
    if stsNo > 0:
            cmd = cmd + b'-' + sts
            
    return cmd

def createAIDES64(type,rackNo,subRackNo,SlotNo,portNo,augNo,stsNo):
    
    rack = bytes(str(rackNo),"ascii")
    subrack = bytes(str(subRackNo), "ascii")
    slot = bytes(str(SlotNo), "ascii")
    port = bytes(str(portNo), "ascii")
    aug = bytes(str(augNo), 'ascii')
    sts = bytes(str(stsNo), 'ascii')
    
    cmd = type + b'-' + rack + b'-'+ subrack + b'-'+ slot

    if portNo > 0:
        cmd = cmd + b'-' + port    
    if augNo > 0:
            cmd = cmd + b'-' + aug
    if stsNo > 0:
            cmd = cmd + b'-' + sts   
    return cmd

def createAIDtup(tup,rackNo,subRackNo,SlotNo,portNo,augNo,stsNo):
    
    rack = bytes(str(rackNo),"ascii")
    subrack = bytes(str(subRackNo), "ascii")
    slot = bytes(str(SlotNo), "ascii")
    port = bytes(str(portNo), "ascii")
    aug = bytes(str(augNo), 'ascii')
    sts = bytes(str(stsNo), 'ascii')
    
    cmd = type + b'-' + rack + b'-' + subrack + b'-' + slot + b'-' + port
    
    if augNo > 0:
            cmd = cmd + b'-' + aug
    if stsNo > 0:
            cmd = cmd + b'-' + sts
            
    return cmd

def ES64SC(inputes64, aid):
    cmd = b'ACT-CLI'
    cmd = cmd + b'::' + aid 
    #print(cmd)
    counter = launchCommand(inputes64, 1, cmd)
    mainLoop(inputes64, counter, 1, cmd)
    
def interfaceEs64(input, x, y):                               
    x = str(x)
    y = str(y)
    x = x.encode('utf-8')
    y = y.encode('utf-8')
    
    cmd = b'interface position  p' + x + b'-' + y + b' remoteeth activate'
    print(cmd)
    counter = launchCommandES64(input, 1, cmd)
    mainLoop(input, counter, 1, cmd)
    
    cmd = b'interface position p'+ x+ b'-'+ y+ b' remoteeth ratelimited 150000'
    counter = launchCommandES64(input, 1, cmd)
    mainLoop(input, counter, 1, cmd)

def trafficdescriptor(input, a, cir, pir):
    a = str(a)
    cir = str(cir)
    pir = str(pir)
    a = a.encode('utf-8')
    cir = cir.encode('utf-8')
    pir = pir.encode('utf-8')
    cmd = b'trafficdescriptor activate'+ b' '+ a + b' '+ b'traffictype gua cir'  + b' '+ cir + b' ' + b'cbs 2048 pir'+b' '+ pir + b' ' + b'pbs 2048'
                                                             
    print(cmd)
    counter = launchCommandES64(input, 1, cmd)
    mainLoop(input, counter, 1, cmd)

def deletetrafficdescriptor(input, a):
    a = str(a)
    a = a.encode('utf-8')
    cmd = b'trafficdescriptor delete' + b' ' + a                                  
               
    counter = launchCommandES64(input, 1, cmd)
    mainLoop(input, counter, 1, cmd)
                           
def etsflow(input, trafficdescriptorName, port1, port2, etsflow, vlan, incr):
    port1 = list(range(port1, port1+incr))
    port2 = list(range(port2, port2+incr))
    etsflow = list(range(etsflow, etsflow+incr))
    vlan = list(range(vlan,vlan+incr))
    trafficdescriptorName = str(trafficdescriptorName)
    trafficdescriptorName = trafficdescriptorName.encode('utf-8')
   
    for i, j, k, l in zip(port1, port2, etsflow, vlan):
                      

        i = str(i)
        i = bytes(str(i), 'utf-8')
        j = bytes(str(j), 'utf-8')
        k = bytes(str(k), 'utf-8')
        l = bytes(str(l), 'utf-8')       
                                                                      
        
        cmd = b'etsflowunidir activate forw'+ k + b' '+ b'port1 p'+ i + b' '+ b'port2 p' + j + b' '+ b'inflowclassifier vlan'+ b' ' + l + b' '+ b'pri dontcare trafficdescriptor'+ b' '+ trafficdescriptorName
        counter = launchCommandES64(input, 1, cmd)
        mainLoop(input, counter, 1, cmd)

        cmd = b'etsflowunidir activate back'+ k + b' '+ b'port1 p'+ j + b' '+ b'port2 p' + i + b' '+ b'inflowclassifier vlan'+ b' ' + l + b' '+ b'pri dontcare trafficdescriptor'+ b' '+ trafficdescriptorName
        counter = launchCommandES64(input, 1, cmd)
        mainLoop(input, counter, 1, cmd)
        
def deleteEtsflow(input, etsflow, incr):
    for k in range(etsflow, incr):
        k = str(k)
        k = k.encode('utf-8')

        cmd = b'etsflowunidir delete forw'+ k
        counter = launchCommandES64(input, 1, cmd)
        mainLoop(input, counter, 1, cmd)

        cmd = b'etsflowunidir delete back'+ k 
        counter = launchCommandES64(input, 1, cmd)
        mainLoop(input, counter, 1, cmd)
        
def logout(input):
    cmd = b'logout'
    counter = launchCommandES64(input, 1, cmd)
    mainLoop(input, counter, 1, cmd)        
                                                 
def canceluser(input):
    cmd = b'CANC-USER'
    counter = launchCommand(input, 1, cmd)
    mainLoop(input, counter, 1, cmd) 

def cleanUp(input):
    tupS =  ()
    tupE = ()     

    tupS = (ent_gbe10, 1, 3, gbeSlot, fromXGEport, 0, 0) + tupS
    tupE = (ent_gbe10, 1, 3, gbeSlot, toXGEport+1, 0, 0) + tupE   
    tupS = (ent_vcg, 1, 3, gbeSlot, fromXGEport, fromVcg, 0) + tupS
    tupE = (ent_vcg, 1, 3, gbeSlot, toXGEport+1, toVcg+1, 0) + tupE     
    tupS = (ent_eslp, 1, 3, es64Slot, fromEs64InPort, 0, 0) + tupS
    tupE = (ent_eslp, 1, 3, es64Slot, toEs64InPort+1, 0, 0) + tupE        
    tupS = (ent_eslp, 1, 3, es64Slot, fromEs64OutPort, 0, 0) + tupS
    tupE = (ent_eslp, 1, 3, es64Slot, toEs64OutPort+1, 0, 0) + tupE          
    tupS = (ent_eslpvcg, 1, 3, es64Slot, fromEs64InPort, 0, 0) + tupS
    tupE = (ent_eslpvcg, 1, 3, es64Slot, toEs64InPort+1, 0, 0) + tupE  
    tupS = (ent_eslpvcg, 1, 3, es64Slot, fromEs64OutPort, 0, 0) + tupS
    tupE = (ent_eslpvcg, 1, 3, es64Slot, toEs64OutPort+1, 0, 0) + tupE       
    tupS = (ent_crs, 1, 3, gbeSlot, fromXGEport, fromVcg, 1) + tupS
    tupE = (ent_crs, 1, 3, gbeSlot, fromXGEport, toVcg, maxMbr) + tupE
    tupS = (ent_crs, 1, 3, es64Slot, fromEs64InPort, 1, 0) + tupS
    tupE = (ent_crs, 1, 3, es64Slot, toEs64InPort, maxMbr, 0) + tupE                    
    tupS = (ent_crs, 1, 3, es64Slot, fromEs64OutPort, 1, 0) + tupS
    tupE = (ent_crs, 1, 3, es64Slot, toEs64OutPort, maxMbr, 0) + tupE      
    tupS = (ent_crs, 1, 3, gbeSlot, toXGEport, fromVcg, 1) + tupS
    tupE = (ent_crs, 1, 3, gbeSlot, toXGEport, toVcg, maxMbr) + tupE           
          
    rollBack(input, tupS, tupE)

def rollBack(input,tup1,tup2):
    print("*********** ROLLBACK CALLED *************")
    lenTup = len(tup1)
    i = 0
    while i < lenTup:
        print("length = ",lenTup)
                                                 
        if tup1[i] == b'ENT_OC48':
            print("delete oc48")
                                         
            for k in range(tup1[i+4], tup2[i+4]):
                OC48_AID = createAID(OC48, 1, 3, 7, k, 0, 0)
                RTRV_OC48(input, OC48_AID)
                DLT_OC48(input, OC48_AID)
                print(OC48_AID)
                             
        elif tup1[i] == b'ENT_STS1':
            print("delete STS1",tup2[i+5])
                             
            portS = tup1[i+4]
            portE = tup2[i+4]
            AuS   = tup1[i+5]
            AuE   = tup2[i+5]
            stsS  = tup1[i+6]
            stsE  = tup2[i+6]
            for a,b,c in product(range(portS, portE), range(AuS, AuE), range(stsS, stsE)):
            #for a,b,c in product(range(10,17), range(1,17), range(1,4)):
                OC48_AID = createAID(OC48sts1, 1, 3, 7, a, b, c)
                print(OC48_AID)
                RTRV_STS(input, sts1, OC48_AID)
                DLT_STS(input, sts1, OC48_AID)
        elif tup1[i] == b'ENT_GBE10':
            print("delete GBE10")
            portS = tup1[i+4]
            portE = tup2[i+4]

            for a in range(portS, portE):
            #for a,b,c in product(range(10,17), range(1,17), range(1,4)):
                aid   = createAID(gbe10, 1, 3, gbeSlot, a, 0, 0)
                print(aid)
                RTRV_GBE10(input, aid)
                DLT_GBE10(input, aid)

        elif tup1[i] == b'ENT_VCG':
            print("delete GBE10VCG")
                             
            portS = tup1[i+4]
            portE = tup2[i+4]
            vcgS  = tup1[i+5]
            vcgE  = tup2[i+5]
            for a,b in product(range(portS, portE), range(vcgS, vcgE)):
            #for a,b,c in product(range(10,17), range(1,17), range(1,4)):
                aid   = createAID(gbe10vcg, 1, 3, gbeSlot, a, b, 0)
                print(aid)
                RTRV_VCG(input, aid)
                DLT_VCG(input, aid)
                
        elif tup1[i] == b'ENT_ESLP':
          
            print("delete ESLP")
            portS = tup1[i+4]
            portE = tup2[i+4]

            for a in range(portS, portE):
                        
                aid   = createAID(eslp, 1, 3, es64Slot, a, 0, 0)
                print(aid)
                RTRV_ESLP(input, aid)
                DLT_ESLP(input, aid)        

        elif tup1[i] == b'ENT_ESLPVCG':
            print("delete ESLPVCG")
            vcgS = tup1[i+4]
            vcgE = tup2[i+4]
            
            for a in range(vcgS, vcgE):
                aid   = createAID(eslpvcg, 1, 3, es64Slot, a, 0, 0)
                print(aid)
                RTRV_VCG(input, aid)
                DLT_VCG(input, aid)
                
        elif tup1[i] == b'ENT_CRS':
            print("delete CRS")

            if tup1[i+3] == es64Slot:
                esVcgS = tup1[i+4]
                gbeVcgS = tup1[i+12]
                esVcgE = tup2[i+4]
                gbeVcgE = tup2[i+12]
                esStsE = tup2[i+5]               
                           
                for (a,b),c in product((zip(range(esVcgS, esVcgE+1), range(gbeVcgS, gbeVcgE+1))), range(1, maxMbr+1)):
                    if a == esVcgE and c == esStsE+1:
                        break                
                    from_AID   = createAID(vcgsts1, 1, 3, es64Slot, a, c, 0)
                    to_AID = createAID(gbe10sts1, 1, 3, gbeSlot, fromXGEport, b, c)
                    print(from_AID, to_AID)             
                    DLT_CRS(input, sts1, from_AID, to_AID)
         
            if tup1[i+3] == gbeSlot:
                gbeVcgS = tup1[i+5]
                esVcgS = tup1[i+11]
                gbeVcgE = tup2[i+5]
                esVcgE = tup2[i+11]
                gbeStsE = tup2[i+6]
                 
                for (a,b),c in product((zip(range(gbeVcgS, gbeVcgE+1), range(esVcgS, esVcgE+1))), range(1, maxMbr+1)):
                    if a == gbeVcgE and c == gbeStsE+1:
                        break                
                    from_AID = createAID(gbe10sts1, 1, 3, gbeSlot, toXGEport, a, c)
                    to_AID   = createAID(vcgsts1, 1, 3, es64Slot, b, c, 0)
                    print(from_AID, to_AID)             
                    DLT_CRS(input, sts1, from_AID, to_AID)
                    
        if tup1[i] == b'ENT_CRS':
            i = i + 14
        else:
            i = i + 7                        
 
def evpl():

    tupS = ()
    tupE = ()   

    print("\n*** Logging in to CLI interface for ES64 configuration!! ***")
    inputes64 = connect(host, port, 1)
 
    es64Aid = createAIDES64(es64sc, 1, 3, es64Slot, 0, 0, 0)
    ES64SC(inputes64, es64Aid)

    # Create ES64 interface ingress to egress ports        
    interfaceEs64(inputes64, fromEs64InPort, toEs64InPort+1)
    interfaceEs64(inputes64, fromEs64OutPort, toEs64OutPort+1)
 
    # Trafficdescriptor inflow and outlows ###
    trafficdescriptor(inputes64, 'Line', 1000000, 1000000)
 
    # Input format for etsflow creation
    # (input, trafficdescriptorName, port1, port2, etsflow,  vlan , range )  
    etsflow(inputes64, 'Line', fromEs64InPort, fromEs64OutPort, etsFlow, vlanIdStart+fromVcg, maxVcg)
    logout(inputes64)

    print("\n*** Connecting to the NE!! ***")           
    input = connect(host, port, 0)

    #Create GBE Facility
    for i in range(fromXGEport, toXGEport+1):
        start = 1
        aid = createAID(gbe10, 1, 3, gbeSlot, i, 0, 0)
        print(aid)
        returnCode = ENT_GBE10(input, aid)
        print(returnCode)
        if returnCode != 0: 
            tupS = (ent_gbe10, 1, 3, gbeSlot, start, 0, 0) + tupS
            tupE = (ent_gbe10, 1, 3, gbeSlot, i, 0, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_gbe10, 1, 3, gbeSlot, start, 0, 0) + tupS
    tupE = (ent_gbe10, 1, 3, gbeSlot, i+1, 0, 0) + tupE          
    print(tupS,tupE)       
       
    #Change FLOWCONT on GBE Facility to NO-PAUSE
    for i in range(fromXGEport, toXGEport+1):
        start = 1
        aid = createAID(gbe10, 1, 3, gbeSlot, i, 0, 0)
        print(aid)
        returnCode = ED_GBE10(input, aid,"NO-PAUSE",maxVcg)
        
    #Create GBE10VCG Facility
    for i,j in product(range(fromXGEport, toXGEport+1), range(fromVcg, toVcg+1)):
        start1 = 1
        start2 = 2
        aid = createAID(gbe10vcg, 1, 3, gbeSlot, i, j, 0)
        print(aid)
        returnCode = ENT_VCG(input, aid, 3, sts1, vlanIdStart+j)
        if returnCode != 0: 
            tupS = (ent_vcg, 1, 3, gbeSlot, start1, start2, 0) + tupS
            tupE = (ent_vcg, 1, 3, gbeSlot, i+1, j+1, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_vcg, 1, 3, gbeSlot, start1, start2, 0) + tupS
    tupE = (ent_vcg, 1, 3, gbeSlot, i+1, j+1, 0) + tupE          
    print(tupS,tupE)    
            
            
    ##LCAS Enable on VCG
    for i,j in product(range(fromXGEport, toXGEport+1), range(fromVcg, toVcg+1)):
        start1 = 1
        start2 = 2
        aid = createAID(gbe10vcg, 1, 3, gbeSlot, i, j, 0)
        print(aid)
        returnCode = ED_VCG(input, aid, "Y", maxMbr)
     
    #Create ESLP IN Facility
    for i in range(fromEs64InPort, toEs64InPort+1):
        start = 1
        aid = createAID(eslp, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ENT_ESLP(input, aid)
        if returnCode != 0: 
            tupS = (ent_eslp, 1, 3, es64Slot, start, 0, 0) + tupS
            tupE = (ent_eslp, 1, 3, es64Slot, i, 0, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_eslp, 1, 3, es64Slot, start, 0, 0) + tupS
    tupE = (ent_eslp, 1, 3, es64Slot, i+1, 0, 0) + tupE          
    print(tupS,tupE)       
        
    #Create ESLP OUT Facility
    for i in range(fromEs64OutPort, toEs64OutPort+1):
        start = 1
        aid = createAID(eslp, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ENT_ESLP(input, aid)
        if returnCode != 0: 
            tupS = (ent_eslp, 1, 3, es64Slot, start, 0, 0) + tupS
            tupE = (ent_eslp, 1, 3, es64Slot, i, 0, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_eslp, 1, 3, es64Slot, start, 0, 0) + tupS
    tupE = (ent_eslp, 1, 3, es64Slot, i+1, 0, 0) + tupE          
    print(tupS,tupE)       
      
       
    #Create ESLPVCG Facility
    for i in range(fromEs64InPort, toEs64InPort+1):
        start1 = 2
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ENT_VCG(input, aid, 3, sts1, 0)
        if returnCode != 0: 
            tupS = (ent_eslpvcg, 1, 3, es64Slot, start1, 0, 0) + tupS
            tupE = (ent_eslpvcg, 1, 3, es64Slot, i+1, 0, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_eslpvcg, 1, 3, es64Slot, start1, 0, 0) + tupS
    tupE = (ent_eslpvcg, 1, 3, es64Slot, i+1, 0, 0) + tupE          
    print(tupS,tupE)    
       
    #Create ESLPVCG Facility
    #for i in range(130,192):
    for i in range(fromEs64OutPort, toEs64OutPort+1):
        start1 = 130
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ENT_VCG(input, aid, 3, sts1, 0)
        if returnCode != 0: 
            tupS = (ent_eslpvcg, 1, 3, es64Slot, start1, 0, 0) + tupS
            tupE = (ent_eslpvcg, 1, 3, es64Slot, i+1, 0, 0) + tupE
            print(tupS,tupE)            
            rollBack(input, tupS, tupE)
            return;
    tupS = (ent_eslpvcg, 1, 3, es64Slot, start1, 0, 0) + tupS
    tupE = (ent_eslpvcg, 1, 3, es64Slot, i+1, 0, 0) + tupE          
    print(tupS,tupE)                         
                         
    ##LCAS Enable on ESLPVCG
    for i in range(fromEs64InPort, toEs64InPort+1):
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ED_VCG(input, aid, "Y", maxMbr)
        
    ##LCAS Enable on ESLPVCG
    for i in range(fromEs64OutPort, toEs64OutPort+1):
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = ED_VCG(input, aid, "Y", maxMbr)
     
    ##PROVMBR  on ESLPVCG
    for i in range(fromEs64InPort, toEs64InPort+1):
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = CNTRL_VCPATH(input, aid, maxMbr)
            
    ##PROVMBR  on ESLPVCG
    for i in range(fromEs64OutPort, toEs64OutPort+1):
        aid = createAID(eslpvcg, 1, 3, es64Slot, i, 0, 0)
        print(aid)
        returnCode = CNTRL_VCPATH(input, aid, maxMbr)
     
    ##PROVMBR  on GBE10VCG
    for i,j in product(range(fromXGEport, toXGEport+1), range(fromVcg, toVcg+1)):
        aid = createAID(gbe10vcg, 1, 3, gbeSlot, i, j, 0)
        print(aid)
        returnCode = CNTRL_VCPATH(input, aid, maxMbr)
     
    ######## create STS1 crossconnections from ESLP VCG to GBE10 VCG #################################    
    for i,j in product(range(fromVcg, toVcg+1), range(1, maxMbr+1)):        
        geStart1 = 1
        geStart2 = 2
        geStart3 = 1
        esStart1 = 2
        esStart2 = 1        
        fromAID = createAID(vcgsts1, 1, 3, es64Slot, i, j, 0)
        toAID = createAID(gbe10sts1, 1, 3, gbeSlot, fromXGEport, i, j)
        print(fromAID,toAID)        
        returnCode = ENT_CRS(input, sts1, fromAID, toAID)
             
        if returnCode != 0: 
            tupS = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2, geStart3) + tupS
            tupE = (ent_crs, 1, 3, gbeSlot, geStart1, i, j) + tupE
            tupS = (ent_crs, 1, 3, es64Slot, esStart1, esStart2, 0) + tupS
            tupE = (ent_crs, 1, 3, es64Slot, i, j, 0) + tupE  
            print(tupS,tupE)
                  
            rollBack(input, tupS, tupE)              
            return;
              
    tupS = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2, geStart3) + tupS
    tupE = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2+maxVcg-1, geStart3+2) + tupE
    tupS = (ent_crs, 1, 3, es64Slot, esStart1, esStart2, 0) + tupS
    tupE = (ent_crs, 1, 3, es64Slot, esStart1+maxVcg-1, esStart2+2, 0) + tupE                    
                  
    print(tupS,tupE)
      
    ######## create STS1 crossconnections from GBE10 VCG to ESLP VCG ############################
    for (i,j),k in product(zip(range(fromVcg, toVcg+1), range(fromEs64OutPort, toEs64OutPort+1)), range(1, maxMbr+1)):        
        geStart1 = 2
        geStart2 = 2
        geStart3 = 1
        esStart1 = 130
        esStart2 = 1
        fromAID = createAID(gbe10sts1, 1, 3, gbeSlot, toXGEport, i, k)
        toAID = createAID(vcgsts1, 1, 3, es64Slot, j, k, 0)        
        print(fromAID,toAID)        
        returnCode = ENT_CRS(input, sts1, fromAID, toAID)
           
        if returnCode != 0:
            tupS = (ent_crs, 1, 3, es64Slot, esStart1, esStart2, 0) + tupS
            tupE = (ent_crs, 1, 3, es64Slot, j, k, 0) + tupE  
            tupS = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2, geStart3) + tupS
            tupE = (ent_crs, 1, 3, gbeSlot, geStart1, i, k) + tupE
      
            print(tupS,tupE)
                  
            rollBack(input, tupS, tupE)              
            return;
      
    tupS = (ent_crs, 1, 3, es64Slot, esStart1, esStart2, 0) + tupS
    tupE = (ent_crs, 1, 3, es64Slot, esStart1+maxVcg-1, esStart2+2, 0) + tupE      
    tupS = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2, geStart3) + tupS
    tupE = (ent_crs, 1, 3, gbeSlot, geStart1, geStart2+maxVcg-1, geStart3+2) + tupE
      
    print(tupS,tupE)
     
    print ("\nTraffic flow for 30 seconds...! Please wait...!")
    time.sleep(30)
    
    # Delete the ES64 flows
    print ("\nClean up ES64 configs...")
    ES64SC(inputes64, es64Aid)
    deleteEtsflow(inputes64, etsFlow, maxVcg+1)
    deletetrafficdescriptor(inputes64, 'Line')
    logout(inputes64)
  
    print ("\nStarting cleanup...")
    cleanUp(input)
 
    print ("\n Logging out!!")
    canceluser(input)
    
    return tcPass2
   
#evpl()
#sys.stdout.close()
