from p2heapify import *

class P3Heapify(P2Heapify):
	# Visitor Methods: #########################################################################################
	# Trivial pass throughs:
	def visit_While(self, ast):
		(testFreeBelow, testBody) = self.visit(ast.test)
		(bodyFreeBelow, bodyBody) = self.visit(ast.body)
		return (testFreeBelow + bodyFreeBelow, While(testBody, bodyBody, None))
	
	def visit_If(self, ast):
		# tests is a list of tuples. The first element of the tuple is a test.
		# the second element is the "then" (what executes if the test passes)
		(testFreeBelow, testBody) = self.visit(ast.tests[0][0])
		(thenFreeBelow, thenBody) = self.visit(ast.tests[0][1])
		(else_FreeBelow, else_Body) = self.visit(ast.else_)
