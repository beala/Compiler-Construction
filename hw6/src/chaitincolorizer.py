#Graph colorizer based on Chaitin's O(nlog(n)) coloring algorithm
#Written by Josh Wepman, joshua.wepman@colorado.edu
from heappriorityqueue import * #we use a heapq to store sorted list of nodes by degree < k
import copy
from x86 import *
class ChaitinColorizer(object):
	theGraph = {} #nodes to list of edges
	heapQueue = None #heapified PQ of nodes by degree
	colorMap = {} #list of colors (registers input, addt'l colors added as necessary color => register name or stack location
	stackOffset = 4
	def __init__(self, graph, colors={1:'eax',2:'ebx',3:'ecx',4:'edx'}):
		self.theGraph = copy.copy(graph)
		self.copyGraph = copy.copy(graph)
		self.colorMap = colors
		self.heapQueue = HeapPriorityQueue(True)
		for node in self.theGraph.keys():
			if (not isinstance(node, VarNode)) or node.color != -1:
				continue
			self.heapQueue.add_task(len(self.theGraph[node]),node)
	def doColor(self):
		curNode = None
		myColorStack = []
		mySpillStack = []
			
		while not self.heapQueue.empty():
			curNode = self.heapQueue.pop_task() 
			myLen = 0
			try:
				myLen = len(self.theGraph[curNode])
			except KeyError:
				pass
			if myLen > len(self.colorMap):
				myColorStack.append(curNode)
			else:
				mySpillStack.append(curNode)
			self.doRemoveNodeConnections(curNode)
		#pop stack and colorize!
		while len(myColorStack) > 0:
			curNode = myColorStack.pop()
			try:
				curNode.color = self.doCalculateLowestAvailColor(curNode)
			except ValueError:
				mySpillStack.insert(0,curNode)
		while len(mySpillStack) > 0:
			curNode = mySpillStack.pop()
			try:
				curNode.color = self.doCalculateLowestAvailColor(curNode)
			except ValueError:
				#spill forced
				curNode.color = self.addNewColor()
		#at this point, all nodes have been colored!
		return self.colorMap
	def doCalculateLowestAvailColor(self,node):
		if len(self.copyGraph[node]) == 0:
			return 1
		adjacentColors = set([])
		try:
			for myNeighbor in self.copyGraph[node]:
				if myNeighbor.color == -1:
					continue
				adjacentColors.add(myNeighbor.color)
			for element in sorted(self.colorMap.keys()):
				if element not in adjacentColors:
					return element
		except KeyError:
			#first color works :)
			raise KeyError("Some weird key error trying to find lowest avail color")
		raise ValueError("No suitable color found :(")
	def addNewColor(self):
		newColor = (4 + (self.stackOffset/4)) 
		self.colorMap[newColor] = self.stackOffset
		self.stackOffset += 4
		return newColor
	def doRemoveNodeConnections(self,node):
		#remove a node and all of its connections from the graph
		try:
			connectedList = copy.copy(self.copyGraph[node])
			for connectedElement in connectedList:
				try:
					self.theGraph[connectedElement].remove(node)
					if not isinstance(connectedElement, VarNode):
						continue
					self.heapQueue.add_task(len(self.theGraph[connectedElement]), connectedElement) #update the heapqueue with new degree
				except ValueError:
					raise ValueError("Not in graph...hmmmm")
					#continue #somehow not in graph :S
			del self.theGraph[node]
		except KeyError:
			return #already not in graph :)
	
	
