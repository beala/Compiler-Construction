from heapq import *
import itertools
class HeapPriorityQueue(object):
	pq = []
	entry_finder = {}
	REMOVED = '<removed-task>'
	counter = 0
	def __init__(self, heapifyMe):
		self.entry_finder = {}
		self.pq = heapifyMe
		heapify(self.pq)

	def add_task(self,task):
		if task in self.entry_finder:
			remove_task(task)
		entry = task
		self.entry_finder[task] = entry
		heappush(self.pq,entry)
		counter += 1

	def remove_task(self,task):
		entry = self.entry_finder.pop(task)
		entry = REMOVED
		counter -= 1

	def pop_task(self):
		while self.pq:
			task = heappop(self.pq)
			if task is not REMOVED:
				del self.entry_finder[task]
				return task
		raise KeyError('pop from an empty priority queue')

	def __len__(self):
		return counter
	
	def empty(self):
		return not counter
