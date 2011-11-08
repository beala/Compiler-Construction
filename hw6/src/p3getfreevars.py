from p2getfreevars import *
class P3GetFreeVars(P2GetFreeVars):
	def visit_If(self, node):
		return self.visit(node.tests[0][0]) | self.visit(node.tests[0][1]) | self.visit(node.else_)	
	def visit_While(self, node):
		#body is a statement, but this works because P2GetFreeVars only indicates a scope change on Module or Lambda, not Stmt nodes
		return self.visit(node.test) | self.visit(node.body)
