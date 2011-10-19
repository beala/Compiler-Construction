#!/usr/bin/python

#MyFlattener.py
from compiler.ast import *
from astvisitor import *

class P0ASTFlattener(ASTVisitor):
	# Private Variables: #########################################################################
	_currentTmpVar = 0
	
	# Private Methods: ###########################################################################
	def _makeTmpVar(self):
		self._currentTmpVar += 1
		return "tmp" + str(self._currentTmpVar)
	def _getCurrentTmpVar(self):
		return "tmp" + str(self._currentTmpVar)
	def _renameVar(self, var_name):
		return "_" + var_name

	# Visitor Methods: ###########################################################################
	def visit_Module(self, node):
		return Module(None,self.visit(node.node))
	
	def visit_Stmt(self, node):
		list_statements = []
		for child in node.nodes:
			list_statements += self.visit(child)
		return Stmt(list_statements)
	
	def visit_Discard(self, node):
		return self.visit(node.expr)[1]
	
	def visit_Const(self, node):
		tmpVar = self._makeTmpVar()
		return (node, [])
 	
	def visit_Name(self, node):
		newName = self._renameVar(node.name)
		return (Name(newName), [])

	def visit_Printnl(self, node):
		(expr, statement_list) = self.visit(node.nodes[0])
		return (statement_list + [Printnl([expr], None)])
	
	def visit_Assign(self,node):
		if isinstance(node.nodes[0], Subscript):
			(expr, statement_list) = self.visit(node.expr)
			(expr_nodes, statement_list_nodes) = self.visit(node.nodes[0])
			return (statement_list + statement_list_nodes + [Assign([AssName(expr_nodes.name,'OP_ASSIGN')], expr)])
		else:
			(expr, statement_list) = self.visit(node.expr)
			newName = self._renameVar(node.nodes[0].name)
			return (statement_list + [Assign([AssName(newName, 'OP_ASSIGN')], expr)])

		#newName = self._renameVar(node.nodes[0].name)
		#return (statement_list + [Assign([AssName(newName, 'OP_ASSIGN')], expr)])
	
	def visit_Add(self, node):
		(lExpr, lstatement_list) = self.visit(node.left)
		(rExpr, rstatement_list) = self.visit(node.right)
		sumTmpVar = self._makeTmpVar()
		addNode = Add(( lExpr, rExpr ))
		return (Name(sumTmpVar), lstatement_list + rstatement_list + [Assign( [AssName(sumTmpVar, 'OP_ASSIGN')], addNode)])
	
	def visit_UnarySub(self,node):
		(expr, statement_list) = self.visit(node.expr)
		tmpVar = self._makeTmpVar()
		return (Name(tmpVar), statement_list + [Assign( [AssName(tmpVar, 'OP_ASSIGN')], UnarySub(expr))])
	
	def visit_CallFunc(self,node):
		tmpVar = self._makeTmpVar()
		return (Name(tmpVar), [Assign( [AssName(tmpVar, 'OP_ASSIGN')], node)])
