from astvisitor import *

class P2GetFreeVars(ASTVisitor):
	#return a set of strings - free variable names
	def visit_Module(self, node):
		freeVars = self.visit(node.node)
		return freeVars - set(node.localVars)
	def visit_Stmt(self, node):
		freeVars = set()
		for stmt in node.nodes:
			freeVars |= self.visit(stmt)
		return freeVars
	def visit_Lambda(self, node):
		freeVars = self.visit(node.code)
		return freeVars - set(node.localVars) - set(node.argnames)
	def visit_Name(self, node):
		if node.name == 'True' or node.name == 'False':
			return set([])
		return set([node.name])

	#the rest are boring functions that just recurse on their child nodes
	def visit_Printnl(self, node):
		return self.visit(node.nodes[0])
	def visit_Const(self, node):
		return set([])
	def visit_Assign(self, node):
		return self.visit(node.expr)
	def visit_AssName(self, node):
		return set([])
	def visit_CallFunc(self, node):
		#at this stage, CallFunc are only runtime functions?
		argSet = set([])
		for element in node.args:
			argSet |= self.visit(element)
		#nameSet = self.visit(node.node)
		return argSet #| nameSet
	def visit_Add(self, node):
		return self.visit(node.left) | self.visit(node.right)
	def visit_IntegerAdd(self, node):
		return self.visit(node.left) | self.visit(node.right)
	def visit_BigAdd(self, node):
		return self.visit(node.left) | self.visit(node.right)
	def visit_UnarySub(self, node):
		return self.visit(node.expr)
	def visit_Or(self, node):
		return self.visit_List(node)
	def visit_And(self, node):
		return self.visit_List(node)
	def visit_Not(self, node):
		return self.visit(node.expr)
	def visit_Compare(self, node):
		returnSet = set([])
		returnSet |= self.visit(node.expr)
		returnSet |= self.visit(node.ops[0][1])
		return returnSet
	def visit_IntegerCompare(self, node):
		returnSet = set([])
		returnSet |= self.visit(node.expr)
		returnSet |= self.visit(node.ops[0][1])
		return returnSet
	def visit_BigCompare(self,node):
		returnSet = set([])
		returnSet |= self.visit(node.expr)
		returnSet |= self.visit(node.ops[0][1])
		return returnSet
	def visit_IfExp(self, node):
		return self.visit(node.test) | self.visit(node.then) | self.visit(node.else_)
	def visit_List(self, node):
		returnSet = set([])
		for expr in node.nodes:
			returnSet |= self.visit(expr)
		return returnSet
	def visit_Dict(self, node):
		returnSet = set([])
		for (key, value) in node.items:
			returnSet |= self.visit(key)
			returnSet |= self.visit(value)
		return returnSet
	def visit_Subscript(self, node):
		return self.visit(node.expr) | self.visit(node.subs[0])
	def visit_Return(self, node):
		return self.visit(node.value)
	def visit_Let(self, node):
		return (self.visit(node.rhs) | self.visit(node.body)) - self.visit(node.var)
	def visit_InjectFrom(self, node):
		return self.visit(node.typ) | self.visit(node.arg)
	def visit_ProjectTo(self, node):
		return self.visit_InjectFrom(node)
	def visit_GetTag(self, node):
		return self.visit(node.arg)
	def visit_Discard(self, node):
		return self.visit(node.expr)
	def visit_CallUserDef(self, node):
		argSet = set([])
		for element in node.args:
			argSet |= self.visit(element)
		nameSet = self.visit(node.node)
		return argSet | nameSet
	def visit_CreateClosure(self, node):
		return self.visit(node.name) | set(node.env)
	def visit_BigAdd(self, node):
		return self.visit_Add(node)
	def visit_IntegerAdd(self, node):
		return self.visit_Add(node)

