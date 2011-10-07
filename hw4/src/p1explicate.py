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
	def _makeBinaryIf(self, leftVar, rightVar, intOrBoolFunc, twoBigsFunc):
		return IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['int'])]), IntegerAdd((ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight))),	\
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), IntegerAdd((ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['int'])] ), IntegerAdd((ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), IntegerAdd((ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['big']),self._compareEqType(tmpVarRight,self._typeMap['big'])] ), BigAdd((ProjectTo(self._typeMap['big'],tmpVarLeft), ProjectTo(self._typeMap['big'],tmpVarRight))), \
					CallFunc(Name('type_error'), [])))))) 
	
	# Visitor Methods: ###########################################################################
	def visit_Module(self, node):
		return Module(None, self.visit(node.node))

	def visit_Stmt(self, node):
		list_statements = []
		for child in node.nodes:
			list_statements += [self.visit(child)]
		return Stmt(list_statements)
	
	def visit_Discard(self, node):
		return self.visit(node.expr)[1]

	def visit_Printnl(self, node):
		expr = self.visit(node.nodes[0])
		return  Printnl([expr], None) 

	def visit_Name(self, node):
		return node
	
	def visit_Const(self, node):
		return node

	def visit_Assign(self, node):
		lExpr = self.visit(node.nodes[0])
		rExpr = self.visit(node.expr)
		return Assign([lExpr],rExpr)

	def visit_UnarySub(self, node):
		expr = self.visit(node.expr)
		tmpVar = Name(self._makeTmpVar())
		return Let(tmpVar, expr, IfExp( self._compareEqType(tmpVar, self._typeMap['int']), InjectFrom(self._typeMap['int'], UnarySub( ProjectTo(self._typeMap['int'], tmpVar))), \
									IfExp( self._compareEqType(tmpVar, self._typeMap['bool']), InjectFrom(self._typeMap['int'], UnarySub( ProjectTo(self._typeMap['bool'], tmpVar))), \
									CallFunc(Name('type_error'),[]))))

	def visit_Add(self, node):
		lExpr = self.visit(node.left)
		rExpr = self.visit(node.right)
		tmpVarLeft = Name(self._makeTmpVar())
		tmpVarRight = Name(self._makeTmpVar())
		return Let(tmpVarLeft, lExpr, Let(tmpVarRight, rExpr, \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['int'])]), InjectFrom(self._typeMap['int'], IntegerAdd((ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight)))),	\
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), InjectFrom(self._typeMap['int'], IntegerAdd((ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight)))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['int'])] ), InjectFrom(self._typeMap['int'], IntegerAdd((ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight)))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), InjectFrom(self._typeMap['int'], IntegerAdd((ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight)))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['big']),self._compareEqType(tmpVarRight,self._typeMap['big'])] ), InjectFrom(self._typeMap['big'],BigAdd((ProjectTo(self._typeMap['big'],tmpVarLeft), ProjectTo(self._typeMap['big'],tmpVarRight)))), \
					CallFunc(Name('type_error'), []) ))))) ))
	
	def visit_AssName(self, node):
		return node

	def visit_Compare(self, node):
		lExpr = self.visit(node.expr)
		rExpr = self.visit(node.ops[1])
		tmpVarLeft = Name(self._makeTmpVar())
		tmpVarRight = Name(self._makeTmpVar())
		return Let(tmpVarLeft, lExpr, Let(tmpVarRight, rExpr, \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['int'])]), InjectFrom(self._typeMap['bool'], Compare(ProjectTo(self._typeMap['int'],tmpVarLeft),[node.ops[0], ProjectTo(self._typeMap['int'],tmpVarRight)])),	\
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), InjectFrom(self._typeMap['bool'], Compare(ProjectTo(self._typeMap['int'],tmpVarLeft), [node.ops[0],ProjectTo(self._typeMap['bool'],tmpVarRight)])), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['int'])] ), InjectFrom(self._typeMap['bool'], Compare(ProjectTo(self._typeMap['bool'],tmpVarLeft), [node.ops[0], ProjectTo(self._typeMap['int'],tmpVarRight)])), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), InjectFrom(self._typeMap['bool'], Compare(ProjectTo(self._typeMap['bool'],tmpVarLeft),[node.ops[0], ProjectTo(self._typeMap['bool'],tmpVarRight)])), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['big']),self._compareEqType(tmpVarRight,self._typeMap['big'])] ), InjectFrom(self._typeMap['bool'], Compare(ProjectTo(self._typeMap['big'],tmpVarLeft), [node.ops[0], ProjectTo(self._typeMap['big'],tmpVarRight)])), \
					InjectFrom(self._typeMap['bool'], Const(0)) ))))) ))
	
	def visit_Or(self, node):
		lExpr = self.visit(node.nodes[0])
		rExpr = self.visit(node.nodes[1])
		tmpVarLeft = Name(self._makeTmpVar())
		tmpVarRight = Name(self._makeTmpVar())
		return Let(tmpVarLeft, lExpr, Let(tmpVarRight, rExpr, \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['int'])]), InjectFrom(self._typeMap['int'], Or([ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight)])),	\
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), IfExp( Compare( Or([ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight)]), ['==', Const(0)] ), InjectFrom(self._typeMap['bool'], Const(0)), InjectFrom(self._typeMap['int'], Or([ProjectTo(self._typeMap['int'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight)]))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['int'])] ), IfExp( Compare( Or([ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight)]), ['==', Const(0)] ), InjectFrom(self._typeMap['bool'], Const(0)), InjectFrom(self._typeMap['int'], Or([ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['int'],tmpVarRight)]))), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']),self._compareEqType(tmpVarRight,self._typeMap['bool'])] ), InjectFrom(self._typeMap['bool'], Or([ProjectTo(self._typeMap['bool'],tmpVarLeft), ProjectTo(self._typeMap['bool'],tmpVarRight)])), \
					IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['big']),self._compareEqType(tmpVarRight,self._typeMap['big'])] ), InjectFrom(self._typeMap['bool'], Compare((ProjectTo(self._typeMap['big'],tmpVarLeft), [node.ops[0], ProjectTo(self._typeMap['big'],tmpVarRight)]))), \
					InjectFrom(self._typeMap['bool'], Const(0)) ))))) ))

if __name__ == '__main__':
	import sys
	import compiler
	print P1Explicate().visit(compiler.parse(sys.argv[1]))
