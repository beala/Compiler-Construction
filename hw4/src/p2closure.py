from astvisitor import *

class P2Closure(ASTVisitor):
	_globalFunctionCounter = 0
	def _makeGlobalName(self):
		self._globalFunctionCounter += 1
		return "lambda"+str(self._globalFunctionCounter)
	def visit_Module(self, node):
		(body, funs) = self.visit(node.node)
		return Module(node.doc, body), funs
	def visit_Stmt(self, node):
		nodeList = []
		funList = []
		for element in node.nodes:
			(stmt, funs) = self.visit(element)
			nodeList.append(stmt)
			funList.extend(funs)
		return Stmt(nodeList), funs
	def visit_Lambda(self, node):
		globalName = self._makeGlobalName()
	
	
	def visit_Printnl(self, node):
	def visit_Const(self, node):
	def visit_Assign(self, node):
	def visit_AssName(self, node):
	def visit_CallFunc(self, node):
	def visit_Add(self, node):
	def visit_UnarySub(self, node):
	def visit_Or(self, node):
	def visit_And(self, node):
	def visit_Not(self, node):
	def visit_Compare(self, node):
	def visit_IfExp(self, node):
	def visit_List(self, node):
	def visit_Dict(self, node):
	def visit_Subscript(self, node)
	def visit_Return(self, node):
	def visit_Let(self, node):
	def visit_InjectFrom(self, node):
	def visit_ProjectTo(self, node):
	def visit_GetTag(self, node):
	def visit_Discard(self, node):
	def visit_CallUserDef(self, node):
	def visit_CreateClosure(self, node):
	def visit_BigAdd(self, node):
	def visit_IntegerAdd(self, node):
