#!/usr/bin/python

#MyFlattener.py
from compiler.ast import *
import compiler
import sys
import string

class MyFlattener:
	#class methods		
	def get_generated_code(self):
		return self.__generated_code
	def flatten(self, ast):
		flat_ast = compiler.ast.Module(None, compiler.ast.Stmt([]))
		self.flatten_sub(ast, 0, flat_ast)
		return flat_ast
	
	# Desc: Recursive flattening function.
	# Args: ast: the AST to be flattened.
	#		tmp_num: Number cooresponding to the next tmp var to be used.
	#		flat_ast: Contains the new AST representing the flattened program.
	# Returns: A new AST representing the flattened program.
	def flatten_sub(self, ast, tmp_num, flat_ast):
		if isinstance(ast, Module):
			# Nothing to do. Just go to the next node.
			self.flatten_sub(ast.node, tmp_num, flat_ast)
			return 0
		elif isinstance(ast, Stmt):
			for node in ast.nodes:
				tmp_num = self.flatten_sub(node, tmp_num, flat_ast)
				# Increment tmp_num for next Stmt so the tmp variable never get
				# the same name.
				tmp_num += 1  
			return tmp_num
		elif isinstance(ast, Discard):
			# Nothing to do. Just go to the next node.
			self.flatten_sub(ast.expr, tmp_num, flat_ast)
			return tmp_num
		elif isinstance(ast, Const):
			# Build statement to assign the constant value to a tmp variable
			stmt = 'tmp' + str(tmp_num) + ' = ' + str(ast.value)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number coorsponding to the tmp variable
			return tmp_num
		elif isinstance(ast, Add):
			# Get the two tmp variable to be added by recursing
			left = self.flatten_sub(ast.left, tmp_num, flat_ast)
			right = self.flatten_sub(ast.right, left + 1, flat_ast)
			# Build a statement to add the two tmp variables
			# and assign that value to a new tmp variable
			stmt = 'tmp' + str(right + 1) + ' = tmp' + str(left) + ' + tmp' + str(right)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number cooresponding to the new tmp variable.
			return right + 1
		elif isinstance(ast, UnarySub):
			# Get the tmp variable that needs to be negated.
			to_negate = self.flatten_sub(ast.expr, tmp_num, flat_ast)
			# Negate the variable, and assign to a new variable.
			stmt = 'tmp' + str(to_negate + 1) + ' = -tmp' + str(to_negate)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number cooresponding to the tmp variable.
			return to_negate + 1
		elif isinstance(ast, CallFunc):
			# CallFunc always refers to an input() (in P0, at least).
			# So, build a statement calling input() and storing it to a tmp var.
			stmt = 'tmp' + str(tmp_num) + ' = input()'
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number cooresponding to the tmp var.
			return tmp_num
		elif isinstance(ast, Printnl):
			# Get the tmp variable to be printed.
			to_print = self.flatten_sub(ast.nodes[0], tmp_num, flat_ast)
			# Build statement printing that tmp var.
			stmt = 'print tmp' + str(to_print)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Nothing to return. print is always an upper node.
			return to_print
		elif isinstance(ast, Assign):
			# Get the name of the variable being assigned to (l value)
			var_name = "__"+ast.nodes[0].name
			# Get the tmp var containing the value to be assigned (r value)
			right = self.flatten_sub(ast.expr, tmp_num, flat_ast)
			stmt = var_name + ' = tmp' + str(right)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Nothing to return. An upper node.		
			return right
		elif isinstance(ast, Name):
			# Assign the variable to a tmp var.
			ast.name = "__"+ast.name
			stmt = 'tmp' + str(tmp_num) + ' = ' + ast.name
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			return tmp_num
		else:
			raise Exception("Error: Unrecognized node/object type.")
