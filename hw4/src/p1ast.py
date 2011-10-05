from compiler.ast import *

class GetTag(Node):
	def __init__(self, arg):
		self.arg = arg
	def __repr__(self):
		return 'GetTag(' + str(self.arg) + ')'

class InjectFrom(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def __repr__(self):
		return 'InjectFrom(' + str(self.typ) + ', ' + str(self.arg) + ')'

class ProjectTo(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def __repr__(self):
		return 'ProjectTo(' + str(self.typ) + ', ' + str(self.arg) + ')'

class Let(Node):
	def __init__(self, var, rhs, body):
		self.var = var
		self.rhs = rhs
		self.body = bod
	def __repr__(self):
		return 'Let(' + str(self.var) + ', ' + str(self.rsh) + ', ' + str(self.body) + ')'

class IntegerAdd(Add):
	def __repr__(self):
		return 'IntegerAdd((' + str(self.left) + ', ' + str(self.right) + '))'
