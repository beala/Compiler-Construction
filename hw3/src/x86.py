# CSCI4555 x86 Abstract Syntax Tree Class
# Created by: Josh Wepman <joshua.wepman@colorado.edu>
# 19 Sept 2011

class Node:
	def __init__(self):
		pass

class ConstNode(Node):
	def __init__(self,myValue):
		self.myValue = myValue
	def __str__(self):
		return "$"+self.myValue
class Register(Node):
	def __init__(self,myRegister):
		self.myRegister = myRegister
	def __str__(self):
		return "%"+myRegister
class VarNode(Node):
	spillable = True
	saturation = 0
	degree = 0
	adjacentNodes = set()
	color = ""
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
	def __str__(self):
		if (self.color != ''):
			return self.color
		else:
			return self.myName+"<uncolored>"
	def addAdjacency(self,other):
		self.adjacentNodes.add(other)

class x86:
	numOperands = 0
	def __init__(self):
		self.instruction = ""
		self.operandList = []
	def __eq__(self,other):
		return (self.instruction == other.instruction and self.operandList == other.operandList)
	def isFullyColored(self):
		for node in self.operandList:
			if (node.isColored == False):
				return False
		return True
	def __str__(self):
		return "%s" % self.operation

class Movl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		self.instruction = "movl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.add(operand2)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s,%s" % (self.operation, self.operandList[0], self.operandList[1])
	


class Pushl(x86):
	numOperands = 1
	def __init__(self,operand1):
		self.instruction = "pushl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s" % (self.operation, self.operandList[0])

class Popl(x86):
	numOperands = 1
	def __init__(self,operand1):
		self.instruction = "popl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s" % (self.operation, self.operandList[0])

class Addl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		self.instruction = "addl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.add(operand2)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s,%s" % (self.operation, self.operandList[0], self.operandList[1])



class Negl(x86):
	numOperands = 1
	def __init__(self,operand1):
		self.instruction = "negl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s" % (self.operation, self.operandList[0])

class Subl(x86):
	numOperands = 2
	def __init__(self,operand1,operand2):
		self.instruction = "subl"
		if (isinstance(operand1, Node)):
			self.operandList.add(operand1)
		else:
			self.operandList.add(Node)
		
		if (isinstance(operand2, Node)):
			self.operandList.add(operand2)
		else:
			self.operandList.add(Node)
	def __str__(self):
		return "%s %s,%s" % (self.operation, self.operandList[0], self.operandList[1])

class Call(x86):
	numOperands = 1
	def __init__(self,operand1):
		self.instruction = "call"
		self.operandList.add(operand1)
	def __str__(self):
		return "%s %s" % (self.operation, self.operandList[0])

class Leave(x86):
	numOperands = 0
	def __init__(self):
		self.instruction = "leave"
		self.operandList = []
class Ret(x86):
	numOperands = 0
	def __init__(self):
		self.instruction = "ret"
		self.operandList = []

