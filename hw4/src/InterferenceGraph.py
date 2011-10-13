from x86 import * 
import Queue

class InterferenceGraph(object):
	__theGraph = {} #`VarNode => set([adjacent VarNodes])
	__ir = []
	__registers = [Register('ecx'),Register('edx'),Register('eax')]
	__listColors = {1:'eax',2:'ebx',3:'ecx',4:'edx'}
	__stackOffset = 4
	__currentTmpVar = 0
	def makeTmpVar(self):
		self.__currentTmpVar += 1
		return "{spillSaver" + str(self.__currentTmpVar)
	def __init__(self,IR):
		self.__theGraph = {}
		self.__initGraph(IR)
		self.__ir = IR
	def __initGraph(self, IR):	
		for instruction in IR:
			if isinstance(instruction, Ifx86):
				for number in range(3):
					self.__initGraph(instruction.operandList[number])
				continue
			for operand in instruction.operandList: 
				if isinstance(operand,VarNode) and not self.__theGraph.has_key(operand):
					self.__theGraph[operand] = set()
		for reg in self.__registers:
			self.__theGraph[reg] = set()

	def insertConnection(self,node1,node2):
		if not ((isinstance(node1,VarNode) or isinstance(node1,Register)) and (isinstance(node2,VarNode) or isinstance(node2,Register))):
			return
		if isinstance(node1, Register) and node1 not in self.__registers:
			return
		elif isinstance(node2, Register) and node2 not in self.__registers:
			return
		self.__theGraph[node1] = self.__theGraph[node1] | set([node2])
		self.__theGraph[node2] = self.__theGraph[node2] | set([node1])
	def getIR(self):
		return self.__ir
	def setIR(self,newIR):
		self.__ir = newIR
	def insertNode(self, node):
		self.__theGraph[node] = set()
	def __copylBeforeTolAfter(self, myIR):
		lAfter = set()
		for node in reversed(myIR):
			if isinstance(node, Ifx86):
				for number in range(3):
					self.__copylBeforeTolAfter(node.operandList[number])
			node.liveSetAfter = lAfter
			lAfter=node.liveSetBefore
	def drawEdges(self, myIR):
		self.__copylBeforeTolAfter(myIR)
		for node in myIR:
			if isinstance(node, Movl) and node.operandList[1] in node.liveSetAfter:
				for iterlAfter in node.liveSetAfter:
					if not (iterlAfter == node.operandList[1] or iterlAfter == node.operandList[0]):
						self.insertConnection(iterlAfter,node.operandList[1])
			elif isinstance(node, Negl) and node.operandList[0] in node.liveSetAfter:
				for iterlAfter in node.liveSetAfter:
					self.insertConnection(iterlAfter,node.operandList[0])
			elif ( isinstance(node, Addl) or isinstance(node, Subl) ) and node.operandList[1] in node.liveSetAfter:
				for iterlAfter in node.liveSetAfter:
					self.insertConnection(iterlAfter,node.operandList[1])
			elif isinstance(node, Call):
				for iterlAfter in node.liveSetAfter:
					for iterReg in self.__registers:
						self.insertConnection(iterlAfter, iterReg)
#			elif isinstance(node, Cmpl):
#				for iterlAfter in node.liveSetAfter:
#					self.insertConnection(iterlAfter, node.operandList[0])
#					self.insertConnection(iterlAfter, node.operandList[1])
			elif isinstance(node, Ifx86):
				writtenToSet = self.__getWrittenTo(node)
				for number in range(3):
					self.drawEdges(node.operandList[number])
				for iterlAfter in node.liveSetAfter:
					for writtenToElement in writtenToSet:
						self.insertConnection(iterlAfter, writtenToElement)
	def __getWrittenTo(self,ifNode):
		mySet = set()
		for instruction in ifNode.operandList[1]+ifNode.operandList[2]:
			if isinstance(instruction, Movl):
				mySet.add(instruction.operandList[1])
			elif isinstance(instruction, Addl):
				mySet.add(instruction.operandList[1])
			elif isinstance(instruction, Negl):
				mySet.add(instruction.operandList[0])
			#elif isinstance(instruction, Popl):
			#	mySet.add(instruction.operandList[0])
			elif isinstance(instruction, Call):
				for iterReg in self.__registers:
					mySet.add(iterReg)
			elif isinstance(instruction, Ifx86):
				mySet = mySet | self.__getWrittenTo(instruction)
		return mySet	
	def __reduceDuplicateMoves(self, irToReduce):
		myCopy = []
		for element in irToReduce:
			if isinstance(element,Movl) and isinstance(element.operandList[0],VarNode) and isinstance(element.operandList[1],VarNode):
				if element.operandList[0] == element.operandList[1]: #or ( not ( element.operandList[0].color == -1 or element.operandList[1].color == -1) and (element.operandList[0].color == element.operandList[1].color)):
					#print str(element.operandList[0].color) + "," + str(element.operandList[1].color)
					continue
			if isinstance(element, Ifx86):
				for number in range(3):
					element.operandList[number] = self.__reduceDuplicateMoves(element.operandList[number])
			myCopy.append(element)
		return myCopy
	def printGraph(self):
		myString = ""
		for node in self.__theGraph.keys():
			myString = myString + str(node) + "--> [" + ','.join([ str(node_connection) for node_connection in self.__theGraph[node] ]) + "]\n"
		return myString
	def __rebuildPriorityQueue(self,oldQueue):
		myNewQueue = Queue.PriorityQueue()
		while not oldQueue.empty():
			myNewQueue.put(oldQueue.get())
		return myNewQueue
	def doCalculateAvailColors(self,node):
		adjacentColors = set()
		for myNeighbor in self.__theGraph[node]:
			adjacentColors = adjacentColors | set([myNeighbor.color])
		return set(self.__listColors.keys()) - adjacentColors
	def doUpdateAdjacentSaturation(self,node):
		for myNeighbor in self.__theGraph[node]:
			myNeighbor.saturation = len(self.doCalculateAvailColors(myNeighbor))
		node.saturation = len(self.doCalculateAvailColors(node))
	def doColor(self):
		#color caller-save register nodes (just in case)
		for reg in self.__registers:
			reg.color = [ key for key,value in self.__listColors.items() if value == reg.myRegister ][0]
		#create priority queue of nodes and iterate
		nodesToColor = Queue.PriorityQueue()
		for node in self.__theGraph:
			if isinstance(node,VarNode):
				nodesToColor.put(node)
		while not nodesToColor.empty():
			adjacentColors = set([])
			node = nodesToColor.get()
			#find lowest color not in adjacent nodes (create one if needed -- this would be a stack location)
			availableColors = self.doCalculateAvailColors(node)
			
			if len(availableColors) == 0:
				#add stack slot (new color)
				largest_key = len(self.__listColors) + 1  #actually, this is the new key
				self.__listColors[largest_key] = self.__stackOffset
				self.__stackOffset = self.__stackOffset + 4
				node.color = largest_key
			else:
				sortedColorsList = [ color_key for color_key in availableColors ]
				sortedColorsList.sort()
				node.color = sortedColorsList[0]
	
			self.doUpdateAdjacentSaturation(node)
			nodesToColor = self.__rebuildPriorityQueue(nodesToColor)
	def emitColoredIR(self):
		myString = "\tpush %ebp\n\tmovl %esp,%ebp\n\tsubl $"+str(self.__stackOffset)+",%esp\n"
		for instruction in self.__ir:
			if instruction.isFullyColored == False:
				return False
			for operand in instruction.operandList:
				if  isinstance(operand,VarNode) and isinstance(operand.color,int):
					if self.__listColors.get(operand.color) == None:
						import pdb; pdb.set_trace()
					if (operand.color <= 4):
						operand.color = "%"+str(self.__listColors.get(operand.color))
					else:
						operand.color = "-"+str(self.__listColors.get(operand.color))+"(%ebp)"
			myString += "\t"+str(instruction)+"\n"
		return myString
	def __resetColors(self):
		for node in self.__theGraph:
			node.color=-1
	def __resetColorList(self):
		self.__listColors = {1:'eax',2:'ebx',3:'ecx',4:'edx'}
	def __calculateLiveSets(self):
 		previousLiveSet = set()
 		for instruction in reversed(self.__ir):
 			previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
	def __spillAnalysis(self, ir, alreadySpilled = False):
		spillFlag = alreadySpilled
		for instruction in ir:
			if isinstance(instruction, Ifx86):
				#Recurse into the test, then, and else branches
			#	if (spillFlag):
			#		import pdb; pdb.set_trace()
				(spillFlag, test_ir) = self.__spillAnalysis(instruction.operandList[0], spillFlag)
				instruction.operandList[0] = test_ir
				
				(spillFlag,then_ir) = self.__spillAnalysis(instruction.operandList[1], spillFlag)
				instruction.operandList[1] = then_ir
				
				(spillFlag, else_ir) = self.__spillAnalysis(instruction.operandList[2], spillFlag)
				instruction.operandList[2] = else_ir
				#Continue to next instruction
				continue
			if instruction.numOperands == 2 and isinstance(instruction.operandList[0],VarNode) and isinstance(instruction.operandList[1],VarNode):
				if instruction.operandList[0].color > 4 and instruction.operandList[1].color > 4:
					#insert spill code
					#if isinstance(instruction, Movl):
					#	secondArg = instruction.operandList[1]
					#	instruction.operandList[1] = VarNode(self.makeTmpVar())
					#	instruction.operandList[1].spillable = False
					#	newInstruction = Movl(instruction.operandList[1],secondArg)
					#	ir.insert(ir.index(instruction)+1,newInstruction)
					#	spillFlag =  True
					if isinstance(instruction, Movl) or isinstance(instruction, Addl) or isinstance(instruction, Cmpl):
						if instruction.operandList[0].spillable == False or instruction.operandList[1].spillable == False:
							#If one of the operands is already unspillable, don't make spill code for the spill code!
							spillFlag = True
							continue
						firstArg = instruction.operandList[0]
						instruction.operandList[0] = VarNode(self.makeTmpVar())
						instruction.operandList[0].spillable = False
						newInstruction = Movl(firstArg, instruction.operandList[0])
						ir.insert(ir.index(instruction), newInstruction)
						spillFlag = True
		#End For
		return (spillFlag, ir)
	
	def allocateRegisters(self):
		_spilled = False
		import Myx86Selector
		while True:
			#self.__ir = self.__reduceDuplicateMoves(self.__ir)
			#print "-"*100
			#Myx86Selector.Myx86Selector().prettyPrint(self.__ir)
			self.__initGraph(self.__ir)
			self.__resetColors()
			self.__resetColorList()
			self.__calculateLiveSets()
			self.drawEdges(self.__ir)
			self.doColor()
			self.__ir = self.__reduceDuplicateMoves(self.__ir)
			#print "-"*100
			#Myx86Selector.Myx86Selector().prettyPrint(self.__ir)
			(_spilled, self.__ir) = self.__spillAnalysis(self.__ir,False)
		#	print "Spilled: " + str(_spilled)
			if not _spilled:
			#	Myx86Selector.Myx86Selector().prettyPrint(self.__ir)
				break
			else:
				#print "Spilled!"
				self.__theGraph = {}	
