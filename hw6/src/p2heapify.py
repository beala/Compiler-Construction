from compiler.ast import *
from astvisitor import *
from p3getfreevars import *
from p2getlocals import *
from p2ast import *
from p1ast import *
import copy
_debug = False

class P2Heapify(ASTVisitor):
	# Private Attributes: ##########################################################################################################	
	_argRenameCounter = 0
	_toHeapify = set() 

	# Private Methods: #############################################################################################################
	def _renameArg(self, nameStr):
		self._argRenameCounter += 1
		return str(nameStr) + "heap_" + str(self._argRenameCounter)	
	
	def _makeAssign(self, lhs, rhs):
		return Assign([AssName(lhs, 'OP_ASSIGN')], rhs)

	
	def _makeSubAssign(self, lhs, element, rhs):
		return Assign([Subscript(Name(lhs), 'OP_ASSIGN', [InjectFrom(Const(0), Const(element))])], rhs)

	# Generic function to iterate over a list and visit each item.
	def _iterate_over_and_visit(self, toIterate):
		bodyList = []
		freeBelowList = []
		for item in toIterate:
			(freeBelow, body) = self.visit(item)
			freeBelowList += freeBelow
			bodyList.append(body)
		return (freeBelowList, bodyList)

	# Turn a set into a list
	def _setToList(self, set_):
		return [item for item in set_]
	# Assign a one element list to lhs.
	def _assignInitList(self, lhs):
		return self._makeAssign(lhs, InjectFrom(Const(3), List([InjectFrom(Const(0), Const(0))])))

	# Visitor Methods: #############################################################################################################
	# Notes: Return a tuple of the values that are free in the current scope and below, along with the AST modified in the necessary
	# 	ways. Only nodes that are the beginning of a new scope should add names to the first element of the tuple (other nodes
	#	should just return whatever they've recieved from their children. The list of freeVars is a list of *strings* not Name() nodes.
	
	def visit_Module(self, ast):
		freeVarObj = P3GetFreeVars()
		freeVarObj.visit(ast)
		self._toHeapify |= set(freeVarObj.getVarsToHeapify())
		if _debug == True:
			print self._toHeapify
		(freeBelow, body) = self.visit(ast.node)
		localInits = []
		for var in set(freeBelow):
			localInits.append(self._assignInitList(var))
			#localInits.append(self._makeAssign(var, List([Const(0)])))
		return Module(None, Stmt(localInits + body.nodes))

	def visit_Lambda(self, ast):
		# Get the varaibles that are free IN THE CURRENT SCOPE. These need to be heapified.
			# Get everything free BELOW AND IN THE CURRENT SCOPE
			# Subtract out everything LOCAL IN THE CURRENT SCOPE
		freeVars = P3GetFreeVars().visit(ast)
		localHere = P2GetLocals().getLocalsInCurrentScope(ast)
		freeHere = set(freeVars) - set(localHere)
		self._toHeapify |= freeVars
		# Get the parameters that need to be heapified: P_h
		argsToHeapify = set(ast.argnames) & self._toHeapify #freeHere
		# Make a new argnames with the heapified parameters renamed: P'
		paramNameMap = {}
		renamedArgNames = copy.copy(ast.argnames)
		for arg in set(argsToHeapify):
			# Find index of arg to be renamed
			argToRename = renamedArgNames.index(arg)
			# Get a new name
			newName = self._renameArg(renamedArgNames[argToRename])
			# Associate it to the old name
			paramNameMap[arg] = newName
			# Set the argslist to the new name
			renamedArgNames[argToRename] = newName
		# Assign a one element list to each element in P_h: paramAllocs
		paramAllocs = []
		for arg in set(argsToHeapify):
			paramAllocs.append(self._assignInitList(arg))
		# Set the variables in P_h (argsToHeapify) to the cooresponding parameters in P' (new argnames) (assign to the first element in each P_h element)
		paramInits = []
		for arg in set(argsToHeapify):
			paramInits.append(self._makeSubAssign(arg, 0, Name(paramNameMap[arg])))
		# Get the local variables that need to be heapified: L_h. These are variables that are local here, but free below.
			# Get variables local to JUST THIS subscope.
			# Get variables free in JUST THE SUBSCOPES BELOW TODO: modify freevars function to do this
		# Assign a 1 element list to each element in L_h
		(freeBelow, body) = self.visit(ast.code)
		heapifyHere = (self._toHeapify & set(localHere)) - set(ast.argnames)
		localInits = []
		for var in set(heapifyHere):
			localInits.append(self._assignInitList(var))
		newLambda = Lambda(renamedArgNames, ast.defaults, ast.flags, Stmt( paramAllocs + localInits + paramInits + body.nodes ))
		return (self._setToList(freeHere), newLambda)

	def visit_Stmt(self, ast):
		(freeBelow, bodies) = self._iterate_over_and_visit(ast.nodes)
		return (freeBelow, Stmt(bodies))
			
	def visit_Name(self, ast):
		if ast.name in self._toHeapify:
			return ([], Subscript(Name(ast.name), 'OP_APPLY', [InjectFrom(Const(0), Const(0))]))
		return ([], ast)

	def visit_Assign(self, ast):
		# TODO: Are we dealing with too many cases here? Maybe we should iterate down into
		#	AssName (and whatever else is in ast.nodes) instead of having all these sepcial
		#	cases.
		(exprFreeBelow, exprBody) = self.visit(ast.expr)
		if isinstance(ast.nodes[0], AssName): 
			if ast.nodes[0].name in self._toHeapify:
				return (exprFreeBelow, self._makeSubAssign(ast.nodes[0].name, 0, exprBody))
			else:
				return (exprFreeBelow, self._makeAssign(ast.nodes[0].name, exprBody))
		
		(nodesFreeBelow, nodesBody) = self._iterate_over_and_visit(ast.nodes)
		return (exprFreeBelow + nodesFreeBelow, Assign(nodesBody, exprBody))
		#return (freeBelow, self._makeAssign(ast.nodes[0].name, body))
			
	# Handled by visit_Assign
	def visit_AssName(self, ast):
		pass		

	#uninteresting -- recurse
	def visit_Printnl(self, ast):
		(freeBelow, body) = self.visit(ast.nodes[0])
		return (freeBelow, Printnl([body], ast.dest))

	def visit_Const(self,ast):
		return ([], ast)

	# Generic function for visiting IntegerAdd, BigAdd, etc.
	# makeNodeFunc is a function that returns the correct type of node (IntegerAdd(), BigAdd(), etc)
	def _visit_Adds(self, ast, makeNodeFunc):
		(leftFreeBelow, leftBody) = self.visit(ast.left)
		(rightFreeBelow, rightBody) = self.visit(ast.right)
		return(leftFreeBelow + rightFreeBelow, makeNodeFunc(leftBody, rightBody))
		
	def visit_Add(self, ast):
		return self._visit_Adds(ast, lambda l, r: Add((l, r)))

	def visit_IntegerAdd(self,ast):
		 return self._visit_Adds(ast, lambda l,r: IntegerAdd((l,r,)))

	def visit_BigAdd(self, ast):
		return self._visit_Adds(ast, lambda l,r: BigAdd((l, r)))

	def _visit_Nodes(self, ast, makeNodeFunc):
		(nodesFreeBelow, nodesBody) = self._iterate_over_and_visit(ast.nodes)
		return (nodesFreeBelow, makeNodeFunc(nodesBody))

	def visit_Or(self, ast):
		return self._visit_Nodes(ast, lambda nodes: Or(nodes))

	def visit_And(self, ast):
		return self._visit_Nodes(ast, lambda nodes: And(nodes))

	def visit_List(self, ast):
		return self._visit_Nodes(ast, lambda nodes: List(nodes))

	def _visit_single(self, single, makeNodeFunc):
		(freeBelow, body) = self.visit(single)
		return (freeBelow, makeNodeFunc(body))
	
	def _visit_expr(self, ast, makeNodeFunc):
		return self._visit_single(ast.expr, makeNodeFunc)
	
	def visit_UnarySub(self, ast):
		return self._visit_expr(ast, lambda expr: UnarySub(expr))

	def visit_Not(self, ast):
		return self._visit_expr(ast, lambda expr: Not(expr))

	def visit_Discard(self, ast):
		return self._visit_expr(ast, lambda expr: Discard(expr))

	def _visit_Compares(self, ast, makeNodeFunc):
		(exprFreeBelow, exprBody) = self.visit(ast.expr)
		return (exprFreeBelow, makeNodeFunc(exprBody, ast.ops))

	def visit_Compare(self, ast):
		return self._visit_Compares(ast, lambda expr, ops: Compare(expr, ops))

	def visit_IntegerCompare(self, ast):
		return self._visit_Compares(ast, lambda expr, ops: IntegerCompare(expr, ops))

	def visit_BigCompare(self, ast):
		return self._visit_Compares(ast, lambda expr, ops: BigCompare(expr, ops))

	def visit_IsCompare(self, ast):
		return self._visit_Compares(ast, lambda expr, ops: IsCompare(expr, ops))	

	def visit_Dict(self, ast):
		itemsBody = []
		itemsFreeBelow = []
		for item in ast.items:
			(vFreeBelow, vBody) = self.visit(item[0])
			(kFreeBelow, kBody) = self.visit(item[1])
			itemsBody.append((vBody, kBody))
			itemsFreeBelow += vFreeBelow + kFreeBelow	
		return (itemsFreeBelow, Dict(itemsBody))

	def visit_Subscript(self, ast):
		(exprFreeBelow, exprBody) = self.visit(ast.expr)
		(subsFreeBelow, subsBody) = self._iterate_over_and_visit(ast.subs)
		return (exprFreeBelow + subsFreeBelow, Subscript(exprBody, ast.flags, subsBody))

	def visit_Return(self, ast):
		return self._visit_single(ast.value, lambda value: Return(value))

	def visit_IfExp(self, ast):
		(testFreeBelow, testBody) = self.visit(ast.test)
		(thenFreeBelow, thenBody) = self.visit(ast.then)
		(else_FreeBelow, else_Body) = self.visit(ast.else_)
		return (testFreeBelow + thenFreeBelow + else_FreeBelow, IfExp(testBody, thenBody, else_Body))

	def visit_Let(self, ast):
		(varFreeBelow, varBody) = self.visit(ast.var)
		(rhsFreeBelow, rhsBody) = self.visit(ast.rhs)
		(bodyFreeBelow, bodyBody) = self.visit(ast.body)
		return (varFreeBelow + rhsFreeBelow + bodyFreeBelow, Let(varBody, rhsBody, bodyBody))

	def _visit_jects(self, ast, makeNodeFunc):
		(typFreeBelow, typBody) = self.visit(ast.typ)
		(argFreeBelow, argBody) = self.visit(ast.arg)
		return (typFreeBelow + argFreeBelow, makeNodeFunc(typBody, argBody))
	
	def visit_InjectFrom(self, ast):
		return self._visit_jects(ast, lambda typ, arg: InjectFrom(typ, arg))

	def visit_ProjectTo(self, ast):
		return self._visit_jects(ast, lambda typ, arg: ProjectTo(typ, arg))

	def	visit_GetTag(self, ast):
		return self._visit_single(ast.arg, lambda arg: GetTag(arg))

	def _visit_Calls(self, ast, makeNodeFunc):
		(nodeFreeBelow, nodeBody) = self.visit(ast.node)
		(argsFreeBelow, argsBody) = self._iterate_over_and_visit(ast.args)
		return (argsFreeBelow + nodeFreeBelow, makeNodeFunc(nodeBody, argsBody))
		
	def visit_CallFunc(self, ast):
		return self._visit_Calls(ast, lambda node, args: CallFunc(node, args))

	def visit_CallUserDef(self, ast):
		return self._visit_Calls(ast, lambda node, args: CallUserDef(node, args))

	# Debugging methods: #############################################################################
	def print_ast(self, stmt_ast, tabcount=0):
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
				self.print_ast(node.code, tabcount+1)
				print '\t' * tabcount + 'EndFunc'
			elif isinstance(node, Assign):
				self.indent(tabcount, str(node.nodes) + " =")
				self.print_ast(Stmt([node.expr]), tabcount + 1)
				self.indent(tabcount, "EndAssign")
			else:
				print '\t' * (tabcount) + str(node)

	def indent(self, tabcount, text):
		print ('\t' * tabcount) + str(text)

if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	_debug = True
	print "-"*20 + "Parsed AST" + "-"*20 
	if os.path.isfile(sys.argv[1]):
		print compiler.parseFile(sys.argv[1])
		to_explicate = compiler.parseFile(sys.argv[1])
	else:
		print compiler.parse(sys.argv[1])
		to_explicate = compiler.parse(sys.argv[1])
	print "-"*20 + "Uniquified AST" + "-"*20
	to_explicate = P2Uniquify().visit(to_explicate)
	P2Uniquify().print_ast(to_explicate.node)
	print "-"*20 + "Explicated AST" + "-"*20
	explicated = P2Explicate().visit(to_explicate)
	P2Uniquify().print_ast(explicated.node)
	print "-"*20 + "Heapified AST" + "-"*20
	heapified = P2Heapify().visit(explicated)
	#print heapified	
	P2Heapify().print_ast(heapified.node)
