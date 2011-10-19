from astvisitor import *

class P2Uniquify(ASTVisitor):
	globalCounter = 0
	# Private Functions: ######################################################################################

	# Desc:	Returns a list of variables that are local to the scope it's given.
	# Args:	stmt_list: A list of AST nodes that represents an arbitrary scope.
	#			This is usually from the 'code' attribute within a Lambda
	#			or Function node.
	# Ret:	A set of variable names that are local to the given scope.
	def _getLocals(self,stmt_node):
		#get anything that is assigned-to
		#assume ast is a statement node (list of statements)
		# List which will hold the names of all local variables.
		local_vars = []

		for stmt in stmt_node.nodes:
			# If it's on the LHS of an assignment, then it's local to this scope.
			if isinstance(stmt, Assign)
				local_vars += [stmt.nodes[0].name]
			# Recurse into new scopes (functions and lambdas) and get their local vars,
			# and add to the current list of local vars.
			elif isinstance(stmt, Function):
				local_vars += [stmt.argnames] # Args count as an assignment
				local_vars += self._getLocals(stmt.code)
			elif isinstance(stmt, Lambda):
				local_vars += [stmt.argnames] # Args count as an assignment
				local_vars += self._getLocals([stmt.code]) # Lambdas only have one stmt, not a stmt_list
			# Although it's technically not a new scope, we must recurse into IfExp
			# to see if any assignments occur inside.
			elif isinstance(stmt, IfExp):
				local_vars += self._getLocals(stmt.test)
				local_vars += self._getLocals(stmt.then)
				local_vars += self._getLocals(stmt.else_)

		return set(local_vars) # Return a set to remove duplicates

	def rename(self, curScopeDict, nameNode):
		nameNode.name = curScopeDict[nameNode.name]
	def uniquifyLocalNames(self, localList, curScopeDict):
		for var in localList:
			curScopeDict[var] = "{"+var+self.globalCounter
			self.globalCounter += 1
	# Visitor Functions: #######################################################################################

	def visit_Lambda(self, ast, curScopeDict):
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		self.visit(ast.code, curScopeDict)
	def visit_Function(self, ast, curScopeDict):
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		self.visit(ast.code, curScopeDict)
	def visit_Module(self, ast, curScopeDict={}):
		localVars = self._getLocals(ast.node)
		self.uniquifyLocalNames(localVars, curScopeDict)
		self.visit(ast.node, curScopeDict)
	def visit_Return(self, ast, curScopeDict):
		self.visit(ast.value, curScopeDict)
	def visit_Stmt(self, ast, curScopeDict):
		for node in ast.nodes:
			self.visit(ast.node, curScopeDict)
	def visit_Name(self, ast, curScopeDict):
		self.rename(curScopeDict, ast)
	def visit_AssName(self, ast, curScopeDict):
		self.rename(curScopeDict, ast)
	
	def visit_Const(self,ast, curScopeDict):
		pass
	def visit_IfExp(self, ast, curScopeDict):
		self.visit(ast.test, curScopeDict)
		self.visit(ast.then, curScopeDict)
		self.visit(ast.else_, curScopeDict)
	def visit_UnarySub(self, ast, curScopeDict):
		self.visit(ast.expr, curScopeDict)
	def visit_Add(self, ast, curScopeDict):
		self.visit(ast.left, curScopeDict)
		self.visit(ast.right, curScopeDict)
	def visit_Discard(self, ast, curScopeDict):
		self.visit(ast.expr, curScopeDict)
	def visit_Printnl(self, ast, curScopeDict):
		self.visit(ast.nodes[0], curScopeDict)
	def visit_And(self, ast, curScopeDict):
		for operand in ast.nodes:
			self.visit(operand, curScopeDict)
	def visit_Or(self, ast, curScopeDict):
		for operand in ast.nodes:
			self.visit(operand, curScopeDict)
	def visit_Not(self, ast, curScopeDict):
		self.visit(ast.expr, curScopeDict)
	def visit_List(self, ast, curScopeDict):
		for element in ast.nodes:
			self.visit(element, curScopeDict)
	def visit_Dict(self, ast, curScopeDict):
		for element in ast.items:
			self.visit(element[0], curScopeDict)
			self.visit(element[1], curScopeDict)
	def visit_Subscript(self, ast, curScopeDict):
		self.visit(ast.expr, curScopeDict)
		for sub in ast.subs
			self.visit(sub, curScopeDict)
	def visit_Compare(self, ast, curScopeDict):
		self.visit(ast.expr, curScopeDict)
		self.visit(ast.ops[1], curScopeDict)
	def visit_CallFunc(self, ast, curScopeDict):
		self.visit(ast.node, curScopeDict)
		for arg in ast.args:
			self.visit(arg, curScopeDict)
	def visit_Assign(self, ast, curScopeDict):
		self.visit(ast.nodes[0], curScopeDict)
		self.visit(ast.expr, curScopeDict)

	# Debugging methods: #############################################################################
	def print_ast(self, stmt_ast, tabcount):
		for node in stmt_ast.nodes:
			if isinstance(node, If):
				print '\t' * tabcount + 'If: ' + str(node.tests[0][0]) + ' then:'
				self.print_ast(node.tests[0][1], tabcount+1)
				print '\t' * (tabcount) + 'Else: '
				self.print_ast(node.else_, tabcount+1)
				print '\t' * (tabcount) + 'End If'
			if isinstance(node, Lambda):
				print \t * tabcount + 'Lambda (' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]))
				print '\t' * tabcount + 'EndLambda'
			if isinstance(node, Function):
				print \t * tabcount + 'def ' + str(node.name) + '(' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]))
				print '\t' * tabcount + 'EndFunc'
			else:
				print '\t' * (tabcount) + str(node)

if __name__ == "__main__":
	import sys 
	import compiler
	print '-' * 10 + 'Parsed AST' + '-' * 10
	import os
	import p1flattener
	if os.path.isfile(sys.argv[1]):
		print str(compiler.parseFile(sys.argv[1])) + '\n'
		unique_ast = P2Uniquify().visit(compiler.parseFile(sys.argv[1]))
	else:
		print str(compiler.parse(sys.argv[1])) + '\n'
		unique_ast = P2Uniquify().visit(compiler.parse(sys.argv[1]))
	print '-' * 10 + 'Uniquified AST' + '-' * 10
	p1flattener.P1ASTFlattener().print_ast(unique_ast.node, 0)
