from MyFlattener import *
from compiler.ast import *
from p1explicate import *

class P1ASTFlattener(P0ASTFlattener):
	def visit_Let(self, node):
		(flatrhs, stmt_list) = self.visit(node.rhs)
		newName = self._renameVar(node.var.name)
		newAssign = Assign([AssName(newName, 'OP_ASSIGN')], flatrhs)
		(body_result, stmt_list_body) = self.visit(node.body)
		return (body_result, stmt_list + [newAssign] + stmt_list_body)

	def visit_IfExp(self, node):
		(fe1, se1) = self.visit(node.test)
		(fe2, se2) = self.visit(node.then)
		(fe3, se3) = self.visit(node.else_)
		tmpVar = self._makeTmpVar()
		ifAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], fe2)
		elseAssign = Assign([AssName(tmpVar,'OP_ASSIGN')], fe3)
		newIf = If([ (fe1, Stmt(se2 +[ifAssign])) ], Stmt(se3+[elseAssign]))
		return (Name(tmpVar), se1 + [newIf])
	
	def visit_Compare(self, node):
		(expr, stmt_list) = self.visit(node.expr)
		(flat_ops, stmt_list_ops) = self.visit(node.ops[0][1])
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Compare(expr, [(node.ops[0][0], flat_ops)]))
		return (Name(tmpVar), stmt_list + stmt_list_ops + [newAssign])

	def visit_Or(self, node):
		flattenedTuples = []
		for element in node.nodes:
			flattenedTuples.append(self.visit(element))
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Or([element for (element,stmt) in flattenedTuples]))
		myStmtList = []
		for (element,stmt) in flattenedTuples:
			myStmtList += stmt
		return (Name(tmpVar), myStmtList  + [newAssign])
	
	def visit_And(self, node):
		flattenedTuples = []
		for element in node.nodes:
			flattenedTuples.append(self.visit(element))
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], And([element for (element,stmt) in flattenedTuples]))
		myStmtList = []
		for (element,stmt) in flattenedTuples:
			myStmtList += stmt
		return (Name(tmpVar), myStmtList + [newAssign])

	def visit_Not(self, node):
		(expr, stmt_list) = self.visit(node.expr)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpvar, 'OP_ASSIGN')], Not(expr))
		return(Name(tmpVar), stmt_list + [newAssign])

	def visit_Subscript(self, node):
		myCurrentTemp = self._getCurrentTmpVar()
		(flat_expr, stmt_list_expr) = self.visit(node.expr)
		(flat_subs, stmt_list_subs) = self.visit(node.subs[0])
		tmpVar = self._makeTmpVar()
		if node.flags == 'OP_APPLY':
			newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Subscript(flat_expr, 'OP_APPLY', [flat_subs]))
			return (Name(tmpVar), stmt_list_expr + stmt_list_subs + [newAssign])
		else:
			newAssign1 = Assign([Subscript(flat_expr, 'OP_ASSIGN', [flat_subs])], Name(myCurrentTemp))
			newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Subscript(flat_expr, 'OP_APPLY', [flat_subs]))
			return (Name(tmpVar), stmt_list_expr + stmt_list_subs + [newAssign1] + [newAssign])

	def visit_List(self,node):
		tupleList = []
		for element in node.nodes:
			tupleList.append(self.visit(element))
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], List([element for (element,stmt) in tupleList]))
		myStmtList = []
		for (element,stmt) in tupleList:
			for element2 in stmt:
				myStmtList.append(element2)
		return (Name(tmpVar), myStmtList + [newAssign])

	def visit_Dict(self,node):
		tupleTupleList = []
		for element in node.items:
			tupleTupleList.append( (self.visit(element[0]), self.visit(element[1])) )
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Dict([ (flat_key[0], flat_value[0]) for (flat_key, flat_value) in tupleTupleList ]))
		myFlatValueandKeyList = []
		for (flat_key, flat_value) in tupleTupleList:
			myFlatValueandKeyList += flat_key[1]
			myFlatValueandKeyList += flat_value[1]
		return (Name(tmpVar), myFlatValueandKeyList + [newAssign])

	def visit_GetTag(self, node):
		(expr, stmt) = self.visit(node.arg)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], GetTag(expr))
		return(Name(tmpVar), stmt + [newAssign])

	def visit_InjectFrom(self, node):
		(expr1, stmt1) = self.visit(node.typ)
		(expr2, stmt2) = self.visit(node.arg)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], InjectFrom(expr1, expr2))
		return (Name(tmpVar), stmt1 + stmt2 + [newAssign])

	def visit_ProjectTo(self, node):
		(expr1, stmt1) = self.visit(node.typ)
		(expr2, stmt2) = self.visit(node.arg)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], ProjectTo(expr1, expr2))
		return (Name(tmpVar), stmt1 + stmt2 + [newAssign])

	def visit_IntegerAdd(self, node):
		(expr_left, stmt_left) = self.visit(node.left)
		(expr_right, stmt_right) = self.visit(node.right)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], IntegerAdd((expr_left, expr_right)))
		return (Name(tmpVar), stmt_left + stmt_right + [newAssign])

	def visit_BigAdd(self, node):
		(expr_left, stmt_left) = self.visit(node.left)
		(expr_right, stmt_right) = self.visit(node.right)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], BigAdd((expr_left, expr_right)))
		return (Name(tmpVar), stmt_left + stmt_right + [newAssign])

	# Debugging methods: #############################################################################
	def print_ast(self, stmt_ast, tabcount):
		for node in stmt_ast.nodes:
			if isinstance(node, If):
				print '\t' * tabcount + 'If: ' + str(node.tests[0][0]) + ' then:'
				self.print_ast(node.tests[0][1], tabcount+1)
				print '\t' * (tabcount) + 'Else: '
				self.print_ast(node.else_, tabcount+1)
				print '\t' * (tabcount) + 'End If'
			else:
				print '\t' * (tabcount) + str(node)
 
if __name__ == "__main__":
	import sys
	import compiler
	print '-' * 10 + 'Parsed AST' + '-' * 10
	import os
	if os.path.isfile(sys.argv[1]):
		print str(compiler.parseFile(sys.argv[1])) + '\n'
		flat_ast = P1ASTFlattener().visit(P1Explicate().visit(compiler.parseFile(sys.argv[1])))
	else:
		print str(compiler.parse(sys.argv[1])) + '\n'
		flat_ast = P1ASTFlattener().visit(P1Explicate().visit(compiler.parse(sys.argv[1])))
	print '-' * 10 + 'Flat AST' + '-' * 10
	P1ASTFlattener().print_ast(flat_ast.node, 0)	
