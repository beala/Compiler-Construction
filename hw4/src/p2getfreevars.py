from astvisitor import *
from p2getlocals import *
debug = False
class P2GetFreeVars(ASTVisitor):
	_reservedNames = ['input', 'type_error']
	#return a set of strings - free variable names
	def visit_Module(self, node):
		freeVars = self.visit(node.node)
		localVars = P2GetLocals().getLocals(node)
		return freeVars - set(localVars)
	def visit_Stmt(self, node):
		freeVars = set()
		for stmt in node.nodes:
			freeVars |= self.visit(stmt)
		return freeVars
	def visit_Lambda(self, node):
		freeVars = self.visit(node.code)
		localVars = P2GetLocals().getLocals(node)
		if debug:
			print str(node.argnames) + ": " + str(freeVars - set(localVars) - set(node.argnames))
		return freeVars - set(localVars) - set(node.argnames)
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
		if node.node.name in self._reservedNames:
			return set([])
		argSet = set([])
		for element in node.args:
			argSet |= self.visit(element)
		nameSet = self.visit(node.node)
		return argSet | nameSet
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

if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	print "-"*20 + "Parsed AST" + "-"*20 
	if os.path.isfile(sys.argv[1]):
		print compiler.parseFile(sys.argv[1])
		to_explicate = compiler.parseFile(sys.argv[1])
	else:
		print compiler.parse(sys.argv[1])
		to_explicate = compiler.parse(sys.argv[1])
	print "-"*20 + "Uniquified AST" + "-"*20
	to_explicate = P2Uniquify().visit(to_explicate)
	P2Uniquify().print_ast(to_explicate.node)
	print "-"*20 + "Explicated AST" + "-"*20
	explicated = P2Explicate().visit(to_explicate)
	P2Uniquify().print_ast(explicated.node)
	print "-"*20 + "Free Vars List" + "-"*20
	debug = True
	P2GetFreeVars().visit(explicated)
