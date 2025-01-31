# CSCI4555 x86 Abstract Syntax Tree Class
# Created by: Josh Wepman <joshua.wepman@colorado.edu>
# 19 Sept 2011

class Node(object):
	def __init__(self):
		pass

class ConstNode(Node):
	def __init__(self,myValue):
		self.myValue = myValue
	def __str__(self):
		return "$"+str(self.myValue)
class Register(Node):
	def __init__(self,myRegister):
		self.myRegister = myRegister
	def __eq__(self,other):
		return self.myRegister == other.myRegister
	def __str__(self):
		return "%"+self.myRegister
class VarNode(Node):
	spillable = True
	saturation = 0
	degree = 0
	adjacentNodes = set()
	color = -1
	myName = ""
	def __init__(self,myName):
		self.myName = myName
	def __cmp__(self,other):
		if (self.spillable == False and other.spillable == True):
			return 1
		elif (other.spillable == False and self.spillable == True):
			return -1
		elif (self.saturation > other.saturation):
			return 1
		elif (other.saturation > self.saturation):
			return -1
		elif (self.degree > other.degree):
			return 1
		elif (other.degree > self.degree):
			return -1
		else:
			return 0
	def equalColors(self,other):
		if not isinstance(other,VarNode):
			return False
		return self.color == other.color
	def __eq__(self,other):
		if not isinstance(other,VarNode):
			return False
		return self.myName == other.myName
	def __str__(self):
		if (self.color != -1):
			return str(self.color) #+"<colored "+self.myName+">"
		else:
			return self.myName+"<uncolored>"
	def addAdjacency(self,other):
		self.adjacentNodes.append(other)

class x86(object):
	numOperands = 0
	liveSetBefore = set()
	liveSetAfter = set()
	def __init__(self):
		self.instruction = ""
		self.operandList = []
		self.liveSetBefore = set()
	def __eq__(self,other):
		return (self.instruction == other.instruction and self.operandList == other.operandList)
	def isFullyColored(self):
		for node in self.operandList:
			if (node.isColored == False):
				return False
		return True
	def getVarNodesFromOperands(self):
		#return list of var nodes (not constants or registers) from operand list
		myList = []
		for node in self.operandList:
			if isinstance(node,VarNode):
				myList.append(node)
		return myList
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = set(currentLiveSet) | set(self.getVarNodesFromOperands())
		return self.liveSetBefore
	def __str__(self):
		return "%s" % self.instruction

class Movl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		super(Movl, self).__init__()
		self.instruction = "movl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.append(operand2)
		else:
			self.operandList.append(Node)
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = currentLiveSet
		if isinstance(self.operandList[1],VarNode):
			self.liveSetBefore = self.liveSetBefore - set([self.operandList[1]])
		if isinstance(self.operandList[0],VarNode):
			self.liveSetBefore = self.liveSetBefore | set([self.operandList[0]])
		return self.liveSetBefore
	def __str__(self):
		return "%s %s,%s" % (self.instruction, self.operandList[0], self.operandList[1])
	


class Pushl(x86):
	numOperands = 1
	def __init__(self,operand1):
		super(Pushl, self).__init__()
		self.instruction = "pushl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])

class Popl(x86):
	numOperands = 1
	def __init__(self,operand1):
		super(Popl, self).__init__()
		self.instruction = "popl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])
	def doCalculateLiveSet(self, currentLiveSet):
		self.liveSetBefore = currentLiveSet - set(self.getVarNodesFromOperands())
		return self.liveSetBefore

class Addl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		super(Addl, self).__init__()
		self.instruction = "addl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.append(operand2)
		else:
			self.operandList.append(Node)
	def __str__(self):
		return "%s %s,%s" % (self.instruction, self.operandList[0], self.operandList[1])



class Negl(x86):
	numOperands = 1
	def __init__(self,operand1):
		super(Negl, self).__init__()
		self.instruction = "negl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])

class Subl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		super(Subl, self).__init__()
		self.instruction = "subl"
		if (isinstance(operand1, Node)):
			self.operandList.append(operand1)
		else:
			self.operandList.append(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.append(operand2)
		else:
			self.operandList.append(Node)
	def __str__(self):
		return "%s %s,%s" % (self.instruction, self.operandList[0], self.operandList[1])

class Call(x86):
	numOperands = 1
	def __init__(self,operand1):
		super(Call, self).__init__()
		self.instruction = "call"
		self.operandList.append(operand1)
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = currentLiveSet
		return self.liveSetBefore
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])

class Leave(x86):
	numOperands = 0
	def __init__(self):
		super(Leave, self).__init__()
		self.instruction = "leave"
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = currentLiveSet
		return self.liveSetBefore
class Ret(x86):
	numOperands = 0
	def __init__(self):
		super(Ret, self).__init__()
		self.instruction = "ret"
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = currentLiveSet
		return self.liveSetBefore
