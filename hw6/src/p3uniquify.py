from p2uniquify import *

class P3Uniquify(P2Uniquify):
	def visit_If(self, ast, curScopeDict):
		newTests = [(self.visit(ast.tests[0][0], curScopeDict), self.visit(ast.tests[0][1], curScopeDict))]
		ast.tests = newTests
		ast.else_ = self.visit(ast.else_)
		return ast
	def visit_While(self, ast, curScopeDict):
		ast.test = self.visit(ast.test)
		ast.body = self.visit(ast.body)
		return ast
	# This should only get called if the Stmt node is nested in something
	# without a scope change (like IF or WHILE). If there's a scope change,
	# the curScopeDict needs to be deepcopied (see _visit_Stmt_Deepcopy)
	def visit_Stmt(self, ast, curScopeDict):
		newStmtList = []
		for node in ast.nodes:
			newStmtList.append(self.visit(node,curScopeDict))
		return Stmt(newStmtList)
