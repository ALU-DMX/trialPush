'''
Created on 25-Feb-2019

@author: vairavels
'''
import unittest
import time
import sys
import os
import os.path
import neInvent as NI
import tcEvpl as EV
import es64sw as ES
import mxsw as MX
 

 
if os.path.exists("C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt"):
    print("yes, found")
    os.remove('C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt')
    print("File removed")


class Test(unittest.TestCase):
   
    def test_1inventory(self):
        sys.stdout=open("C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt","a")
        print("Test Case - 1:\n")
        NI.neInventory() 
        self.assertEqual(NI.tcPass1, True) 
        sys.stdout.close()    
      
    def test_2evpl(self):
        sys.stdout=open("C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt","a")  
        print("Test Case - 2:\n")
        EV.evpl()      
        self.assertEqual(EV.tcPass2, True)   
        sys.stdout.close()    
         
    def test_3es64sw(self):   
        sys.stdout=open("C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt","a")  
        print("Test Case - 3:\n")
        ES.es64TC()
        self.assertEqual(ES.tcPass3, True)
        sys.stdout.close()  

    def test_4mxsw(self):   
        sys.stdout=open("C:\\Users\\vairavels\\Desktop\\1678_test_automation.txt","a")  
        print("Test Case - 4:\n")
        MX.mxswitch()
        self.assertEqual(MX.tcPass4, True)
        sys.stdout.close() 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()