from compiler import *
from compiler.ast import *
import copy
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
	# Private Attributes: #####################################################################################
	uniqueNameCounter = 0
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

	def renameToUnique(self, curScopeDict, nameStr):
		return curScopeDict[nameStr]

	def uniquifyLocalNames(self, localList, curScopeDict):
		for var in localList:
			curScopeDict[var] = var+str(self.uniqueNameCounter)+"*"
			self.uniqueNameCounter += 1

	# Visitor Functions: #######################################################################################

	def visit_Lambda(self, ast, curScopeDict):
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		# Need to pass in a copy of curScopeDict or else subscopes will change the dict
		# of the current scope.
		ast.code = self.visit(ast.code, copy.deepcopy(curScopeDict))
		# Can't write directly to argname (don't know why) so make a new
		# argname_list and assign to ast.argnames
		argname_list = []
		for argname in ast.argnames:
			argname_list += [self.renameToUnique(curScopeDict, argname)]
		ast.argnames = argname_list
		return ast

	def visit_Function(self, ast, curScopeDict):
		# Uniquify the function's name first, because this is actually in the outerscope.
		ast.name = self.renameToUnique(curScopeDict, ast.name)
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		new_stmt_list = []
		for node in ast.code.nodes:
			new_stmt_list += [self.visit(node, copy.deepcopy(curScopeDict))]
		ast.code.nodes = new_stmt_list
		# Can't write directly to argname (don't know why) so make a new
		# argname_list and assign to ast.argnames
		argname_list = []
		for argname in ast.argnames:
			argname_list  += [self.renameToUnique(curScopeDict, argname)]
		ast.argnames = argname_list
		return ast

	def visit_Module(self, ast, curScopeDict={}):
		localVars = self._getLocals(ast)
		self.uniquifyLocalNames(localVars, curScopeDict)
		new_stmt_list = []
		for node in ast.node.nodes:
			new_stmt_list += [self.visit(node, copy.deepcopy(curScopeDict))]
		ast.node.nodes = new_stmt_list
		return ast

	def visit_Name(self, ast, curScopeDict):
		if not (ast.name == 'True' or ast.name == 'False'):
			ast.name = self.renameToUnique(curScopeDict, ast.name)
		return ast
	
	def visit_AssName(self, ast, curScopeDict):
		ast.name = self.renameToUnique(curScopeDict, ast.name)
		return ast

	# Trivial visitor methods below:	
	def visit_Const(self, ast, curScopeDict):
		return ast

	def visit_Return(self, ast, curScopeDict):
		ast.value = self.visit(ast.value, curScopeDict)
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
			elif isinstance(node, Lambda):
				print '\t' * tabcount + 'Lambda (' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]), tabcount+1)
				print '\t' * tabcount + 'EndLambda'
			elif isinstance(node, Function):
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
	P2Uniquify().print_ast(ast.node, 0)
