from p2flattener import *
class P3ASTFlattener(P2ASTFlattener):
	def visit_If(self, node):
		(fe1, se1) = self.visit(node.tests[0][0])
		se2 = self.visit(node.tests[0][1]) #is a Stmt node
		se3 = self.visit(node.else_) #is a Stmt node
		newIf = If([(fe1, se2)], se3)
		return se1 + [newIf]
	def visit_While(self, node):
		(fe1, se1) = self.visit(node.test)
		se2 = self.visit(node.body) #is a Stmt node
		return se1 + [While(fe1, se2, None)]

