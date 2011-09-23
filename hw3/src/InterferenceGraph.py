from x86 import * 

class InterferenceGraph(object):
	__theGraph = {} #`VarNode => set([adjacent VarNodes])
	__ir = []
	__registers = [Register('ecx'),Register('edx'),Register('eax')]

	def __init__(self,IR):
		self.__ir = IR
		for node2 in self.__ir:
			for node in node2.operandList: 
				if isinstance(node,VarNode) and not self.__theGraph.has_key(node):
					self.__theGraph[node] = set()
		for reg in self.__registers:
			self.__theGraph[reg] = set()
	def insertConnection(self,node1,node2):
		self.__theGraph[node1] = self.__theGraph[node1] | set([node2])
		self.__theGraph[node2] = self.__theGraph[node2] | set([node1])
	def insertNode(self, node):
		self.__theGraph[node] = set()
	def drawEdges(self):
		lAfter = set()
		for node in reversed(self.__ir):
			if isinstance(node, Movl) and node.operandList[1] in lAfter:
				for iterlAfter in lAfter:
					if iterlAfter != node.operandList[1] and iterlAfter != node.operandList[0]:
						self.insertConnection(iterlAfter,node.operandList[1])
			elif isinstance(node, Negl) and node.operandList[0] in lAfter:
				for iterlAfter in lAfter:
					self.insertConnection(iterlAfter,node.operandList[0])
			elif ( isinstance(node, Addl) or isinstance(node, Subl) ) and node.operandList[1] in lAfter:
				for iterlAfter in lAfter:
					self.insertConnection(iterlAfter,node.operandList[1])
			elif isinstance(node, Call):
				for iterlAfter in lAfter:
					for iterReg in self.__registers:
						self.insertConnection(iterlAfter, iterReg)
			lAfter = node.liveSetBefore

	def printGraph(self):
		myString = ""
		for node in self.__theGraph.keys():
			myString = myString + str(node) + "--> [" + ','.join([ str(node_connection) for node_connection in self.__theGraph[node] ]) + "]\n"
		return myString
		
