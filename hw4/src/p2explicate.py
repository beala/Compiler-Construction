from p1explicate import *
from compiler.ast import *
class P2Explicate(P1Explicate):

	# Private Variables: #######################################################################################
	_typeMap = {'int': Const(0),
				'bool': Const(1),
				'fun' : Const(2),
				'big' : Const(3) }

	# Visitor Methods: #########################################################################################
	def visit_Module(self, node):
		newModule = Module(None, self.visit(node.node))
		newModule.localVars = node.localVars
		return newModule
	def visit_Function(self, node):
		#create a super-lambda node here and visit children
		newAssign = AssName(node.name, 'OP_ASSIGN')
		newLambda = Lambda(node.argnames, node.defaults, node.flags, self.visit(node.code))
		newLambda.localVars = node.localVars
		return Assign([newAssign], InjectFrom(self._typeMap['fun'],newLambda))
	def visit_Lambda(self, node):
		#create a super-lambda here and visit children
		#remember, at this stage, arg names are simple strings
		myStmt = self.visit(Return(node.code)) #also wrap in a return statement
		newLambda = Lambda(node.argnames, node.defaults, node.flags, Stmt([myStmt]))
		newLambda.localVars = node.localVars
		return InjectFrom(self._typeMap['fun'], newLambda)
	def visit_Return(self, node):
		#pretty straight-forward, just explicate our children and return
		return Return(self.visit(node.value))
	def visit_CallFunc(self, node):
		newArgs = []
		newArgs = [self.visit(argument) for argument in node.args]
		node.args = newArgs
		myExpr = Name(self._makeTmpVar())
		return Let(myExpr, node, InjectFrom(GetTag(myExpr), myExpr))	

if __name__ == '__main__':
	import sys 
	import compiler
	import os
	from p2uniquify import *
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
	P2Uniquify().print_ast(P2Explicate().visit(to_explicate).node)
