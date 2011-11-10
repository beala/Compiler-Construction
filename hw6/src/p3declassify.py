from astvisitor import *
from compiler.ast import *
from p3ast import *

class P3Declassify(ASTVisitor):
	# Private Attributes: ######################################################################################
	_curTmpVar = 0

	# Private Methods: #########################################################################################
	_makeTmpVar(self):
		self._curTempVar += 1
		return "declass_tmp_" + str(self._curTmpVar)

	_makeAssign(self, lhs, rhs):
		return Assign([AssName(lhs, 'OP_ASSIGN')], rhs)

	# Visitor Methods: #########################################################################################
	visit_Class(self, ast):
		classTmp = self._makeTmpVar()
		tmpAssign = self._makeAssign(classTmp, CreateClass(ast.bases))
		tmpBody = ast.code.nodes
		classAssign = self._makeAssign(ast.name, classTmp)
		return [tmpAssign] + tmpBody + [classAssign]
	
	visit_Module(self, ast):
		return self.visit(ast.node)

	visit_Stmt(self, ast):
		declassifiedStmts = []
		for stmt in ast.nodes:
			declassifiedStmts.append(self.visit(stmt))
		return Stmt(declassifiedStmts)

