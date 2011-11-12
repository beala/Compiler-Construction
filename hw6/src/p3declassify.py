from astvisitor import *
from compiler.ast import *
from p3ast import *

class P3Declassify(ASTVisitor):
	# Private Attributes: ######################################################################################
	_curTmpVar = 0
	_curTmpMethod = 0
	# Private Methods: #########################################################################################
	def _makeTmpVar(self):
		self._curTmpVar += 1
		return "declass_tmp_" + str(self._curTmpVar)
	def _makeTmpMethod(self):
		self._curTmpMethod += 1
		return "declass_tmp_method" + str(self._curTmpMethod)
	def _makeAssign(self, lhs, rhs):
		return Assign([AssName(lhs, 'OP_ASSIGN')], rhs)
	def _makeAssignAssAttr(self, expr, attrName, rhs):
		return Assign([AssAttr(Name(expr), attrName, 'OP_ASSIGN')], rhs)
	def _iterateOverAndVisit(self, toIterate, curClass):
		result = []
		for item in toIterate:
			newItem = self.visit(item, curClass)
			if isinstance(newItem, list):
				result += newItem
			else:
				result.append(newItem)
		return result

	# Visitor Methods: #########################################################################################
	def visit_Class(self, ast, curClass):
		# Make a class, and assign it to a tmpVar
		classTmp = self._makeTmpVar()
		tmpAssign = self._makeAssign(classTmp, CreateClass(ast.bases))
		# Declassify the body and pass down the current class name.
		tmpBody = self.visit(ast.code, classTmp)
		# Assign the tmpVar to the class's real name
		classAssign = self._makeAssign(ast.name, Name(classTmp))
		# Return class creation + the body + the class assignment
		return [tmpAssign] + tmpBody.nodes + [classAssign]

	def visit_Assign(self, ast, curClass):
		newAssignExpr = self.visit(ast.expr, curClass)
		# If it's an AssAttr, then call the correct runtime func (SetAttr)
		#	also happens if we are in a class scope!
		if isinstance(ast.nodes[0], AssAttr):
			assAttrNode = ast.nodes[0]
			# Declassify the exprs
			newAssignExpr = self.visit(ast.expr, curClass)
			# Return the new SetAttr node to replace the assign node.
			return Assign([AssAttr(assAttrNode.expr, assAttrNode.attrname, assAttrNode.flags)], newAssignExpr)
		elif curClass != None:
			#inside a class, so we must convert into an AssAttr
			assNameNode = ast.nodes[0]
			newAssignExpr = self.visit(ast.expr, curClass)
			return Assign([AssAttr(Name(curClass), assNameNode.name, assNameNode.flags)], newAssignExpr)
		else:
			# Do ast.nodes need to be declassified? I don't think so.
			return Assign(ast.nodes, newAssignExpr)

	def visit_Getattr(self, ast, curClass):
		newGetAttrExpr = self.visit(ast.expr, curClass)
		return Getattr(newGetAttrExpr, ast.attrname)

	def visit_Name(self, ast, curClass):
		if curClass== None:
			return ast
		else:
			return IfExp(HasAttr(Name(curClass), ast.name), Getattr(Name(curClass), ast.name), ast)

	def visit_CallFunc(self, ast, curClass):
		newArgs = self._iterateOverAndVisit(ast.args, curClass)
		#newNode = self.visit(ast.node, curClass)
		return CallFunc(ast.node, newArgs)
	
	def visit_Module(self, ast, curClass):
		# Not in a class at the module level, so pass down None
		return Module(None,self.visit(ast.node, None))
	
	def visit_Stmt(self, ast, curClass):
		newNodes = self._iterateOverAndVisit(ast.nodes, curClass)
		return Stmt(newNodes)

	def visit_Printnl(self, ast, curClass):
		newNodes = self.visit(ast.nodes[0], curClass)
		return Printnl([newNodes], ast.dest)

	def visit_AssName(self, ast, curClass):
		newName = self.visit(ast.name, curClass)
		return AssName(newName, ast.flags)

	def visit_Discard(self, ast, curClass):
		newExpr = self.visit(ast.expr, curClass)
		return Discard(newExpr)

	def visit_Const(self, ast, curClass):
		return ast

	def visit_Add(self, ast, curClass):
		newLeft = self.visit(ast.left, curClass)
		newRight = self.visit(ast.right, curClass)
		return Add((newLeft, newRight))

	def visit_UnarySub(self, ast, curClass):
		newExpr = self.visit(ast.expr, curClass)
		return UnarySub(newExpr)

	def visit_Compare(self, ast, curClass):
		newExpr = self.visit(ast.expr, curClass)
		newOps2 = self.visit(ast.ops[0][1], curClass)
		return Compare(newExpr, [(ast.ops[0][0], newOps2)] )

	def _visit_AndOrList(self, ast, curClass, makeNodeFunc):
		newNodes = self._iterateOverAndVisit(ast.nodes, curClass)
		return makeNodeFunc(newNodes)

	def visit_And(self, ast, curClass):
		return self._visit_AndOrList(ast, curClass, lambda arg: And(arg))

	def visit_Or(self, ast, curClass):
		return self._visit_AndOrList(ast, curClass, lambda arg: Or(arg))

	def visit_List(self, ast, curClass):
		return self._visit_AndOrList(ast, curClass, lambda arg: List(arg))

	def visit_Dict(self, ast, curClass):
		newItems = []
		for item in ast.items:
			newItems.append( (self.visit(item[0], curClass), self.visit(item[1], curClass)) )
		return Dict(newItems)

	def visit_Subscript(self, ast, curClass):
		newExpr = self.visit(ast.expr, curClass)
		newSubs = self._iterateOverAndVisit(ast.subs, curClass)
		return Subscript(newExpr, ast.flags, newSubs)

	def visit_IfExp(self, ast, curClass):
		newTest = self.visit(ast.test, curClass)
		newThen = self.visit(ast.then, curClass)
		newElse_= self.visit(ast.else_, curClass)
		return IfExp(newTest, newThen, newElse_)

	def visit_Not(self, ast, curClass):
		newExpr = self.visit(ast.expr, curClass)
		return Not(newExpr)

	def visit_Function(self, ast, curClass):
		if curClass != None:
			newFuncName = self._makeTmpMethod()
			newCode = self.visit(ast.code, curClass)
			newFunc = Function(ast.decorators, newFuncName, ast.argnames, ast.defaults, ast.flags, ast.doc, newCode)
			newAssign = self._makeAssignAssAttr(curClass, ast.name, Name(newFuncName))
			return [newFunc] + [newAssign]
		else:
			return ast

	def visit_Lambda(self, ast, curClass):
		newCode = self.visit(ast.code, curClass)
		return Lambda(ast.argnames, ast.defaults, ast.flags, newCode)
	def visit_Return(self, ast, curClass):
		newCode = self.visit(ast.value, curClass)
		return Return(newCode)	
	def visit_If(self, ast, curClass):
		newTest = self.visit(ast.tests[0][0], curClass)
		newThen = self.visit(ast.tests[0][1], curClass)
		newElse = self.visit(ast.else_, curClass)
		return If([(newTest, newThen)], newElse)
	def visit_While(self, ast, curClass):
		newTest = self.visit(ast.test, curClass)
		newBody = self.visit(ast.body, curClass)
		return While(newTest, newBody, None)


