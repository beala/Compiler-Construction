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
		if not isinstance(other, Register):
			return False
		return self.myRegister == other.myRegister
	def __str__(self):
		return "%"+self.myRegister
class MemLoc(Node):
	def __init__(self, offset):
		self.offset = offset #caller specifies +/-
		self.spillable = True
	def __str__(self):
		return "%s(%%ebp)" % str(self.offset)
	def __eq__(self, other):
		if not isinstance(other, MemLoc):
			return False
		return self.offset == other.offset
class AddressLabel(Node):
	def __init__(self, myValue):
		self.myValue = myValue
	def __str__(self):
		return '$' + ("%s" % self.myValue)
class VarNode(Node):
	spillable = True
	saturation = 0
	degree = 0
	adjacentNodes = set()
	color = -1
	myName = ""
	def __repr__(self):
		return str(self)
	def __init__(self,myName):
		self.myName = myName
	def __cmp__(self,other):
		if (self.spillable == False and other.spillable == True):
			return -1
		elif (other.spillable == False and self.spillable == True):
			return 1
		elif (self.saturation > other.saturation):
			return -1
		elif (other.saturation > self.saturation):
			return 1
		elif (self.degree > other.degree):
			return -1
		elif (other.degree > self.degree):
			return 1
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
	def calculatePriority(self):
		return -1 * (self.saturation + 0 if self.spillable else 100)

class x86(object):
	numOperands = 0
	liveSetBefore = set()
	liveSetAfter = set()
	optimizeBehavior = True
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
	def __repr__(self):
		return self.__str__()
class LiveSetAlg(object):
	_instrNode = None
	def setInstrNode(self, instructNode):
		self._instrNode = instructNode

	def doCalcLiveSetIfWhile(self, previousLiveSet):
		liveSetAll = set()
		if isinstance(self._instrNode, Whilex86):
			iterations = 2
		else:
			iterations = 1
		for i in range(iterations):
			for number in reversed(range(self._instrNode.numOperands)):
				# Calculate the l_before of each.
				# previousLiveSet = set()
				for instruction in reversed(self._instrNode.operandList[number]):
					previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
				# Union it into the l_before of the if instruction
				liveSetAll = liveSetAll | previousLiveSet
		
		liveSetBefore = set(liveSetAll)
		liveSetBefore &= previousLiveSet
		return liveSetBefore

	def doCalcLiveSetWhile(self, previousLiveSet):
		liveSetAll = set()
		for i in range(2):
			liveSetAll = self._doCalcLiveSet_IfWhile(liveSetAll, previousLiveSet)
		liveSetBefore = set(liveSetAll)
		liveSetBefore &= previousLiveSet
		return liveSetBefore

	def _doCalcLiveSet_IfWhile(self, liveSetAll, previousLiveSet):
		# Iterate through if, then, else.
		for number in reversed(range(self._instrNode.numOperands)):
			# Calculate the l_before of each.
			# previousLiveSet = set()
			for instruction in reversed(self._instrNode.operandList[number]):
				previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
			# Union it into the l_before of the if instruction
			liveSetAll = liveSetAll | previousLiveSet
		return liveSetAll

class Ifx86(x86):
	numOperands = 3
	def __init__(self, test, then, else_):
		super(Ifx86, self).__init__()
		self.instruction = "_IF"
		self.operandList = [test, then, else_]
	def doCalculateLiveSet(self, previousLiveSet):
#		liveSetAlg = LiveSetAlg()
#		liveSetAlg.setInstrNode(self)
#		self.liveSetBefore = liveSetAlg.doCalcLiveSetIfWhile(previousLiveSet)
#		return self.liveSetBefore

		liveSetAll = set()
		# Iterate through if, then, else.
		originalLiveSet = previousLiveSet
		for number in reversed(range(3)):
			# Calculate the l_before of each.
			# previousLiveSet = set()
			if number == 1:
				previousLiveSet = originalLiveSet
			if number == 0:
				previousLiveSet = self.operandList[1][0].liveSetBefore | (self.operandList[2][0].liveSetBefore if len(self.operandList[2]) > 0 else set([]))
			for instruction in reversed(self.operandList[number]):
				previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
			# Union it into the l_before of the if instruction
			liveSetAll = liveSetAll | previousLiveSet
		
		self.liveSetBefore = set(liveSetAll)
		self.liveSetBefore &= previousLiveSet
		#import pdb; pdb.set_trace()
		return self.liveSetBefore
	def __str__(self):
		myString = ""
		for number in range(3):
			for instruction in self.operandList[number]:
				myString +=  "-"*(number+1) + ">" + str(instruction)+"\n"
		return myString

class Whilex86(x86):
	numOperands = 2
	def __init__(self, test, body):
		super(Whilex86, self).__init__()
		self.instrution = "_WHILE"
		self.operandList = [test, body]
	def doCalculateLiveSet(self, previousLiveSet):
		liveSetAlg = LiveSetAlg()
		liveSetAlg.setInstrNode(self)
		self.liveSetBefore = liveSetAlg.doCalcLiveSetIfWhile(previousLiveSet)
		return self.liveSetBefore
		
#		liveSetAll = set()
#		# Iterate through if, then, else.
#		for i in range(2):
#			for number in reversed(range(2)):
#				# Calculate the l_before of each.
#				# previousLiveSet = set()
#				for instruction in reversed(self.operandList[number]):
#					previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
#				# Union it into the l_before of the if instruction
#				liveSetAll = liveSetAll | previousLiveSet
#		
#		self.liveSetBefore = set(liveSetAll)
#		self.liveSetBefore &= previousLiveSet
#		#import pdb; pdb.set_trace()
#		return self.liveSetBefore
	def __str__(self):
		myString = ""
		myString += "WHILE:\n"
		myString += "\t TEST: "+str(self.operandList[0])
		myString += "\n\t BODY:" + str(self.operandList[1])
		for number in range(1):
			for instruction in self.operandList[number]:
				myString +=  "-"*(number+1) + ">" + str(instruction)+"\n"
		return myString

class Cmpl(x86):
	numOperands = 2
	def __init__(self,op1,op2):
		super(Cmpl, self).__init__()
		self.instruction = "cmpl"
		if isinstance(op1, Node):
			self.operandList.append(op1)
		else:
			raise TypeError("Can't assign that to Cmpl!")
		if isinstance(op2, Node):
			self.operandList.append(op2)
		else:
			raise TypeError("Can't assign that to Cmpl!")
	def __str__(self):
		return "%s %s,%s" % (self.instruction, self.operandList[0], self.operandList[1])
class Jmp(x86):
	numOperands = 1
	def __init__(self,label):
		super(Jmp, self).__init__()
		self.instruction = "jmp"
		self.operandList.append(label)
	def __str__(self): 
		return "%s %s" % (self.instruction, self.operandList[0])
	def doCalculateLiveSet(self):
		pass
class JmpStar(Jmp):
	numOperands = 1
	def __init__(self, operand1):
		super(JmpStar, self).__init__(operand1)
		self.instruction = "jmp *"
		self.operandList.append(operand1)
		self.operandList[0].spillable = False
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])
	def doCalculateLiveSet(self, currentLiveSet):
		self.liveSetBefore = currentLiveSet | set([self.operandList[0]])
		return self.liveSetBefore
class Jne(x86):
	numOperands = 1
	def __init__(self,label):
		super(Jne, self).__init__()
		self.instruction = "jne"
		self.operandList.append(label)
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])
	def doCalculateLiveSet(self):
		pass
class Label(x86):
	numOperands = 0
	def __init__(self, label):
		super(Label, self).__init__()
		self.instruction = label
	def __str__(self):
		return "%s:" % (self.instruction)
	def doCalculateLiveSet(self):
		pass
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
		self.isDeadWrite = False
	def doCalculateLiveSet(self,currentLiveSet):
		self.liveSetBefore = currentLiveSet
		if (self.optimizeBehavior) and (isinstance(self.operandList[1], VarNode)) and (self.operandList[1] not in currentLiveSet):
			#import pdb; pdb.set_trace()
			self.isDeadWrite = True
			return self.liveSetBefore
		if isinstance(self.operandList[1],VarNode):
			self.liveSetBefore = self.liveSetBefore - set([self.operandList[1]])
		if isinstance(self.operandList[0],VarNode):
			self.liveSetBefore = self.liveSetBefore | set([self.operandList[0]])
		return self.liveSetBefore
	def __str__(self):
		if self.optimizeBehavior and self.isDeadWrite:
			return "# removed dead write! " + "%s %s,%s" % (self.instruction, self.operandList[0], self.operandList[1])
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

class CallStar(Call):
	numOperands = 1
	def __init__(self, operand1):
		super(CallStar, self).__init__(operand1)
		self.instruction = "call *"
		self.operandList.append(operand1)
	def __str__(self):
		return "%s %s" % (self.instruction, self.operandList[0])
	def doCalculateLiveSet(self, currentLiveSet):
		self.liveSetBefore = currentLiveSet | set([self.operandList[0]])
		return self.liveSetBefore
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
class FunctionLabel(Label):
	def doCalculateLiveSet(self, currentLiveSet):
		self.liveSetBefore = currentLiveSet
		return self.liveSetBefore
	def __str__(self):
		return "\n.globl "+self.instruction+"\n"+ self.instruction+":"
