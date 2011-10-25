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

	# Visitor Methods: #############################################################################################################
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
		freeBelow = []
		bodies = []
		for stmt in ast.nodes:
			(free, body) = self.visit(stmt)
			freeBelow += free
			bodies += body
		return (freeBelow, Stmt(bodies))
			
	def visit_Name(self, ast):
		if ast.name in self._toHeapify
			return ([], Subscript(Name(ast.name), 'OP_APPLY', [Const(0)]))
		return ([], ast)

	def visit_Assign(self, ast):
		(freeBelow, body) = self.visit(ast.expt)
		if isinstance(ast.nodes[0], AssName) and ast.nodes[0].name in self._toHeapify:
			return ([], self._makeSubAssign(ast.nodes[0].name, 0, body))
			
		return ([], Assign(ast.nodes, body))

	# Handled by visit_Assign
	def visit_AssName(self, ast):
		pass		

	#uninteresting -- recurse
