from MyFlattener import *
from compiler.ast import *

class P1ASTFlattener(P0ASTFlattener):
	def visit_Let(self, node):
		(flatrhs, stmt_list) = self.visit(node.rhs)
		newAssign = Assign([AssName(node.var.name, 'OP_ASSIGN')], flatrhs)
		(body_result, stmt_list_body) = self.visit(node.body)
		return (body_result, stmt_list + [newAssign] + stmt_list_body)

	def visit_IfExp(self, node):
		(fe1, se1) = self.visit(node.test)
		(fe2, se2) = self.visit(node.then)
		(fe3, se3) = self.visit(node.else_)
		tmpVar = self._makeTmpVar()
		ifAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], fe2)
		elseAssign = Assign([AssName(tmpVar,'OP_ASSIGN')], fe3)
		newIf = If([ (fe1, Stmt(se2 +[ifAssign], None)) ], Stmt(se3+[elseAssign], None))
		return (Name(tmpVar), se1 + [newIf])
				
