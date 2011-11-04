from heapq import *
import itertools
import random
class HeapPriorityQueue(object):
	pq = []
	entry_finder = {}
	REMOVED = '<removed-task>'
	counter = 0
	tie_breaker = itertools.count()
	
	def __init__(self,useRandomNonce=False):
		self.entry_finder = {}
		self.pq = []
		heapify(self.pq)
		self.counter = len(self.pq)
		#useRandomNonce is a random tie-breaker, to prevent deadlock in register allocation
		self.useRandomNonce = useRandomNonce

	def add_task(self,priority,task):
		if task in self.entry_finder:
			self.remove_task(task)
		tb = next(self.tie_breaker)
		randomNonce = 0
		if self.useRandomNonce:
			randomNonce = random.randint(0,10)
		entry = [task.spillable, priority, randomNonce, tb, "", task]
		self.entry_finder[task] = entry
		heappush(self.pq,entry)
		self.counter += 1

	def remove_task(self,task):
		entry = self.entry_finder.pop(task)
		entry[-2] = self.REMOVED
		self.counter -= 1

	def pop_task(self):
		while self.pq:
			entry = heappop(self.pq)
			task = entry[-1]
			removed = entry[-2]
			if removed != self.REMOVED:
				del self.entry_finder[task]
				self.counter -= 1
				return task
		raise KeyError('pop from an empty priority queue')

	def __len__(self):
		return self.counter
	
	def empty(self):
		return not self.counter
	def __repr__(self):
		#pretty print heap
		retVal = ""
		for element in self.pq:
			priority, tb, removed, node = element
			if removed != self.REMOVED:
				retVal += "-->"+str(node)+" with priority of: "+str(priority)
		return retVal
