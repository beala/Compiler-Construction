from p2flattener import *
from p3ast import *
class P3ASTFlattener(P2ASTFlattener):
	def visit_If(self, node):
		(test_result, test_flat) = self.visit(node.tests[0][0])
		then_flat = self.visit(node.tests[0][1]) #is a Stmt node
		else_flat = self.visit(node.else_) #is a Stmt node
		#newIf = If([(fe1, se2)], se3)
		#return se1 + [newIf]
		return test_flat + [If([(test_result, then_flat)], else_flat)]
	def visit_While(self, node):
		(test_result, test_flat) = self.visit(node.test)
		body_flat = self.visit(node.body) #is a Stmt node
		#whileTest = Stmt(se1+[InjectFrom(Const(0),IntegerCompare(fe1, [("==", Const(1))]))])
		#whileTest = Stmt(se1])
		#return [While(whileTest, se2, None)]
		return [While(Stmt(test_flat + [test_result]), body_flat, None)]
	def visit_CreateClass(self, node):
		flattened_result_base_list = []
		flattened_stmt_base_list = []
		#for base in node.bases:
		#	(flattened_result, flattened_stmt) = self.visit(base)
		#	flattened_result_base_list.append(flattened_result)
		#	flattened_stmt_base_list += flattened_stmt
		(flattened_result_base_list, flattened_stmt_base_list) = self.visit(InjectFrom(Const(3), List(node.bases)))
		tmpVar = self._makeTmpVar()
		newCreateClass = Assign([AssName(tmpVar, 'OP_ASSIGN')],CreateClass(flattened_result_base_list))
		return (Name(tmpVar), flattened_stmt_base_list + [newCreateClass])
	def visit_Getattr(self, node):
		(expr_result, expr_stmt) = self.visit(node.expr)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], Getattr(expr_result, node.attrname))
		return (Name(tmpVar), expr_stmt + [newAssign])
if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p3uniquify import *
	from p3explicate import *
	from p3heapify import *
	from p3closure import *
	print "-"*20 + "Parsed AST" + "-"*20 
	if os.path.isfile(sys.argv[1]):
		print compiler.parseFile(sys.argv[1])
		to_explicate = compiler.parseFile(sys.argv[1])
	else:
		print compiler.parse(sys.argv[1])
		to_explicate = compiler.parse(sys.argv[1])
	print "-"*20 + "Uniquified AST" + "-"*20
	to_explicate = P3Uniquify().visit(to_explicate)
	P3Uniquify().print_ast(to_explicate.node)
	print "-"*20 + "Explicated AST" + "-"*20
	explicated = P3Explicate().visit(to_explicate)
	P3Uniquify().print_ast(explicated.node)
	print "-"*20 + "Heapified AST" + "-"*20
	heapified = P3Heapify().visit(explicated)
	#print heapified	
	P3Heapify().print_ast(heapified.node)
	(ast, fun_list) = P3Closure().visit(heapified)
	print "-"*20 + "Global Func List" + "-"*20
	P3Uniquify().print_ast(Stmt(fun_list)) 
	print "-"*20 + "Closure Converted AST" + "-"*20
	to_flatten = P3Closure().doClosure(heapified)
	P3Uniquify().print_ast(Stmt(to_flatten))
	print "-"*20 + "Flattened Func List" + "-"*20
	flattened = P3ASTFlattener().visit(to_flatten)
	P3Uniquify().print_ast(Stmt(flattened))
