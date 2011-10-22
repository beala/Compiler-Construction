
from compiler import *
from compiler.ast import *

# Desc: This returns a list of local variables in a given scope and it's subscopes.
# 			Scopes in Python begin at function definitions, so the input is a Function
#			or Lambda or Module node (the 'main' function, so to speak).
# Args:	A Function, Lambda, or Module node.
# Ret:	A list of strings, where the string are the names of variables local to the
#			given scope.

def getLocals(node):
	local_vars = []
	# Base case. If a variable is assigned to, it's local.
	if isinstance(node, Assign):
		if isinstance(node.nodes[0], AssName):
			local_vars += [node.nodes[0].name]
		elif isinstance(node.nodes[0], Name):
			local_vars += [node.nodes[0].name]
		elif isinstance(node.nodes[0], Subscript):
			local_vars += getLocals(node.expr)
			local_vars += getLocals(node.nodes[0].expr)
			local_vars += getLocals(node.nodes[0].subs)
		return local_vars
	elif isinstance(node, Function):
		# Careful! A function's name is local to the scope *above* it.
		# We must account for this in the visitor functions below.
		local_vars += [node.name]
		local_vars += node.argnames
		for stmt in node.code.nodes:
			local_vars += getLocals(stmt)
		return local_vars
	elif isinstance(node, Lambda):
		local_vars += node.argnames
		local_vars += getLocals(node.code)
		return local_vars
	elif isinstance(node, Module):
		for stmt in node.node.nodes:
			local_vars += getLocals(stmt)
		return local_vars
	elif isinstance(node, If) or isinstance(node, IfExp):
		# I don't think there can be an assign inside IfExpr, but just in case...
		local_vars += getLocals(node.tests[0][0])
		local_vars += getLocals(node.tests[0][1])
		local_vars += getLocals(node.else_)
		return local_vars
	return []
