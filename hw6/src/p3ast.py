from compiler.ast import *

class CreateClass(Node):
	bases = None
	def __init__(self, bases):
		self.bases = bases
	def __repr__(self):
		return "CreateClass(" + str(self.bases) + ")"
