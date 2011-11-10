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
		# Make a class, and assign it to a tmpVar
		classTmp = self._makeTmpVar()
		tmpAssign = self._makeAssign(classTmp, CreateClass(ast.bases))
		# Declassify the body
		tmpBody = self.visit(ast.code)
		# Assign the tmpVar to the class's real name
		classAssign = self._makeAssign(ast.name, classTmp)
		# Return class creation + the body + the class assignment
		return [tmpAssign] + tmpBody.nodes + [classAssign]

	visit_Assign(self, ast):
		newAssignExpr = self.visit(ast.expr)
		# If it's an AssAttr, then call the correct runtime func (SetAttr)
		if isinstance(ast.nodes[1], AssAttr):
			assAttrNode = ast.nodes[1]
			# Declassify the exprs
			newAssAttrExpr = self.visit(assAttrNode.expr)
			# Return the new SetAttr node to replace the assign node.
			return SetAttr(newAssAttrExpr, assAttrNode.attrname, newAssignExpr)
		else:
			# Do ast.nodes need to be declassified? I don't think so.
			return Assign(ast.nodes, newAssignExpr)

	visit_Getattr(self, ast):
		newGetAttrExpr = self.visit(ast.expr)
		return GetAttrRuntime(newGetAttrExpr, ast.attrname)


	visit_Module(self, ast):
		return self.visit(ast.node)

	visit_Stmt(self, ast):
		declassifiedStmts = []
		for stmt in ast.nodes:
			declassifiedStmts.append(self.visit(stmt))
		return Stmt(declassifiedStmts)

