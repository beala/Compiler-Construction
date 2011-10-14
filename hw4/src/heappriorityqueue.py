from heapq import *
import itertools
class HeapPriorityQueue(object):
	pq = []
	entry_finder = {}
	REMOVED = '<removed-task>'
	counter = 0
	tie_breaker = itertools.count()
	
	def __init__(self):
		self.entry_finder = {}
		self.pq = []
		self.counter = len(self.pq)

	def add_task(self,priority,task):
		if task in self.entry_finder:
			self.remove_task(task)
		tb = next(self.tie_breaker)
		entry = [priority, tb, "", task]
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
