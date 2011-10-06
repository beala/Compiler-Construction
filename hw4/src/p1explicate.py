#!/usr/bin/python

from MyFlattener import *
from compiler import *
from p1ast import *
class P1Explicate(ASTVisitor):
	# Private Variables: #########################################################################
	_currentTmpVar = 0
	_typeMap = {'int': 0,
				'bool': 1,
				'big' : 3 }
	
	# Private Methods: ###########################################################################
	def _makeTmpVar(self):
		self._currentTmpVar += 1
		return "exp_tmp" + str(self._currentTmpVar)

	def _getCurrentTmpVar(self):
		return "exp_tmp" + str(self._currentTmpVar)

	def _renameVar(self, var_name):
		return "_" + var_name

	def _compareEqType(self, lhs, rhs):
		return Compare(GetTag(lhs), [('==', rhs)])

	def _makeBigAssIf(self, varToTest, intFunc, boolFunc, bigFunc):
		errFunc='type_error'
		return IfExp( self._compareEqType(varToTest, self._typeMap['int']), 						\
									CallFunc(Name(intFunc), []), 									\
									IfExp( self._compareEqType(varToTest, self._typeMap['bool']),	\
										CallFunc(Name(boolFunc), []),								\
										IfExp( self._compareEqType(varToTest, self._typeMap['big']),\
											CallFunc(Name(bigFunc), []),							\
											CallFunc(Name(errFunc), []) )))
	
	# Visitor Methods: ###########################################################################
	def visit_Module(self, node):
		return Module(None, self.visit(node.node))

	def visit_Stmt(self, node):
		list_statements = []
		for child in node.nodes:
			list_statements += self.visit(child)
		return Stmt(list_statements)
	
	def visit_Discard(self, node):
		return self.visit(node.expr)[1]

	def visit_Printnl(self, node):
		(expr, s_list) = self.visit(node.nodes[0])
		tmpVar = Name(self._makeTmpVar())
		letStmt = Let(tmpVar, expr, self._makeBigAssIf(tmpVar, 'print_int', 'print_bool', 'print_big'))
		return (tmpVar, [letStmt] + s_list)

	def visit_Name(self, node):
		return (node, [])

	def visit_Add(self, node):
		(lExpr, lstatement_list) = self.visit(node.left)
		(rExpr, rstatement_list) = self.visit(node.right)
		sumTmpVar = self._makeTmpVar()
		addNode = Add(( lExpr, rExpr ))
		return (Name(sumTmpVar), lstatement_list + rstatement_list + [Assign( [AssName(sumTmpVar, 'OP_ASSIGN')], addNode)])

if __name__ == '__main__':
	import sys
	import compiler
	print P1Explicate().visit(compiler.parse(sys.argv[1]))
