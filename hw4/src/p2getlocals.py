
from compiler import *
from compiler.ast import *

class P2GetLocals(object):

# Desc: This returns a list of local variables in a given scope and it's subscopes.
# 			Scopes in Python begin at function definitions, so the input is a Function
#			or Lambda or Module node (the 'main' function, so to speak).
# Args:	A Function, Lambda, or Module node.
# Ret:	A list of strings, where the string are the names of variables local to the
#			given scope.

	def getLocals(self, node):
		return self._getLocals(node, True)

	def getLocalsInCurrentScope(self, node):
		return self._getLocals(node, False)

	def _getLocals(self, node, doSubScopes, recurDepth=0):
		local_vars = []
		# Base case. If a variable is assigned to, it's local.
		if isinstance(node, Assign):
			if isinstance(node.nodes[0], AssName):
				local_vars += [node.nodes[0].name]
			elif isinstance(node.nodes[0], Name):
				local_vars += [node.nodes[0].name]
			elif isinstance(node.nodes[0], Subscript):
				local_vars += self._getLocals(node.expr, recurDepth + 1)
				local_vars += self._getLocals(node.nodes[0].expr, recurDepth + 1)
				local_vars += self._getLocals(node.nodes[0].subs, recurDepth + 1)
			return local_vars
		elif isinstance(node, Function):
			# Careful! A function's name is local to the scope *above* it.
			# We must account for this in the visitor functions below.
			local_vars += [node.name]
			local_vars += node.argnames
			for stmt in node.code.nodes:
				local_vars += self._getLocals(stmt, recurDepth + 1)
			return local_vars
		elif isinstance(node, Lambda):
			# Don't recurse into nested scopes if doSubScopes is False
			if doSubScopes == False and doSubScopes > 0:
				return []
			# Iterate through statements if there's a statement node below.
			if isinstance(node.code, Stmt):
				for stmt in node.code.nodes:
					local_vars += self._getLocals(stmt, recurDepth + 1)
			else:
				local_vars += self._getLocals(node.code, recurDepth + 1)
			local_vars += node.argnames
			return local_vars
		elif isinstance(node, Module):
			for stmt in node.node.nodes:
				local_vars += self._getLocals(stmt, recurDepth + 1)
			return local_vars
		elif isinstance(node, If) or isinstance(node, IfExp):
			# I don't think there can be an assign inside IfExpr, but just in case...
			local_vars += self._getLocals(node.tests[0][0], recurDepth + 1)
			local_vars += self._getLocals(node.tests[0][1], recurDepth + 1)
			local_vars += self._getLocals(node.else_, recurDepth + 1)
			return local_vars
		return []
