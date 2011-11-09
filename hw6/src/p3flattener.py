from p2flattener import *
class P3ASTFlattener(P2ASTFlattener):
	def visit_If(self, node):
		(fe1, se1) = self.visit(node.tests[0][0])
		se2 = self.visit(node.tests[0][1]) #is a Stmt node
		se3 = self.visit(node.else_) #is a Stmt node
		newIf = If([(fe1, se2)], se3)
		return se1 + [newIf]
	def visit_While(self, node):
		(fe1, se1) = self.visit(node.test)
		se2 = self.visit(node.body) #is a Stmt node
		#whileTest = Stmt(se1+[InjectFrom(Const(0),IntegerCompare(fe1, [("==", Const(1))]))])
		whileTest = Stmt(se1+ [fe1])
		return [While(whileTest, se2, None)]

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
