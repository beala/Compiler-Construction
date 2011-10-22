from p1flattener import *
from compiler.ast import *
from p2explicate import *
from p2ast import *
from p1ast import *

class P2ASTFlattener(P1ASTFlattener):
	def _renameVar(self, var_name):
		return var_name

	def visit_Function(self, node):
		code_stmt = self.visit(node.code)
		newFunction = Function(node.decorators, node.name, node.argnames, node.defaults, node.flags, node.doc, Stmt(code_stmt.nodes))
		newFunction.localVars = node.localVars
		return newFunction
	#def visit_Stmt(self, node):
	#	result_list = []
	#	stmt_list = []
	#	for element in node.nodes:
	#		(result, stmt) = self.visit(element)
	#		result_list += result
	#		stmt_list += stmt

	def visit_Return(self, node):
		(flat_value , stmt_value) = self.visit(node.value)
	#	tmpVar = self._makeTmpVar()
	#	newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], flat_value)
	#	return (Return(tmpVar), stmt_value + [newAssign])
		return stmt_value + [Return(flat_value)]
	def visit_CreateClosure(self, node):
		(flat_name, name_stmt) = self.visit(node.name)
		(flat_env, env_stmt) = self.visit(node.env)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], CreateClosure(flat_name, flat_env))
		return (Name(tmpVar), env_stmt + name_stmt + [newAssign])
	def visit_CallUserDef(self, node):
		(node_result, node_stmt) = self.visit(node.node)
		args_result = []
		args_stmt = []
		for element in node.args:
			(result, stmt) = self.visit(element)
			args_result += [result]
			args_stmt += stmt
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], CallUserDef(node_result, args_result))
		return (Name(tmpVar), node_stmt + args_stmt + [newAssign])
	def visit_GetFunPtr(self, node):
		(name_result, name_stmts) = self.visit(node.name)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], GetFunPtr(name_result))
		return (Name(tmpVar), name_stmts + [newAssign])
	def visit_GetFreeVars(self, node):
		(name_result, name_stmts) = self.visit(node.name)
		tmpVar = self._makeTmpVar()
		newAssign = Assign([AssName(tmpVar, 'OP_ASSIGN')], GetFreeVars(name_result))
		return (Name(tmpVar), name_stmts + [newAssign])
	def visit_list(self, node):
		func_list = []
		for func in node:
			func_list += [self.visit(func)]
		return func_list
	def visit_Name(self, node):
		return (node, [])

if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	from p2closure import *
	print "-"*20 + "Parsed AST" + "-"*20 
	if os.path.isfile(sys.argv[1]):
		print compiler.parseFile(sys.argv[1])
		to_explicate = compiler.parseFile(sys.argv[1])
	else:
		print compiler.parse(sys.argv[1])
		to_explicate = compiler.parse(sys.argv[1])
	print "-"*20 + "Uniquified AST" + "-"*20
	to_explicate = P2Uniquify().visit(to_explicate)
	P2Uniquify().print_ast(to_explicate.node)
	print "-"*20 + "Explicated AST" + "-"*20
	to_closure_convert = P2Explicate().visit(to_explicate)
	P2Uniquify().print_ast(to_closure_convert.node)
	(ast, fun_list) = P2Closure().visit(to_closure_convert)
	print "-"*20 + "Global Func List" + "-"*20
	P2Uniquify().print_ast(Stmt(fun_list)) 
	print "-"*20 + "Closure Converted AST" + "-"*20
	P2Uniquify().print_ast(ast.node)
	print "-"*20 + "Final Func List" + "-"*20
	to_flatten = P2Closure().doClosure(to_closure_convert)
	P2Uniquify().print_ast(Stmt(to_flatten))
	print "-"*20 + "Flattened Func List" + "-"*20
	flattened = P2ASTFlattener().visit(to_flatten)
	P2Uniquify().print_ast(Stmt(flattened))
