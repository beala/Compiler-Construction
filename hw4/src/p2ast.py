from compiler.ast import *

class CreateClosure(Node):
	name = None
	env = None
	def __init__(self, name, env):
		self.name = name
		self.env = env
	def __repr__(self)
		return "CreateClosure(" + str(self.name) + " ," + str(self.env) + ")"

class CallUserDef(CallFunc):
	def __repr__(self):
		return 'CallUserDef(' + str(self.node) + " ," + str(self.args) + ")"

class LocalVars(Node):
	local_vars = []
	def __init__(self, local_vars)
		self.local_vars = local_vars
	def __repr__(self):
		return 'LocalVars(' + str(self.local_vars) + ')'

class GetFunPtr(Node):
	name = None
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return 'GetFunPtr(' + str(self.name) + ')'

class GetFreeVars(Node):
	name = None
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return 'GetFreeVars(' + str(self.name) + ')'
