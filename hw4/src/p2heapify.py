from compiler.ast import *
from astvisitor import *
from p2getfreevars import *
from p2getlocals import *

class P2Heapify(ASTVisitor):
	def visit_Module:
	def visit_Lambda(self, ast):
		(freeBelow, body) = self.visit(node.body)
		freeVars = P2GetFreeVars().visit(node)
		localVars = getLocals(node)
		for stmt in ast.code.nodes
			if isinstance(stmt, Lambda)
				
	def visit_Stmt:
	def visit_Name:
	def visit_Assign:
	def visit_AssName
	
	#uninteresting -- recurse
