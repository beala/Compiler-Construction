#!/usr/bin/python

from MyFlattener import *
from compiler import *
from p1ast import *
class P1Explicate(ASTVisitor):
	# Private Variables: #########################################################################
	_currentTmpVar = 0
	_typeMap = {'int': Const(0),
				'bool': Const(1),
				'big' : Const(3) }
	
	# Private Methods: ###########################################################################
	def _makeTmpVar(self):
		self._currentTmpVar += 1
		return "exp_tmp" + str(self._currentTmpVar)

	def _getCurrentTmpVar(self):
		return "exp_tmp" + str(self._currentTmpVar)

	def _renameVar(self, var_name):
		return "_" + var_name

	def _compareEqType(self, lhs, rhs):
		return InjectFrom(self._typeMap['bool'], IntegerCompare(InjectFrom(self._typeMap['int'], GetTag(lhs)), [('==', InjectFrom(self._typeMap['int'],rhs))]))

	# Visitor Methods: ###########################################################################
	def visit_Module(self, node):
		newModule = Module(None, self.visit(node.node))
		return newModule

	def visit_Stmt(self, node):
		list_statements = []
		for child in node.nodes:
			list_statements += [self.visit(child)]
		return Stmt(list_statements)
	
	def visit_Discard(self, node):
		return Discard(self.visit(node.expr))

	def visit_Printnl(self, node):
		expr = self.visit(node.nodes[0])
		return  Printnl([expr], None) 

	def visit_Name(self, node):
		# If name is on the LHS of an expr, the thing on the RHS should alreay have been
		# injected.
		# If name is on the RHS, then earlier in the program, it should have had an already 
		# injected thing assigned to it (by step 1)
		# Therefore, it's already been injected and doesn't need to be again.
		if (node.name=='True' or node.name=='False'):
			return InjectFrom(self._typeMap['bool'], node)
		else:
			return node
	
	def visit_Const(self, node):
		return InjectFrom(self._typeMap['int'], node) # Inject const because it is always a leave node. It can't already have been injected.

	def visit_Assign(self, node):
		lExpr = self.visit(node.nodes[0])
		rExpr = self.visit(node.expr)
		return Assign([lExpr],  rExpr)

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
		rExpr = self.visit(node.ops[0][1])
		tmpVarLeft = Name(self._makeTmpVar())
		tmpVarRight = Name(self._makeTmpVar())
		if node.ops[0][0] == 'is':
			return Let(tmpVarLeft, lExpr, Let(tmpVarRight, rExpr, InjectFrom(self._typeMap['bool'], IsCompare(tmpVarLeft, [(node.ops[0][0], tmpVarRight)]))))
		# If we're testing equality, return False if the two operands are of a different type.
		# If we're testing non-equality, return True
		if node.ops[0][0] == '==':
			lastElse = Const(0)
		elif node.ops[0][0] == '!=':
			lastElse = Const(1)
		return Let(tmpVarLeft, lExpr, Let(tmpVarRight, rExpr, InjectFrom(self._typeMap['bool'],  
				IfExp( And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['int'] )]),IntegerCompare(ProjectTo(self._typeMap['int'],tmpVarLeft), [(node.ops[0][0], ProjectTo(self._typeMap['int'],tmpVarRight))]), \
				IfExp (And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']), self._compareEqType(tmpVarRight, self._typeMap['bool'] )]),IntegerCompare(ProjectTo(self._typeMap['bool'],tmpVarLeft),[(node.ops[0][0], ProjectTo(self._typeMap['bool'],tmpVarRight))]), \
				IfExp (And( [self._compareEqType(tmpVarLeft, self._typeMap['bool']), self._compareEqType(tmpVarRight, self._typeMap['int'] )]),IntegerCompare(ProjectTo(self._typeMap['bool'],tmpVarLeft), [(node.ops[0][0], ProjectTo(self._typeMap['int'],tmpVarRight))]), \
				IfExp (And( [self._compareEqType(tmpVarLeft, self._typeMap['int']), self._compareEqType(tmpVarRight, self._typeMap['bool'] )]),IntegerCompare(ProjectTo(self._typeMap['int'],tmpVarLeft),[(node.ops[0][0], ProjectTo(self._typeMap['bool'],tmpVarRight))]), \
				IfExp (And( [self._compareEqType(tmpVarLeft, self._typeMap['big']), self._compareEqType(tmpVarRight, self._typeMap['big'] )]), BigCompare(ProjectTo(self._typeMap['big'],tmpVarLeft), [(node.ops[0][0], ProjectTo(self._typeMap['big'],tmpVarRight))]), \
				lastElse ))))))))	

	def visit_Or(self, node):
		lExpr = self.visit(node.nodes[0])
		tmpVarLeft = Name(self._makeTmpVar())
		return Let(tmpVarLeft, lExpr, IfExp( tmpVarLeft, tmpVarLeft, self.visit(node.nodes[1])))
		
	def visit_And(self, node):
		lExpr = self.visit(node.nodes[0])
		tmpVarLeft = Name(self._makeTmpVar())
		return Let(tmpVarLeft, lExpr, IfExp( tmpVarLeft, self.visit(node.nodes[1]), tmpVarLeft))

	def visit_Not(self, node):
		expr = self.visit(node.expr)
		tmpVarLeft = Name(self._makeTmpVar())
		return Let(tmpVarLeft, expr, InjectFrom( self._typeMap['bool'], IfExp( tmpVarLeft, Const(0), Const(1))))

	def visit_List(self, node):
		newList = List([])
		for element in node.nodes:
			newList.nodes.append(self.visit(element))
		return InjectFrom(self._typeMap['big'],newList)

	def visit_Dict(self, node):
		newDict = Dict([])
		for element in node.items:
			newDict.items.append( (self.visit(element[0]), self.visit(element[1]) ) )
		return InjectFrom(self._typeMap['big'],newDict)

	def visit_Subscript(self, node):
		return Subscript( self.visit(node.expr), node.flags, [self.visit(i) for i in node.subs] )

	def visit_IfExp(self, node):
		myTest = self.visit(node.test)
		myThen = self.visit(node.then)
		myElse_ = self.visit(node.else_)
		tmpMyTest = Name(self._makeTmpVar())
		return Let( tmpMyTest, myTest, IfExp(tmpMyTest, myThen, myElse_))

	def visit_CallFunc(self, node):
		return InjectFrom(self._typeMap['int'], node)

if __name__ == '__main__':
	import sys
	import compiler
	print compiler.parse(sys.argv[1])
	print P1Explicate().visit(compiler.parse(sys.argv[1]))
