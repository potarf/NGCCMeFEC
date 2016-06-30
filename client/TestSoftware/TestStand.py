#TestStand.py

import RM
import sys
sys.path.append('../')
from client import webBus

class TestStand:
    def __init__(self, backplane, activeSlots, summaryList, suiteSelection, piAddress, iterations):
        '''Create a test stand object filled with necessary RMs, cards'''
	self.bus = webBus(piAddress, 0)
	self.suiteSelection = suiteSelection
	self.iters = iterations

        self.activeSlots = activeSlots
        self.RMs = []

        RM4_active = []
        RM3_active = []
        RM2_active = []
        RM1_active = []

	RM4_summaries = summaryList[0:4]
	RM3_summaries = summaryList[4:8]
	RM2_summaries = summaryList[8:12]
	RM1_summaries = summaryList[12:16]

        for slot in self.activeSlots:
            if slot in [2,3,4,5]:
                #RM4
                RM4_active.append(slot)
            elif slot in [7,8,9,10]:
                #RM3
                RM3_active.append(slot)
            elif slot in [18,19,20,21]:
                #RM2
                RM2_active.append(slot)
            elif slot in [23,24,25,26]:
                #RM1
                RM1_active.append(slot)

        #initialize RMs
	print "--- Determining which slots contain active cards ---\n"
        self.RMs.append(RM.RM(backplane, 1, RM1_active, RM1_summaries, self.bus))
        self.RMs.append(RM.RM(backplane, 2, RM2_active, RM2_summaries, self.bus))
        self.RMs.append(RM.RM(backplane, 3, RM3_active, RM3_summaries, self.bus))
        self.RMs.append(RM.RM(backplane, 4, RM4_active, RM4_summaries, self.bus))
	print "\n--- Slot determination finished. Beginning tests ---\n\n"

    def runAll(self):
	    for r in self.RMs:
		r.runAll(self.suiteSelection,self.iters)

    def runSingle(self, key):
        for r in self.RMs:
            r.runSingle(key)

    def __repr__(self):
        '''Object representation'''
        return "TestStand()"
    def __str__(self):
        '''Return string representation of object data'''
        s = ""
        for i in xrange(len(self.RMs)):
            s += "RM%i:\n%s\n" % (i, str(self.RMs[i]))
        return s
