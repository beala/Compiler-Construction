from astvisitor import *
from prjast import *
from compiler.ast import *

## Dictionary notation
#	Flow Sensitive Global Dictionary
#		{'node' ->
#			{'before' -> [varTup, varTup, ...],
#			 'after' -> [varTup, varTup, ...]
#			}
#		}
#
#	varTup
#		(varName, [assNode, assNode,...])

class TailCallAnalysis(ASTVisitor):
	
	_nodesToOptimize = []
	def getNodesToOptimize(self): return self._nodesToOptimize

	# Private Methods: #########################################################################################
	def _makeNodeDict(self):
		nodeDict = {}
		nodeDict['before'] = []
		nodeDict['after'] = []
		return nodeDict

	def _searchListForVarTup(self, name, list_):
		varsFound = []
		for element in list_:
			if element[0] == name:
				varsFound.append(element)
		return varsFound

	def _iterateAndVisit(self, astList, rBefore, globalDict):
		for element in astList:
			rAfter = self.visit(element, rBefore, globalDict)
			rBefore = rAfter
		return rAfter

	# Visitor Methods: #########################################################################################
	def visit_Function(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		self.visit(ast.code, {}, globalDict)	# Kill everything at the beginning of a function.
		nodeDict['after'] = []	# Kill everything at the end of a function
		globalDict[ast] = nodeDict
		return []

	def visit_Stmt(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		rAfter = self._iterateAndVisit(ast.nodes, rBefore, globalDict) 
		nodeDict['after'] = rAfter
		#globalDict[ast] = nodeDict
		return rAfter

	def visit_Assign(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		rAfter = []
		# If the assign is a copy from a var in rBefore
		if isinstance(ast.expr, Name) and (self._searchListForVarTup(ast.expr.name, rBefore)):
			copiedFrom = self._searchListForVarTup(ast.expr.name, rBefore)
			varName = ast.nodes[0].name
			assNodes = [] 
			for assNode in copiedFrom:
				assNodes += assNode[1]
			varTup = (varName, assNodes)
			rAfter.append(varTup)
			#copiedFrom = self._searchListForVarTup(ast.expr.name, rBefore)
			#newVarDict = {} # New varDict for the variable in the RHS of the assignment
			#newVarDict['varName'] = ast.nodes[0].name
			#newVarDict['assNode'] = copiedFrom['assNode']
			#rAfter.append(newVarDict)
			#import pdb; pdb.set_trace()
		# Elif the assign is from a CallUserDef
		elif isinstance(ast.expr, CallFunc) or isinstance(ast.expr, CallUserDef):
			varName = ast.nodes[0].name
			assNodes = [ast]
			varTup = (varName, assNodes)
			rAfter.append(varTup)
			#varDict = {}
			#varDict['varName'] = ast.nodes[0].name
			#varDict['assNode'] = ast
			#rAfter.append(varDict)
		# Else kill everthing in R_after
		else:
			pass # rAfter already empty

		nodeDict['after'] = rAfter
		globalDict[ast] = nodeDict
		return rAfter

	def visit_Return(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		# If a variable holding a return value is returned
		if isinstance(ast.value, Name) and self._searchListForVarTup(ast.value.name, rBefore):
			varsReturned = self._searchListForVarTup(ast.value.name, rBefore)
			for varTup in varsReturned:
				self._nodesToOptimize += varTup[1] # Add to the set of nodes to be optimized.
				for node in varTup[1]:
					node.tailCall = True # Mark the node as being a tail call
		
		# rAfter is always empty after return
		rAfter = []
		nodeDict['after'] = rAfter
		globalDict[ast] = nodeDict
		return rAfter

	def visit_If(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		ifAfter = self.visit(ast.tests[0][1], rBefore, globalDict)
		elseAfter = self.visit(ast.else_, rBefore, globalDict)
		#import pdb; pdb.set_trace()
		rAfter = ifAfter + elseAfter
		nodeDict['after'] = rAfter

		globalDict[ast] = nodeDict
		return rAfter

	# This is not functioning. Just getting the skeleton here for consistency.
	def visit_While(self, ast, rBefore, globalDict):
		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		rAfter = self.visit(ast.body, rBefore, globalDict)
		nodeDict['after'] = rAfter

		globalDict[ast] = nodeDict
		return rAfter

	# For all other nodes, set rAfter to empty.
	def default(self, node, *extra):
		rBefore = extra[0]
		globalDict = extra[1]

		nodeDict = self._makeNodeDict()
		nodeDict['before'] = rBefore
		nodeDict['after'] = []
		globalDict[node] = nodeDict
		return []

	# Other statements that need recursion
	def visit_Module(self, ast, globalDict):
		self.visit(ast.node, globalDict)
