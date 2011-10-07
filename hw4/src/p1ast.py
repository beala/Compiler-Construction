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
		self.body = body
	def __repr__(self):
		return 'Let(' + str(self.var) + ', ' + str(self.rhs) + ', ' + str(self.body) + ')'

class IntegerAdd(Add):
	def __repr__(self):
		return 'IntegerAdd((' + str(self.left) + ', ' + str(self.right) + '))'

class BigAdd(Add):
	def __repr__(self):
		return 'BigAdd((' + str(self.left) + ', ' + str(self.right) + '))'
