from astvisitor import *
from prjast import *

## Dictionary notation
#   Global-level dictionary -> { 'varName' ->
#								 	{ 'assign' -> [AssignNode1, AssignNode2, ...]
#								 	  'isReturned' -> False
#									  'containsReturn' -> True/False/Maybe
#									}
#							   }

class TailCallAnalysis(ASTVisitor):
	contRetFlag = { 'True' => True,
					'False' => False,
					'Sometimes' => "Sometimes" } 
	def _iterateAndVisit(self, astList, globalDict):
		for element in astList:
			self.visit(element, globalDict)
	def visit_Function(self, ast, globalDict):
		self.visit(ast.code, globalDict)
	def visit_Stmt(self, ast, globalDict):
		self._iterateAndVisit(ast.nodes, globalDict)

	def visit_Assign(self, ast, globalDict):			
		if isinstance(ast.expr, CallFunc) or isinstance(ast.expr, CallUserDef):
			#Look up in dictionary.
			if globalDict.has_key(ast.nodes[0].name):
				varDict = globalDict[ast.nodes[0].name]
				varDict['assign'].append(ast)
				if varDict['containsReturn'] == False:
					varDict['containsReturn'] = contRetFlat['Sometimes'] 
			else:
				varDict = { 'assign' => set([ast]),
							'isReturned' => False,
							'containsReturn' => True }
				globalDict[ast.nodes[0].name] = varDict
			#If, not in dictionary:
			#	Add to dict (Add assign, isReturned->False, containsReturn->True)
			#else
			#	Add current assign node to 'assign'
			#	containsReturn: If 'false' change to 'maybe'

		elif isinstance(ast.expr, Name):
			if globalDict.has_key(ast.expr.name):
				if globalDict.has_key(ast.nodes[0].name):
					for element in globalDict[ast.expr.name]['assign']:
						globalDict[ast.nodes[0].name]['assign'].append(element)
				else:
					varDict = { 'assign' => set([ast])
								'isReturned' => False
								'containsReturn' => True
									}
					for element in globalDict[ast.expr.name]['assign']:
						varDict['assign'].append(element)
					globalDict[ast.nodes[0].name] = varDict
	def visit_Return(self, ast, globalDict):
		if isinstance(ast.value, Name) and globalDict.has_key(ast.value.name):
			globalDict[ast.value.name]['isReturned'] = True

	def default(self, node, *extra):
		pass

	# Other statements that need recursion

	def visit_Module(self, ast, globalDict):
		self.visit(ast.node, globalDict)
	def visit_Printnl(self, ast, globalDict):
		self.visit(ast.nodes[0], globalDict))
	def visit_Discard(self, ast, globalDict):
		self.visit(ast.expr, globalDict)
	def visit_If(self, ast, globalDict):
		self.visit(ast.tests[0][0], globalDict)
		self.visit(ast.tests[0][1], globalDict)
		self.visit(ast.else_, globalDict)
	def visit_While(self, ast, globalDict):
		self.visit(ast.test, globalDict)
		self.visit(ast.body, globalDict)
