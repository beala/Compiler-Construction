#CSCI4555 RegisterAlloc.py - Register Allocation Class Files
#Created by: Josh Wepman, <joshua.wepman@colorado.edu>
#Date: 18 September 2011

class varNode:
	#corresponds to node in register allocator graph
	def __cmp__(self, other):
		if (self.degree > other.degree):
			return 1
		else if (self.degree == other.degree):
			return 0
		else:
			return -1
	def __init__(self, name, isTemporary=False, isSpillable=True):
		self.name = name
		self.isTemporary = isTemporary
		self.isSpillable = isSpillable
		self.degree = 0
		
class nodeStructure:

class varGraph:
	#set of varNodes and connctions between them
	def __init__(self):
		self.isColored = False
		self.nodes 