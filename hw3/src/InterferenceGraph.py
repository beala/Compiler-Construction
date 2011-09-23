from x86 import * 
import Queue

class InterferenceGraph(object):
	__theGraph = {} #`VarNode => set([adjacent VarNodes])
	__ir = []
	__registers = [Register('ecx'),Register('edx'),Register('eax')]
	__listColors = {1:'eax',2:'ebx',3:'ecx',4:'edx'}
	__stackOffset = 4
	def __init__(self,IR):
		self.__ir = IR
		for node2 in self.__ir:
			for node in node2.operandList: 
				if isinstance(node,VarNode) and not self.__theGraph.has_key(node):
					self.__theGraph[node] = set()
		for reg in self.__registers:
			self.__theGraph[reg] = set()
	def insertConnection(self,node1,node2):
		if not ((isinstance(node1,VarNode) or isinstance(node1,Register)) and (isinstance(node2,VarNode) or isinstance(node2,Register))):
			return
		self.__theGraph[node1] = self.__theGraph[node1] | set([node2])
		self.__theGraph[node2] = self.__theGraph[node2] | set([node1])
	def getIR(self):
		return self.__ir
	def insertNode(self, node):
		self.__theGraph[node] = set()
	def __copylBeforeTolAfter(self):
		lAfter = set()
		for node in reversed(self.__ir):
			node.liveSetAfter = lAfter
			lAfter=node.liveSetBefore
	def drawEdges(self):
		self.__copylBeforeTolAfter()
		for node in self.__ir:
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
	def __reduceDuplicateMoves(self):
		myCopy = []
		for element in self.__ir:
			if isinstance(element,Movl) and isinstance(element.operandList[0],VarNode) and isinstance(element.operandList[1],VarNode):
				if element.operandList[0].color == element.operandList[1].color:
					#print str(element.operandList[0].color) + "," + str(element.operandList[1].color)
					continue
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
		self.__ir = self.__reduceDuplicateMoves()
	def emitColoredIR(self):
		myString = "\tpush %ebp\n\tmovl %esp,%ebp\n\tsubl $"+str(self.__stackOffset)+",%esp\n"
		for instruction in self.__ir:
			if instruction.isFullyColored == False:
				return False
			for operand in instruction.operandList:
				if  isinstance(operand,VarNode) and isinstance(operand.color,int):
					if (operand.color <= 4):
						operand.color = "%"+str(self.__listColors.get(operand.color))
					else:
						operand.color = "-"+str(self.__listColors.get(operand.color))+"(%ebp)"
			myString += "\t"+str(instruction)+"\n"
		return myString
