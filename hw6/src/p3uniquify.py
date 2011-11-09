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
	
	# Debugging methods: #############################################################################
	def print_ast(self, stmt_ast, tabcount=0):
		for node in stmt_ast.nodes:
			if isinstance(node, If):
				print '\t' * tabcount + 'If: ' + str(node.tests[0][0]) + ' then:'
				self.print_ast(node.tests[0][1], tabcount+1)
				print '\t' * (tabcount) + 'Else: '
				self.print_ast(node.else_, tabcount+1)
				print '\t' * (tabcount) + 'End If'
			if isinstance(node, While):
				print '\t' * tabcount + 'While: ' + str(node.test) + ' then:'
				self.print_ast(node.body, tabcount+1)
				print '\t' * (tabcount) + 'End While'
			elif isinstance(node, Lambda):
				print '\t' * tabcount + 'Lambda (' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]), tabcount+1)
				print '\t' * tabcount + 'EndLambda'
			elif isinstance(node, Function):
				print '\t' * tabcount + 'def ' + str(node.name) + '(' + str(node.argnames) + '):'
				self.print_ast(node.code, tabcount+1)
				print '\t' * tabcount + 'EndFunc'
			else:
				print '\t' * (tabcount) + str(node)
