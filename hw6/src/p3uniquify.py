from p2uniquify import *
from p3ast import *
class P3Uniquify(P2Uniquify):
	# Private Functions: ###############################################################

	# Desc: Take a variable name that hasn't be renamed yet, and return
	#			what it should be renamed to.
	# Args:	A variable's name, as a string.
	# Ret:	The variable's new uniquified name (as a string).
	def renameToUnique(self, curScopeDict, nameStr):
		if curScopeDict.has_key(nameStr):
			return curScopeDict[nameStr]
		else:
			return nameStr
	
	def visit_If(self, ast, curScopeDict):
		newTests = [(self.visit(ast.tests[0][0], curScopeDict), self.visit(ast.tests[0][1], curScopeDict))]
		ast.tests = newTests
		ast.else_ = self.visit(ast.else_, curScopeDict)
		return ast
	def visit_While(self, ast, curScopeDict):
		ast.test = self.visit(ast.test, curScopeDict)
		ast.body = self.visit(ast.body, curScopeDict)
		return ast
	# This should only get called if the Stmt node is nested in something
	# without a scope change (like IF or WHILE). If there's a scope change,
	# the curScopeDict needs to be deepcopied (see _visit_Stmt_Deepcopy)
	def visit_Stmt(self, ast, curScopeDict):
		newStmtList = []
		for node in ast.nodes:
			newStmtList.append(self.visit(node,curScopeDict))
		return Stmt(newStmtList)
	def visit_CreateClass(self, ast, curScopeDict):
		newBases = []
		for node in ast.bases:
			newBases.append(self.visit(node, curScopeDict))
		return CreateClass(newBases)
	def visit_AssAttr(self, ast, curScopeDict):
		newExpr = self.visit(ast.expr, curScopeDict)
		return AssAttr(newExpr, ast.attrname, ast.flags)
	def visit_Getattr(self, ast, curScopeDict):
		newExpr = self.visit(ast.expr, curScopeDict)
		return Getattr(newExpr, ast.attrname)
	def visit_HasAttr(self, ast, curScopeDict):
		newExpr = self.visit(ast.expr, curScopeDict)
		return HasAttr(newExpr, ast.attrname)
	# Debugging methods: #############################################################################
	def print_ast(self, stmt_ast, tabcount=0):
		for node in stmt_ast.nodes:
			if isinstance(node, If):
				print '\t' * tabcount + 'If: ' + str(node.tests[0][0]) + ' then:'
				self.print_ast(node.tests[0][1], tabcount+1)
				print '\t' * (tabcount) + 'Else: '
				self.print_ast(node.else_, tabcount+1)
				print '\t' * (tabcount) + 'End If'
			elif isinstance(node, While):
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
