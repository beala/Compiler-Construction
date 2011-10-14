from heapq import *
import itertools
class HeapPriorityQueue(object):
	pq = []
	entry_finder = {}
	REMOVED = '<removed-task>'
	counter = 0
	def __init__(self):
		self.entry_finder = {}
		self.pq = []
		self.counter = len(self.pq)
	def add_task(self,priority,task):
		if task in self.entry_finder:
			self.remove_task(task)
		entry = [priority, task]
		self.entry_finder[task] = entry
		heappush(self.pq,entry)
		self.counter += 1

	def remove_task(self,task):
		entry = self.entry_finder.pop(task)
		entry[1] = self.REMOVED
		self.counter -= 1

	def pop_task(self):
		while self.pq:
			entry = heappop(self.pq)
			task = entry[1]
			if task != self.REMOVED:
				del self.entry_finder[task]
				self.counter -= 1
				return task
		raise KeyError('pop from an empty priority queue')

	def __len__(self):
		return self.counter
	
	def empty(self):
		return not self.counter
