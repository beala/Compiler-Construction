from compiler.ast import *
from astvisitor import *
from p2getfreevars import *
from p2getlocals import *

class P2Heapify(ASTVisitor):
	# Private Attributes: ##########################################################################################################	
	_argRenameCounter = 0
	_toHeapify = []

	# Private Methods: #############################################################################################################
	def _renameArg(self, nameStr):
		_argRenameCounter += 1
		return str(nameStr) + "heap_" + str(self._argRenameCounter)	
	
	def _makeAssign(self, lhs, rhs):
		return Assign([AssName(lhs, 'OP_ASSIGN')], rhs)

	def _makeSubAssign(self, lhs, element, rhs):
		return Assign([Subscript(Name(lhs), 'OP_ASSIGN', [Const(element)])], rhs)

	# Generic function to iterate over a list and visit each item.
	def _iterate_over_and_visit(self, toIterate):
		bodyList = []
		freeBelowList = []
		for item in toIterate:
			(freeBelow, body) = self.visit(item)
			freeBelow += freeBelowList
			bodyList.append(body)
		return (freeBelow, bodyList)

	# Visitor Methods: #############################################################################################################
	# Notes: Return a tuple of the values that are free in the current scope and below, along with the AST modified in the necessary
	# 	ways. Only nodes that are the beginning of a new scope should add names to the first element of the tuple (other nodes
	#	should just return whatever they've recieved from their children. The list of freeVars is a list of *strings* not Name() nodes.
	
	def visit_Module(self, ast):
		(freeBelow, body) = self.visit(ast.node)
		localInits = []
		for var in freeBelow:
			localInits += self._makeAssign(var, List([0]))
		return Module(None, Stmt(localInits + body))

	def visit_Lambda(self, ast):
		# Get the varaibles that are free IN THE CURRENT SCOPE. These need to be heapified.
			# Get everything free BELOW AND IN THE CURRENT SCOPE
			# Subtract out everything LOCAL IN THE CURRENT SCOPE
		freeVars = P2GetFreeVars().visit(node)
		localHere = P2GetLocals().getLocalsInCurrentScope(ast)
		freeHere = set(freeVars) - set(localHere)
		# Get the parameters that need to be heapified: P_h
		argsToHeapify = set(ast.argnames) & freeHere
		# Make a new argnames with the heapified parameters renamed: P'
		paramNameMap = {}
		for arg in argsToHeapify:
			# Find index of arg to be renamed
			argToRename = ast.argnames.index(arg)
			# Get a new name
			newName = self._renameArg(ast.argnames[argToRename])
			# Associate it to the old name
			paramNameMap[arg] = newName
			# Set the argslist to the new name
			ast.argnames[argToRename] = newName
		# Assign a one element list to each element in P_h: paramAllocs
		paramAllocs = []
		for arg in ast.argsToHeapify:
			paramAllocs.append(self._makeAssign(arg, List([0])))
		# Set the variables in P_h (argsToHeapify) to the cooresponding parameters in P' (new argnames) (assign to the first element in each P_h element)
		paramInits = []
		for arg in ast.argsToHeapify:
			paramInits.append(self._makeSubAssign(arg, 0, Name(paramNameMap[arg]))
		# Get the local variables that need to be heapified: L_h. These are variables that are local here, but free below.
			# Get variables local to JUST THIS subscope.
			# Get variables free in JUST THE SUBSCOPES BELOW TODO: modify freevars function to do this
		# Assign a 1 element list to each element in L_h
		(freeBelow, body) = self.visit(node.body)
		heapifyHere = freeBelow & localHere
		localInits = []
		for var in heapifyHere:
			localInits.append(self._makeAssign(var, List([0])))
		self._toHeapify += localInits
		newLambda = Lambda(ast.argnames, ast.defaults, ast.flags, Stmt( paraAllocs + paramInits + localInits + body ))
		return (freeHere, newLambda)

	def visit_Stmt(self, ast):
		(freeBelow, bodies) = self._iterate_over_and_visit(ast.nodes)
		return (freeBelow, Stmt(bodies))
			
	def visit_Name(self, ast):
		if ast.name in self._toHeapify
			return ([], Subscript(Name(ast.name), 'OP_APPLY', [Const(0)]))
		return ([], ast)

	def visit_Assign(self, ast):
		(freeBelow, body) = self.visit(ast.expt)
		if isinstance(ast.nodes[0], AssName) and ast.nodes[0].name in self._toHeapify:
			return ([], self._makeSubAssign(ast.nodes[0].name, 0, body))
			
	# Handled by visit_Assign
	def visit_AssName(self, ast):
		pass		

	#uninteresting -- recurse
	def visit_Printnl(self, ast):
		(freeBelow, body) = self.visit(ast.nodes[0])
		return (freeBelow, Printnl([body], ast.dest)

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
		return (freeBelow, makeNodeFunc(single))
	
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
		return self._visit_single(ast.values, lambda values: Return(value))

	def visit_IfExp(self, ast):
		(testFreeBelow, testBody) = self.visit(ast.test)
		(thenFreeBelow, thenBody) = self.visit(ast.then)
		(else_FreeBelow, else_Body) = self.visit(ast.else_)
		return (testFreeBelow + thenFreeBelow + else_freeBelow, IfExp(testBody, thenBody, else_Body)

	def visit_Let(self, ast):
		(varFreeBelow, varBody) = self.visit(ast.var)
		(rhsFreeBelow, rhsBody) = self.visit(ast.rhs)
		(bodyFreeBelow, bodyBody) = self.visit(ast.body)
		return (varFreeBelow + rhsFreeBelow + bodyFreeBelow, Let(varBody, rhsBody, bodyBody))

	def _visit_jects(self, ast, makeNodeFunc):
		(typFreeBelow, typBody) = self.visit(ast.typ)
		(argFreeBelow, argBody) = self.visit(ast.arg)
		return (typFreeBelow + argFreeBelow, makeNodFunc(typBody, argBody))
	
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
		return self._visit_Calls(self, ast, lambda node, args: CallFunc(node, args))

	def visit_CallUserDef(self, ast):
		return self._visit_Calls(self, ast, lambda node, args: CallUserDef(node, args))
