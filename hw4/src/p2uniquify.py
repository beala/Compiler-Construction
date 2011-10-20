from compiler import *
from compiler.ast import *

class ASTVisitor(object):
	def visit(self, node, curScopeDict={}):
		'''Visit a node'''
		# Find a specific visit method. Default to "default".
		methname = "visit_%s" % node.__class__.__name__
		method = getattr(self, methname, self.default)
		return method(node, curScopeDict)
    
	def default(self, node):
		'''Visit node children'''
		print "Uh oh: A method doesn't exist for this node type: %s" % node.__class__.__name__

class P2Uniquify(ASTVisitor):
	globalCounter = 0
	# Private Functions: ######################################################################################

	def _getLocals(self, node):
		local_vars = []
		if isinstance(node, Assign):
			local_vars += [node.nodes[0].name]
			return local_vars
		elif isinstance(node, Function):
			local_vars += [node.name]
			local_vars += node.argnames
			for stmt in node.code.nodes:
				local_vars += self._getLocals(stmt)
			return local_vars
		elif isinstance(node, Lambda):
			local_vars += node.argnames
			local_vars += self._getLocals(node.code)
			return local_vars
		elif isinstance(node, Module):
			for stmt in node.node.nodes:
				local_vars += self._getLocals(stmt)
			return local_vars
		elif isinstance(node, IfExp):
			# I don't think there can be an assign inside IfExpr, but just in case...
			local_vars += self._getLocals(node.test)
			local_vars += self._getLocals(node.then)
			local_vars += self._getLocals(node.else_)
			return local_vars
		return []
		#else:
		#	raise TypeError("Uh oh! What's a " + str(node.__class__.__name___) + "????")
				
	# Desc:	Returns a list of variables that are local to the scope it's given.
	# Args:	stmt_list: A list of AST nodes that represents an arbitrary scope.
	#			This is usually from the 'code' attribute within a Lambda
	#			or Function node.
	# Ret:	A set of variable names that are local to the given scope.
	def _getLocalsOLD(self,stmt_node):
		#get anything that is assigned-to
		#assume ast is a statement node (list of statements)
		# List which will hold the names of all local variables.
		local_vars = []

		for stmt in stmt_node.nodes:
			# If it's on the LHS of an assignment, then it's local to this scope.
			if isinstance(stmt, Assign):
				local_vars += [stmt.nodes[0].name]
			# Recurse into new scopes (functions and lambdas) and get their local vars,
			# and add to the current list of local vars.
			elif isinstance(stmt, Function):
				local_vars += [stmt.name] # For uniquifying function names
				local_vars += [element.name for element in stmt.argnames] # Args count as an assignment
				local_vars += self._getLocals(stmt.code)
			elif isinstance(stmt, Lambda):
				local_vars += [element.name for element in stmt.argnames] # Args count as an assignment
				local_vars += self._getLocals(stmt.code) # Lambdas only have one stmt, not a stmt_list
			# Although it's technically not a new scope, we must recurse into IfExp
			# to see if any assignments occur inside.
			elif isinstance(stmt, IfExp):
				local_vars += self._getLocals(stmt.test)
				local_vars += self._getLocals(stmt.then)
				local_vars += self._getLocals(stmt.else_)

		return set(local_vars) # Return a set to remove duplicates

	def rename(self, curScopeDict, nameNode):
		nameNode.name = curScopeDict[nameNode.name]

	def renameStr(self, curScopeDict, nameStr):
		return curScopeDict[nameStr]

	def uniquifyLocalNames(self, localList, curScopeDict):
		for var in localList:
			curScopeDict[var] = "{"+var+str(self.globalCounter)
			self.globalCounter += 1

	# Visitor Functions: #######################################################################################

	def visit_Lambda(self, ast, curScopeDict):
		# Convert all Lambdas to contain a Stmt node in the 'code' attribute to mirror
		# Function nodes.
		#newRet = Return(ast.code)
		#ast = Lambda([Name(name) for name in ast.argnames] , ast.defaults, ast.flags, Stmt([newRet]))
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		ast.code = self.visit(ast.code, curScopeDict)
		# Can't write directly to argname (don't know why) so make a new
		# argname_list and assign to ast.argnames
		argname_list = []
		for argname in ast.argnames:
			argname_list += [self.renameStr(curScopeDict, argname)]
		ast.argnames = argname_list
		return ast
	def visit_Function(self, ast, curScopeDict):
		#ast = Function(ast.decorators, Name(ast.name), [Name(name) for name in ast.argnames], ast.defaults, ast.flags, ast.doc, ast.code) 
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		ast.code = self.visit(ast.code, curScopeDict)
		# Can't write directly to argname (don't know why) so make a new
		# argname_list and assign to ast.argnames
		argname_list = []
		for argname in ast.argnames:
			argname_list  += [self.renameStr(curScopeDict, argname)]
		ast.argnames = argname_list
		ast.name = self.renameStr(curScopeDict, ast.name)
		return ast
	def visit_Module(self, ast, curScopeDict={}):
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		ast.node = self.visit(ast.node, curScopeDict)
		return ast
	def visit_Return(self, ast, curScopeDict):
		ast.value = self.visit(ast.value, curScopeDict)
		return ast
	def visit_Stmt(self, ast, curScopeDict):
		for node in ast.nodes:
			node = self.visit(node, curScopeDict)
		return ast
	def visit_Name(self, ast, curScopeDict):
		if not (ast.name == 'True' or ast.name == 'False'):
			ast.name = self.renameStr(curScopeDict, ast.name)
		return ast
	def visit_AssName(self, ast, curScopeDict):
		self.rename(curScopeDict, ast)
		return ast
	
	def visit_Const(self, ast, curScopeDict):
		return ast
	def visit_IfExp(self, ast, curScopeDict):
		ast.test = self.visit(ast.test, curScopeDict)
		ast.then = self.visit(ast.then, curScopeDict)
		ast.else_ = self.visit(ast.else_, curScopeDict)
		return ast
	def visit_UnarySub(self, ast, curScopeDict):
		ast.expr = self.visit(ast.expr, curScopeDict)
		return ast
	def visit_Add(self, ast, curScopeDict):
		ast.left = self.visit(ast.left, curScopeDict)
		ast.right = self.visit(ast.right, curScopeDict)
		return ast
	def visit_Discard(self, ast, curScopeDict):
		ast.expr = self.visit(ast.expr, curScopeDict)
		return ast
	def visit_Printnl(self, ast, curScopeDict):
		ast.nodes[0] = self.visit(ast.nodes[0], curScopeDict)
		return ast
	def visit_And(self, ast, curScopeDict):
		for operand in ast.nodes:
			operand = self.visit(operand, curScopeDict)
		return operand
	def visit_Or(self, ast, curScopeDict):
		for operand in ast.nodes:
			operand = self.visit(operand, curScopeDict)
		return ast
	def visit_Not(self, ast, curScopeDict):
		ast.expr = self.visit(ast.expr, curScopeDict)
		return ast
	def visit_List(self, ast, curScopeDict):
		for element in ast.nodes:
			element = self.visit(element, curScopeDict)
		return ast
	def visit_Dict(self, ast, curScopeDict):
		for element in ast.items:
			element[0] = self.visit(element[0], curScopeDict)
			element[1] = self.visit(element[1], curScopeDict)
		return ast
	def visit_Subscript(self, ast, curScopeDict):
		ast.expr = self.visit(ast.expr, curScopeDict)
		for sub in ast.subs:
			sub = self.visit(sub, curScopeDict)
		return ast
	def visit_Compare(self, ast, curScopeDict):
		ast.expr = self.visit(ast.expr, curScopeDict)
		ast.ops[1] = self.visit(ast.ops[1], curScopeDict)
		return ast
	def visit_CallFunc(self, ast, curScopeDict):
		ast.node = self.visit(ast.node, curScopeDict)
		for arg in ast.args:
			arg = self.visit(arg, curScopeDict)
		return ast
	def visit_Assign(self, ast, curScopeDict):
		ast.nodes[0] = self.visit(ast.nodes[0], curScopeDict)
		ast.expr = self.visit(ast.expr, curScopeDict)
		return ast

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
				print '\t' * tabcount + 'Lambda (' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]), tabcount+1)
				print '\t' * tabcount + 'EndLambda'
			if isinstance(node, Function):
				print '\t' * tabcount + 'def ' + str(node.name) + '(' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]), tabcount+1)
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
		ast = compiler.parseFile(sys.argv[1])
		P2Uniquify().visit(ast)
	else:
		print str(compiler.parse(sys.argv[1])) + '\n'
		ast = compiler.parse(sys.argv[1])
		P2Uniquify().visit(ast)
	print '-' * 10 + 'Uniquified AST' + '-' * 10
	p1flattener.P1ASTFlattener().print_ast(ast.node, 0)
