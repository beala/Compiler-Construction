from astvisitor import *
from prjast import *
from compiler.ast import *

## Dictionary notation
#	Flow Sensitive Global Dictionary
#		{'node' ->
#			{'before' -> [varDict, varDict, varDict],
#			 'after' -> [varDict, varDict, varDict]
#			}
#		}
#
#	varDict
#		{varName -> name		#The name of the var, as a string	
#	 	 assNode -> AssNode } 	#The original assignment node where the CallFunc happens

class TailCallAnalysis(ASTVisitor):
	
	_nodesToOptimize = set()
	def getNodesToOptimize(self): return self._nodesToOptimize

	# Private Methods: #########################################################################################
	def _makeNodeDict(self):
		nodeDict = {}
		nodeDict['before'] = []
		nodeDict['after'] = []
		return nodeDict

	def _searchListForVarDict(self, name, list_):
		for element in list_:
			#if element['varName'] == name:
			if element[0] == name:
				return element
		return False

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
		if isinstance(ast.expr, Name) and (self._searchListForVarDict(ast.expr.name, rBefore)):
			copiedFrom = self._searchListForVarDict(ast.expr.name, rBefore)
			varName = ast.nodes[0].name
			assNode = copiedFrom[1]
			varTup = (varName, assNode)
			rAfter.append(varTup)
			#copiedFrom = self._searchListForVarDict(ast.expr.name, rBefore)
			#newVarDict = {} # New varDict for the variable in the RHS of the assignment
			#newVarDict['varName'] = ast.nodes[0].name
			#newVarDict['assNode'] = copiedFrom['assNode']
			#rAfter.append(newVarDict)
			#import pdb; pdb.set_trace()
		# Elif the assign is from a CallUserDef
		elif isinstance(ast.expr, CallFunc) or isinstance(ast.expr, CallUserDef):
			varName = ast.nodes[0].name
			assNode = ast
			varTup = (varName, assNode)
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
		if isinstance(ast.value, Name) and self._searchListForVarDict(ast.value.name, rBefore):
			varReturned = self._searchListForVarDict(ast.value.name, rBefore)
			self._nodesToOptimize.add(varReturned[1]) # Add to the set of nodes to be optimized.
		
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
		rAfter = set(ifAfter) | set(elseAfter)
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
