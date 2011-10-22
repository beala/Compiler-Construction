from astvisitor import *
from p2getfreevars import *
from p1ast import *
from p2ast import *

class P2Closure(ASTVisitor):
	# Private Attributes: ###################################################################################
	_globalFunctionCounter = 0
	_curTmpVar = 0

	# Private Methods: ######################################################################################
	def _makeGlobalName(self):
		self._globalFunctionCounter += 1
		return "lambda"+str(self._globalFunctionCounter)

	def _makeTmpVar(self):
		self._curTmpVar += 1
		return "closure" + str(self._curTmpVar)

	def _createMainFunc(self, fun_list, main_ast):
		mainFunc = Function(None, Name('main'), [], None, 0, None, Stmt(main_ast.node.nodes + [Return(Const(0))]))
		mainFunc.localVars = main_ast.localVars
		return fun_list + [mainFunc]
	
	# Visitor Methods: ######################################################################################
	def visit_Module(self, node):
		(body, funs) = self.visit(node.node)
		newModule = Module(node.doc, body)
		newModule.localVars = node.localVars
		return (newModule, funs)
	def visit_Stmt(self, node):
		nodeList = []
		funList = []
		for element in node.nodes:
			(stmt, funs) = self.visit(element)
			nodeList.append(stmt)
			funList.extend(funs)
		return (Stmt(nodeList), funList)

	def visit_Lambda(self, node):
		# Recurse on the body to get the 'newbody'
		(newBody, funs) = self.visit(node.code)
		# Get a name for this lambda
		globalName = self._makeGlobalName()
		# Create function definition
		# TODO: Put freevar code in 'newCodeHeader' after we implement heapify
		newCodeHeader = []
		newCode = newBody.nodes
		newFunDef = Function(None, Name(globalName), node.argnames, node.defaults, node.flags, None, Stmt(newCodeHeader + newCode))
		newFunDef.localVars = node.localVars
		# TODO: Add freevar code to CreateClosure (after we implement heapify)
		return (CreateClosure(Name(globalName), InjectFrom(Const(3), List([]))), funs + [newFunDef]) 

	def visit_CallFunc(self, node):
		if node.node.name == 'input':
			return (node, [])
		
		# Recurse into name and arguments
		# The funs_arg/name will be added to the function list that's returned.
		# The body_arg/name will be used when creating the new Let node that's returned.
		(body_name, funs_name) = self.visit(node.node)
		body_arg = []
		funs_arg = []
		for arg in node.args:
			(body2, funs2) = self.visit(arg)
			body_arg += [body2]
			funs_arg += funs2
		
		# TODO: Populate this list once we get heapify working
		freeVars = []
		newTmpVar = Name(self._makeTmpVar())
		newLet = Let(newTmpVar, body_name, CallUserDef(GetFunPtr(newTmpVar), [GetFreeVars(newTmpVar)] + body_arg))
		return (newLet, funs_arg + funs_name)

	def visit_Printnl(self, node):
		(body_nodes, fun_nodes) = self.visit(node.nodes[0])
		return (Printnl([body_nodes], node.dest), fun_nodes)

	def visit_Const(self, node):
		return (node, [])
	def visit_Name(self, node):
		return (node, [])
	def visit_Assign(self, node):
		body_node = []
		funs_node = []
		for element in node.nodes:
			(body, funs) = self.visit(element)
			body_node += [body]
			funs_node += funs
		(body_expr, funs_expr) = self.visit(node.expr)
		return (Assign(body_node, body_expr), funs_node + funs_expr)

	def visit_AssName(self, node):
		return (node, [])

	def visit_UnarySub(self, node):
		(body, funs) = self.visit(node.expr)
		return (UnarySub(body), funs)

	def visit_Or(self, node):
		body_nodes = []
		funs_nodes = []
		for node in node.nodes:
			(body, funs) = self.visit(node)
			body_nodes += [body]
			funs_nodes += funs
		return (Or(body_nodes), funs_nodes)

	def visit_And(self, node):
		body_nodes = []
		funs_nodes = []
		for node in node.nodes:
			(body, funs) = self.visit(node)
			body_nodes += [body]
			funs_nodes += funs
		return (And(body_nodes), funs_nodes)

	def visit_Not(self, node):
		(body, funs) = self.visit(node.expr)
		return (Not(body), funs)

	def visit_Compare(self, node):
		(body_expr, funs_expr) = self.visit(node.expr)
		(body_ops, funs_ops) = self.visit(node.ops[0][1])
		return (Compare(body_expr, [(node.ops[0][0], body_ops)]), funs_expr + funs_ops)
	
	def visit_IntegerCompare(self, node):
		(body_expr, funs_expr) = self.visit(node.expr)
		(body_ops, funs_ops) = self.visit(node.ops[0][1])
		return (IntegerCompare(body_expr, [(node.ops[0][0], body_ops)]), funs_expr + funs_ops)
	def visit_BigCompare(self, node):
		(body_expr, funs_expr) = self.visit(node.expr)
		(body_ops, funs_ops) = self.visit(node.ops[0][1])
		return (BigCompare(body_expr, [(node.ops[0][0], body_ops)]), funs_expr + funs_ops)
	def visit_IfExp(self, node):
		(body_test, funs_test) = self.visit(node.test)
		(body_then, funs_then) = self.visit(node.then)
		(body_else_, funs_else_) = self.visit(node.else_)
		return (IfExp(body_test, body_then, body_else_), funs_test + funs_then + funs_else_)

	def visit_List(self, node):
		body_nodes = []
		funs_nodes = []
		for node in node.nodes:
			(body, funs) = self.visit(node)
			body_nodes += [body]
			funs_nodes += funs
		return (List(body_nodes), funs_nodes)

	def visit_Dict(self, node):
		item_nodes = []
		item_funs = []
		for (key, val) in node.items:
			(tmpkeyNodes, tmpkeyFuns) = self.visit(key)
			(tmpvalNodes, tmpvalFuns) = self.visit(val)
			item_nodes.append((tmpkeyNodes, tmpvalNodes))
			item_funs.extend(tmpkeyFuns + tmpvalFuns)
		return (Dict(item_nodes), item_funs)

	def visit_Subscript(self, node):
		(expr, expr_funs) = self.visit(node.expr)
		(sub, sub_funs) = self.visit(node.subs[0])
		return (Subscript(expr, node.flags, [sub]), expr_funs + sub_funs)

	def visit_Return(self, node):
		(value, funs) = self.visit(node.value)
		return (Return(value), funs)

	def visit_Let(self, node):
		(var, var_funs) = self.visit(node.var)
		(rhs, rhs_funs) = self.visit(node.rhs)
		(body, body_funs) = self.visit(node.body)
		return (Let(var, rhs, body), var_funs + rhs_funs + body_funs)

	def visit_InjectFrom(self, node):
		(arg, funs_arg) = self.visit(node.arg)
		(typ, funs_typ) = self.visit(node.typ)
		return (InjectFrom(typ, arg), funs_arg + funs_typ)		

	def visit_ProjectTo(self, node):
		(arg, funs_arg) = self.visit(node.arg)
		(typ, funs_typ) = self.visit(node.typ)
		return (ProjectTo(typ, arg), funs_arg + funs_typ)		

	def visit_GetTag(self, node):
		(arg, funs_arg) = self.visit(node.arg)
		return (GetTag(arg), funs_arg)

	def visit_Discard(self, node):
		(expr, funs_expr) = self.visit(node.expr)
		return (Discard(expr), funs_expr)
	

	def visit_BigAdd(self, node):
		(body_left, funs_left) = self.visit(node.left)
		(body_right, funs_right) = self.visit(node.right)

		return (BigAdd((body_left, body_right) ), funs_left + funs_right)

	def visit_IntegerAdd(self, node):
		(body_left, funs_left) = self.visit(node.left)
		(body_right, funs_right) = self.visit(node.right)

		return (IntegerAdd((body_left, body_right) ), funs_left + funs_right)
	
	# Public Methods: #######################################################################################
	def doClosure(self, ast):
		(main_ast, fun_list) = self.visit(ast)
		return self._createMainFunc(fun_list, main_ast)

if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
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
	P2Uniquify().print_ast(Stmt(P2Closure().doClosure(to_closure_convert)))
