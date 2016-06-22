from client import webBus
import QIELib
import IglooLib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib
i = IglooLib


class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logfile #changed from logstream to logfile
        self.iterations = iterations
    def run(self):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody() == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
    def log(self, message):
        logprint(message, file=self.logfile)
    def testBody(self):
        return True

# ------------------------------------------------------------------------
class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMajVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaMinVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMinVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ones(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ones"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class zeroes(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "zeroes"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaTopOrBottom(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaTopOrBottom"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class uniqueID(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "uniqueID"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statusReg(Test): #inherit from Test class, overload testBody() function
    # -------------------------------------------

    def read(self, desiredReg = "all"):
        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister(b, i.iglooAdd, reg, size)
        #print "allRegList: ", allRegList

        # if bad read
        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        statusReg = {
            "InputSpyWordNum"   :   allRegStr[0:10], # number of words in InputSpyFifo (depth = 512)
            "InputSpyFifoEmpty" :   allRegStr[10],
            "InputSpyFifoFull"  :   allRegStr[11],
            "Qie_DLLNoLock"     :   allRegStr[12:24], # good when '0'
            "BRIDGE_SPARE"      :   allRegStr[24:30],
            "1_bit"             :   allRegStr[30], # should be '0'
            "PLL_320MHz_Lock"   :   allRegStr[31] # good when '1'
                }

        allReg = statusReg["InputSpyWordNum"] + " : " + statusReg["InputSpyFifoEmpty"]\
            + " : " + statusReg["InputSpyFifoFull"] + " : " + statusReg["Qie_DLLNoLock"]\
            + " : " + statusReg["BRIDGE_SPARE"] + " : " + statusReg["1_bit"]\
            + " : " + statusReg["PLL_320MHz_Lock"]

        if desiredReg == "all":
            return allReg

        else:
            return statusReg[desiredReg]

    # -------------------------------------------
    def testBody(self):
        readPass = False
        rwrPass = False

        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        print self.read()

        if self.read() !=False:
            readPass = True

        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class cntrRegDisplay(Test): #inherit from Test class, overload testBody() function
    # -------------------------------------------
    def read(self, desiredReg = "all"):
        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister(b, i.iglooAdd, reg, size)
        #print "allRegList: ", allRegList

        # if bad read
        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        cntrReg = {
        "31bX"             :   allRegStr[0:26],
        "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
        "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
        "2_bit_0"           :   allRegStr[28:30],
        "WrEn_InputSpy"     :   allRegStr[30:31],
        "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            }

        allReg = "31bx: " + cntrReg["31bX"] + '\n'\
             + "orbitHisto_clear: " + cntrReg["orbitHisto_clear"] + '\n'\
             + "orbitHisto_run: " + cntrReg["orbitHisto_run"] + '\n'\
             + "2_bit_0: " + cntrReg["2_bit_0"] + '\n'\
             + "WrEn_InputSpy: " + cntrReg["WrEn_InputSpy"] + '\n'\
             + "CI_mode: " + cntrReg["CI_mode"]

        # another option for readout instead of allReg is simply cntrReg (prints list)
        if desiredReg == "all":
            return allReg

        else:
            return cntrReg[desiredReg]
    {
    # -------------------------------------------
    # def write(self, desiredReg, settingList):
    #     name = "cntrReg"
    #     reg = i.igloo[name]["register"]
    #     size = i.igloo[name]["size"] / 8
    #
    #     # READ FIRST
    #     read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
    #
    #     if (read1 == False): return False
    #
    #     #makes read1 (byte list) into a bit string
    #     allRegStr = ''.join(i.catBitsFromBytes(i.getBitsFromBytes(read1)))
    #
    #     settingStr = ''.join(settingList)
    #     toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
    #
    #     # WRITE, THEN READ AGAIN TO SEE CHANGES
    #     if desiredReg == "all":
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 =i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'if': WRITE1/READ2 ERROR"
    #             return False
    #
    #     else:
    #         cntrReg = {
    #         "31bX"             :   allRegStr[0:6],
    #         "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
    #         "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
    #         "2_bit_0"           :   allRegStr[18:20],
    #         "WrEn_InputSpy"     :   allRegStr[20:26],
    #         "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
    #             }
    #
    #         cntrReg[desiredReg] = settingStr
    #
    #         toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'else': WRITE1/READ2 ERROR"
    #             return False
    }
    # packed away: old interactive write() function
    {
    # -------------------------------------------
    # in theory, you can make string parameter settingList = ['000000', '11', '001001', etc]"
    # and it will join the elements and assign them to appropriate settings
    # in cntrReg...
    # def write(self, desiredReg, settingList):
    #     name = "cntrReg"
    #     reg = i.igloo[name]["register"]
    #     size = i.igloo[name]["size"] / 8
    #
    #     # READ FIRST
    #     read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
    #
    #     if (read1 == False): return False
    #
    #     #makes read1 (byte list) into a bit string
    #     allRegStr = ''.join(i.catBitsFromBytes(i.getBitsFromBytes(read1)))
    #
    #     settingStr = ''.join(settingList)
    #     toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
    #
    #     # WRITE, THEN READ AGAIN TO SEE CHANGES
    #     if desiredReg == "all":
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 =i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'if': WRITE1/READ2 ERROR"
    #             return False
    #
    #     else:
    #         cntrReg = {
    #         "31bX"             :   allRegStr[0:6],
    #         "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
    #         "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
    #         "2_bit_0"           :   allRegStr[18:20],
    #         "WrEn_InputSpy"     :   allRegStr[20:26],
    #         "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
    #             }
    #
    #         cntrReg[desiredReg] = settingStr
    #
    #         toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'else': WRITE1/READ2 ERROR"
    #             return False
    }

    # -------------------------------------------
    def testBody(self):
        readPass = False
        rwrPass = False

        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s Display----------" %name
        print self.read()

        if self.read() !=False:
            readPass = True

        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            return True
        else:
            return False

        # desiredReg = raw_input("Enter cntrReg name (enter=all, 'more'=ShowNames): ")
        # if desiredReg == '': desiredReg = 'all'
        # elif desiredReg == 'more':
        #     print "31bX, " + "orbitHisto_clear, " + "orbitHisto_run, "\
        #         + "2_bit_0, " + "WrEn_InputSpy, " + "CI_mode"
        #     desiredReg = raw_input("Enter cntrReg name: ")
        #     if desiredReg == '': desiredReg = 'all'
        #
        # settingList = raw_input("Enter cntrReg setting list ['n1','n2', ...]: ")
        #
        # self.write(desiredReg, settingList)

        # for RO register, read1 == read2 constitutes a PASS
        # NEED TO CHANGE THIS FOR CNTRREG SINCE WE EXPECT TO R/W NON-RAND VALUES!!
# ------------------------------------------------------------------------
class cntrRegChange(Test): # NOTE: this run() function is overloaded to require parameters
    # -------------------------------------------
    def testBody(self, desiredReg, settingStr):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s Change----------" %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
        print "settingStr: ", settingStr

        # Read1 = current register status
        read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
        print "allRegStr: ", allRegStr

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister(b, i.iglooAdd, reg, size) # gets new reg status
            print "cntrReg after 'all' WRITE: ", read2

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"              :   allRegStr[0:26],
            "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[28:30],
            "WrEn_InputSpy"     :   allRegStr[30:31],
            "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
                }
            # cntrReg = {
            # "31bX"             :   allRegStr[0:26],
            # "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            # "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            # "2_bit_0"           :   allRegStr[28:30],
            # "WrEn_InputSpy"     :   allRegStr[30:31],
            # "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            #     }

            #print "settingStr confirm: ", settingStr
            cntrReg[desiredReg] = settingStr
            #print "cntrReg[desiredReg]: ", cntrReg

            # Since Python is 'pass-by-object-reference', just because we changed
            # the dict cntrReg doesn't mean we changed allRegStr... So do that now
            #allRegStr = ''.join(cntrReg)
            allRegStr = cntrReg['31bX'] + cntrReg['orbitHisto_clear']\
                + cntrReg['orbitHisto_run'] + cntrReg["2_bit_0"]\
                + cntrReg['WrEn_InputSpy'] + cntrReg['CI_mode']

            #print "stringToBitList: ", i.stringToBitList(allRegStr)
            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            #print "toWrite: ", toWrite
            write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
            print "cntrReg after %s WRITE: " %desiredReg, read2
            if not (write1 and read2): return False
            else:
                return True

    # -------------------------------------------
    def run(self, desiredReg, settingStr):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg, settingStr) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
# ------------------------------------------------------------------------
class cntrRegChange_Quiet(Test): # NOTE: this run() function is overloaded to require parameters
    # -------------------------------------------
    def testBody(self, desiredReg, settingStr):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s Change----------" %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
        # print "settingStr: ", settingStr

        # Read1 = current register status
        read1 = i.readFromRegister_Quiet(b, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
        # print "allRegStr: ", allRegStr

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister_Quiet(b, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister_Quiet(b, i.iglooAdd, reg, size) # gets new reg status
            # print "cntrReg after 'all' WRITE: ", read2

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"              :   allRegStr[0:26],
            "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[28:30],
            "WrEn_InputSpy"     :   allRegStr[30:31],
            "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
                }
            # cntrReg = {
            # "31bX"             :   allRegStr[0:26],
            # "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            # "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            # "2_bit_0"           :   allRegStr[28:30],
            # "WrEn_InputSpy"     :   allRegStr[30:31],
            # "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            #     }

            #print "settingStr confirm: ", settingStr
            cntrReg[desiredReg] = settingStr
            #print "cntrReg[desiredReg]: ", cntrReg

            # Since Python is 'pass-by-object-reference', just because we changed
            # the dict cntrReg doesn't mean we changed allRegStr... So do that now
            #allRegStr = ''.join(cntrReg)
            allRegStr = cntrReg['31bX'] + cntrReg['orbitHisto_clear']\
                + cntrReg['orbitHisto_run'] + cntrReg["2_bit_0"]\
                + cntrReg['WrEn_InputSpy'] + cntrReg['CI_mode']

            #print "stringToBitList: ", i.stringToBitList(allRegStr)
            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            #print "toWrite: ", toWrite
            write1 = i.writeToRegister_Quiet(b, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister_Quiet(b, i.iglooAdd, reg, size) #displays new reg
            # print "cntrReg after %s WRITE: " %desiredReg, read2
            if not (write1 and read2): return False
            else:
                return True

    # -------------------------------------------
    def run(self, desiredReg, settingStr):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg, settingStr) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
# ------------------------------------------------------------------------
class cntrRegTerminalChange(Test): # (NOT USED)
    # FILL THIS IN
    def testBody(self):
        return True
# ------------------------------------------------------------------------
class clk_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "clk_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(b, i.iglooAdd, reg, size)):
            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class rst_QIE_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "rst_QIE_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(b, i.iglooAdd, reg, size)):
            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class wte_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "wte_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(b, i.iglooAdd, reg, size)):
            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class capIDErr_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "capIDErr_count"
        reg = [i.igloo[name]["register"]["link1"],\
            i.igloo[name]["register"]["link2"],i.igloo[name]["register"]["link3"]]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        linkPass = [False, False, False]

        # for RO count register, just test ability to read out
        link = 0
        for n in reg:
            print '----Link',link+1,'----'
            if (i.readFromRegister(b, i.iglooAdd, n, size)):
                linkPass[link] = True

            link = link + 1

        if (linkPass[0] and linkPass[1] and linkPass[2]):
            print "~~ALL PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fifo_data(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fifo_data"
        reg = [i.igloo[name]["register"]["data1"],\
            i.igloo[name]["register"]["data2"],i.igloo[name]["register"]["data3"]]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        dataPass = [False, False, False]

        # for RO register, read1 == read2 constitutes a PASS
        data = 0
        for n in reg:
            print '----Data',data+1,'----'
            if (i.RWR_forRO(b, i.iglooAdd, n, size)):
                dataPass[data] = True

            data = data + 1

        if (dataPass[0] and dataPass[1] and dataPass[2]):
            print "~~ALL PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class inputSpy(Test): #NOTE: processes Spy Buffer Data with bitwise operations
    # -------------------------------------------
    def testBody(self):
        name = "inputSpy"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print "----------%s----------" %name
        passCount_512 = 0 # maximum = 512
        prevCapId = []

        # Set total numbers of iterations (512 for full testing of InputSpy)
        TotalIterations = 512

        for iter in range(0, TotalIterations):
            print "ITER: ", iter
            capIdPass          = False
            adcPass            = False

            buff = i.readFromRegister(b, i.iglooAdd, reg, size)

            # if good read
            if (buff) != False:
                buff.reverse() # InputSpy doesn't flip bytes like Bridge does
                #print "buff from read: ", buff

                # Get InputSpy data (qieList = [capIdConcise, adc, rangeQ, tdc])
                qieList = self.printData(buff)

                # Check CapID
                print "prevCapId: ", prevCapId
                if self.checkCapId(qieList[0], prevCapId, iter):
                    print "~~CapIDs Rotate~~"
                    capIdPass = True
                else: print "CapId Rotation ERROR: ", prevCapId, ' -> ', qieList[0]

                # Check ADC
                if self.checkAdc(qieList[1]):
                    print "~~ACD Good Range~~"
                    adcPass = True

                if (capIdPass and adcPass): passCount_512 += 1

                prevCapId = qieList[0]

            # if bad read
            else: print "ERROR: Cannot Read Buffer, ITER: ",iter

        # return after 512 iterations
        if passCount_512 == TotalIterations:
            print "~~ ALL 512 PASS ~~"
            return True
        else:
            print ">> Pass Count (out of 512): ", passCount_512, " <<"
            return False

    # -------------------------------------------
    def interleave(self, c0, c1):
        retval = 0;
        for i in range(0,8):
            bitmask = 0x01 << i
            retval |= ((c0 & bitmask) | ((c1 & bitmask) << 1)) << i

        return retval
    # -------------------------------------------
    def printData(self,buff): # returns: qieList = [capIdConcise, adc, rangeQ, tdc]
        # buff holds 25 bytes (first 24)
        pedArray = [] # dimensions: pedArray[12][4]
        for x in xrange(12):
            row = []
            for y in xrange(4):
                row.append(-1)
            pedArray.append(row)

        BITMASK_TDC = 0x07 # const char
        OFFSET_TDC  = 4 # const int
        BITMASK_ADC = 0x07 # const char
        OFFSET_ADC  = 1 # const int
        BITMASK_EXP = 0x01 # const char
        OFFSET_EXP  = 0 # const int
        BITMASK_CAP = 0x01 # const char
        OFFSET_CAP  = 7 # const int

        fifoEmpty = buff[24] & 0x80
        fifoFull  = buff[24] & 0x40
        clkctr    = buff[24] & 0x3f
        adc     = []
        tdc     = []
        capId   = []
        rangeQ  = []

        for i in range(0,12):

            adc1 = (buff[(11-i)*2 + 1] >> OFFSET_ADC) & BITMASK_ADC
            adc0 = (buff[(11-i)*2    ] >> OFFSET_ADC) & BITMASK_ADC
            tdc1 = (buff[(11-i)*2 + 1] >> OFFSET_TDC) & BITMASK_TDC
            tdc0 = (buff[(11-i)*2    ] >> OFFSET_TDC) & BITMASK_TDC
            cap1 = (buff[(11-i)*2 + 1] >> OFFSET_CAP) & BITMASK_CAP
            cap0 = (buff[(11-i)*2    ] >> OFFSET_CAP) & BITMASK_CAP
            exp1 = (buff[(11-i)*2 + 1] >> OFFSET_EXP) & BITMASK_EXP
            exp0 = (buff[(11-i)*2    ] >> OFFSET_EXP) & BITMASK_EXP

            adc.append(self.interleave(adc0, adc1))
            tdc.append(self.interleave(tdc0, tdc1))
            capId.append(self.interleave(cap0, cap1))
            rangeQ.append(self.interleave(exp0, exp1))

            pedArray[i][0x03 & int(capId[i])] += int(0x3f & adc[i])

        print "capID...", capId

        print "FIFO empty: %1d   FIFO full: %1d   clk counter: %6d\n" % (fifoEmpty,fifoFull,clkctr)
        print "       "
        # for i in range(12):
        #     print "  QIE %2d  " % (i + 1)


        capIdConcise = []
        for i in capId:
            capIdConcise.append(i & 0x03)

        print "\nCapID: ", capIdConcise
        print "\nADC:   ", adc
        print "\nRANGE: ", rangeQ
        print "\nTDC:   ", tdc
        print '\n'

        qieList = [capIdConcise, adc, rangeQ, tdc]

        return qieList
    # -------------------------------------------
    def checkCapId(self, capId, prevCapId, iter):
        allSamePass = True
        rotatePass  = True
        checkList = [capId[0]]*12
        rotateList = []

        # check that all 12 chips are same capId
        count = 0
        for i in capId:
            if (i != checkList[count]):
                allSamePass = False
            count += 1

        if iter != 0: # if a legit prevCapId exists
            if prevCapId[0]   == 0:   rotateList = [1]*12
            elif prevCapId[0] == 1:   rotateList = [2]*12
            elif prevCapId[0] == 2:   rotateList = [3]*12
            elif prevCapId[0] == 3:   rotateList = [0]*12
            else: print "PrevCapId out of Scope 0-3"

            if capId != rotateList:
                rotatePass = False

        return (allSamePass and rotatePass)

    # -------------------------------------------
    def checkAdc(self, adc):
        goodValPass = True

        for i in adc:
            if i >= 100:
                print "Bad ADC Value: ", i
                goodValPass = False

        return goodValPass
# ------------------------------------------------------------------------
class inputSpyRWR(Test): #NOTE: confirms RO nature of reg... doesn't process Spy Buffer
    def testBody(self):
        name = "inputSpy"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print "----------%s RWR----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class inputSpy_512Reads(Test):
    def testBody(self):
        myCntrRegChange = cntrRegChange_Quiet(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print myCntrRegChange.run("WrEn_InputSpy", '1')
        myCntrRegChange = cntrRegChange_Quiet(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print myCntrRegChange.run("WrEn_InputSpy", '0')
        # myCntrRegDisplay = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        # print myCntrRegDisplay.run()
        myInputSpy = inputSpy(b,i.igloo["inputSpy"]["register"],'iglooClass.txt', 1)
        print myInputSpy.run()

        return True
# ------------------------------------------------------------------------
class spy96Bits(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "spy96Bits"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class qie_ck_ph(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "qie_ck_ph"
        reg = [i.igloo[name]["register"][1],i.igloo[name]["register"][2],\
            i.igloo[name]["register"][3],i.igloo[name]["register"][4],\
            i.igloo[name]["register"][5],i.igloo[name]["register"][6],\
            i.igloo[name]["register"][7],i.igloo[name]["register"][8],\
            i.igloo[name]["register"][9],i.igloo[name]["register"][10],\
            i.igloo[name]["register"][11],i.igloo[name]["register"][12]]

        # for i in range(1,13):
        #     reg.append(i.igloo[name]["register"][str(i)])

        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        qiePass = [False,False,False,False,False,False,False,False,\
            False,False,False,False]

        # for RO register, read1 == read2 constitutes a PASS
        count = 0
        for n in reg:
            print '----Qie',count+1,'----'
            if (i.RWR_withRestore(b, i.iglooAdd, n, size)):
                qiePass[count] = True

            count = count + 1

        if (qiePass[0] and qiePass[1] and qiePass[2] and qiePass[3] and \
            qiePass[4] and qiePass[5] and qiePass[6] and qiePass[7] and \
            qiePass[8] and qiePass[9] and qiePass[10] and qiePass[11]):
            print "~~ALL PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_mode(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "link_test_mode"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_pattern(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "link_test_pattern"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "dataToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class addrToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "addrToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ctrlToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ctrlToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataFromSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "dataFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statFromSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "statFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class scratchReg(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "scratchReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class CI_Mode_On(Test): # turns on Charge Injection on card
    def testBody(self):
        myCntrRegChange = cntrRegChange_Quiet(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print myCntrRegChange.run("CI_mode", '1')
        return True
# ------------------------------------------------------------------------
class CI_Mode_Off(Test): # turns off Charge Injection on card
    def testBody(self):
        myCntrRegChange = cntrRegChange_Quiet(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print myCntrRegChange.run("CI_mode", '0')
        return True
# ------------------------------------------------------------------------

def runAll():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)

    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaMinVer(b,i.igloo["fpgaMinVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = ones(b,i.igloo["ones"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = zeroes(b,i.igloo["zeroes"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaTopOrBottom(b,i.igloo["fpgaTopOrBottom"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = uniqueID(b,i.igloo["uniqueID"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = statusReg(b,i.igloo["statusReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run("all", "")
    m = clk_count(b,i.igloo["clk_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = rst_QIE_count(b,i.igloo["rst_QIE_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = wte_count(b,i.igloo["wte_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = capIDErr_count(b,i.igloo["capIDErr_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fifo_data(b,i.igloo["fifo_data"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = inputSpy(b,i.igloo["inputSpy"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = spy96Bits(b,i.igloo["spy96Bits"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = qie_ck_ph(b,i.igloo["qie_ck_ph"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = link_test_mode(b,i.igloo["link_test_mode"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = link_test_pattern(b,i.igloo["link_test_pattern"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = dataToSERDES(b,i.igloo["dataToSERDES"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = addrToSERDES(b,i.igloo["addrToSERDES"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = ctrlToSERDES(b,i.igloo["ctrlToSERDES"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = dataFromSERDES(b,i.igloo["dataFromSERDES"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = statFromSERDES(b,i.igloo["statFromSERDES"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = scratchReg(b,i.igloo["scratchReg"]["register"],'iglooClass.txt', 1)
    print m.run()

def runSelect():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)


    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaMinVer(b,i.igloo["fpgaMinVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = ones(b,i.igloo["ones"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = zeroes(b,i.igloo["zeroes"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaTopOrBottom(b,i.igloo["fpgaTopOrBottom"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = uniqueID(b,i.igloo["uniqueID"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = statusReg(b,i.igloo["statusReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run("all", "")
    m = clk_count(b,i.igloo["clk_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = rst_QIE_count(b,i.igloo["rst_QIE_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = wte_count(b,i.igloo["wte_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = capIDErr_count(b,i.igloo["capIDErr_count"]["register"],'iglooClass.txt', 1)
    print m.run()
    # m = fifo_data(b,i.igloo["fifo_data"]["register"],'iglooClass.txt', 1)
    # print m.run()
    m = inputSpy(b,i.igloo["inputSpy"]["register"],'iglooClass.txt', 1)
    print m.run()
    # m = spy96Bits(b,i.igloo["spy96Bits"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = qie_ck_ph(b,i.igloo["qie_ck_ph"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = link_test_mode(b,i.igloo["link_test_mode"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = link_test_pattern(b,i.igloo["link_test_pattern"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = dataToSERDES(b,i.igloo["dataToSERDES"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = addrToSERDES(b,i.igloo["addrToSERDES"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = ctrlToSERDES(b,i.igloo["ctrlToSERDES"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = dataFromSERDES(b,i.igloo["dataFromSERDES"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = statFromSERDES(b,i.igloo["statFromSERDES"]["register"],'iglooClass.txt', 1)
    # print m.run()
    # m = scratchReg(b,i.igloo["scratchReg"]["register"],'iglooClass.txt', 1)
    # print m.run()

def readOutInputSpy():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run("WrEn_InputSpy", "1")

    m = inputSpy(b,i.igloo["inputSpy"]["register"],'iglooClass.txt', 512)
    print m.run()

def processInputSpy():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)
    m = inputSpy_512Reads(b,i.igloo["inputSpy"]["register"],'iglooClass.txt', 1)
    print m.run()

def changeCI_MODE():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run("CI_mode", "1")
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()

def cntrRegShow():
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(3)
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
    print m.run()

def setCI_mode(onOffBit):
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0)
    
    if onOffBit == 1:
        m = CI_Mode_On(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print m.run()

    elif onOffBit == 0:
        m = CI_Mode_Off(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
        print m.run()

    else: print "Invalid onOffBit"

# def SetQInjMode(onOffBit, slot, piAddress):
# def SetQInjMode(onOffBit):
#     #expects onOffBit of 0 or 1
#     cntrRegShow()
#     if onOffBit == 0 or onOffBit == 1:
#         #b = webBus(piAddress, 0)
#         b.write(0x1c,[0x11,0x03,0,0,0])
#         b.write(0x09,[0x11,onOffBit,0,0,0])
#         b.sendBatch()
#     else:
#         print "INVALID INPUT IN SetQInjMode... doing nothing"
#
#     cntrRegShow()


###########################################
# RUN FUNCTIONS
###########################################

#runAll()
#runSelect()
#readOutInputSpy()
processInputSpy()
#changeCI_MODE()




# RW functions to do cursory RW test:
#   * uniqueID
#   * qie_ck_ph
#   * link_test_mode
#   * link_test_pattern
#   * dataToSERDES
#   * addrToSERDES
#   * ctrlToSERDES
#   * scratchReg
# RW functions to allow setting changes:
#   * cntrReg




# def changeCI_MODE():
#     def openChannel():
#       b.write(0x72,[0x02])
#       b.write(0x74,[0x02])
#       b.sendBatch()
#     openChannel()
#
#     def openIgloo(slot):
#         #the igloo is value "3" in I2C_SELECT table
#         b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
#         b.sendBatch()
#     openIgloo(3)
#
#         b.write(0x09,[0x11,1,0,0,0])
#         b.sendBatch()
#
#
# def changeCI_MODE():
#     def openChannel():
#       b.write(0x72,[0x02])
#       b.write(0x74,[0x02])
#       b.sendBatch()
#     openChannel()
#
#     def openIgloo(slot):
#         #the igloo is value "3" in I2C_SELECT table
#         b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
#         b.sendBatch()
#     openIgloo(3)
#
#     m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
#     print m.run()
#     m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
#     print m.run("CI_mode", "1")
#     m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 1)
#     print m.run()
