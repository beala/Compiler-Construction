from compiler.ast import *

class CreateClass(Node):
	bases = None
	def __init__(self, bases):
		self.bases = bases
	def __repr__(self):
		return "CreateClass(" + str(self.bases) + ")"
class HasAttr(Node):
	def __init__(self, expr, attrname):
		self.expr = expr
		self.attrname = attrname
	def __repr__(self):
		return "HasAttr(" + str(self.expr) + ", " + str(self.attrname) + ")"
