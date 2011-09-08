#!/usr/bin/python

#csci4555_compiler.py
from compiler.ast import *
import compiler
import sys
import string
import lexer

class csci4555_compiler:
	#class variables
	__dict_vars = {} #dictionary (associative array) of variable names to memory locations relative to ebp
	__stack_offset = 0
	__generated_code = ""

	#class methods		
	def get_generated_code(self):
		return self.__generated_code
	def flatten(self, ast):
		flat_ast = compiler.ast.Module(None, compiler.ast.Stmt([]))
		self.flatten_sub(ast, 0, flat_ast, self.__dict_vars)
		return flat_ast
	
	# Desc: Recursive flattening function.
	# Args: ast: the AST to be flattened.
	#		tmp_num: Number cooresponding to the next tmp var to be used.
	#		flat_ast: Contains the new AST representing the flattened program.
	# Returns: A new AST representing the flattened program.
	def flatten_sub(self, ast, tmp_num, flat_ast, __dict_vars):
		if isinstance(ast, Module):
			# Nothing to do. Just go to the next node.
			self.flatten_sub(ast.node, tmp_num, flat_ast, self.__dict_vars)
			return 0
		elif isinstance(ast, Stmt):
			for node in ast.nodes:
				tmp_num = self.flatten_sub(node, tmp_num, flat_ast, self.__dict_vars)
				# Increment tmp_num for next Stmt so the tmp variable never get
				# the same name.
				tmp_num += 1  
			return tmp_num
		elif isinstance(ast, Discard):
			# Nothing to do. Just go to the next node.
			self.flatten_sub(ast.expr, tmp_num, flat_ast, self.__dict_vars)
			return tmp_num
		elif isinstance(ast, Const):
			# Build statement to assign the constant value to a tmp variable
			stmt = 'tmp' + str(tmp_num) + ' = ' + str(ast.value)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number coorsponding to the tmp variable
			return tmp_num
		elif isinstance(ast, Add):
			# Get the two tmp variable to be added by recursing
			left = self.flatten_sub(ast.left, tmp_num, flat_ast, self.__dict_vars)
			right = self.flatten_sub(ast.right, left + 1, flat_ast, self.__dict_vars)
			# Build a statement to add the two tmp variables
			# and assign that value to a new tmp variable
			stmt = 'tmp' + str(right + 1) + ' = tmp' + str(left) + ' + tmp' + str(right)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Return the number cooresponding to the new tmp variable.
			return right + 1
		elif isinstance(ast, UnarySub):
			# Get the tmp variable that needs to be negated.
			to_negate = self.flatten_sub(ast.expr, tmp_num, flat_ast, self.__dict_vars)
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
			to_print = self.flatten_sub(ast.nodes[0], tmp_num, flat_ast, self.__dict_vars)
			# Build statement printing that tmp var.
			stmt = 'print tmp' + str(to_print)
			flat_ast.node.nodes.append(compiler.parse(stmt).node.nodes[0])
			# Nothing to return. print is always an upper node.
			return to_print
		elif isinstance(ast, Assign):
			# Get the name of the variable being assigned to (l value)
			var_name = "__"+ast.nodes[0].name
			# Get the tmp var containing the value to be assigned (r value)
			right = self.flatten_sub(ast.expr, tmp_num, flat_ast, self.__dict_vars)
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
			
	def _update_dict_vars(self, var_name):
		self.__stack_offset = self.__stack_offset + 4
		self.__dict_vars[var_name] = self.__stack_offset
		return self.__stack_offset
	def _encapsulate_generated_code(self):
		self.__generated_code = ".globl main\nmain:\npushl %ebp\nmovl %esp, %ebp\nsubl $"+str(self.__stack_offset)+",%esp\n" + self.__generated_code + "movl $0, %eax\nleave\nret\n"
	def generate_x86_code(self, ast, _dict_vars):
		if isinstance(ast, Module):
			# Nothing to do. Just go to the next node.
			self.generate_x86_code(ast.node, _dict_vars)
			return
		elif isinstance(ast, Stmt):
			for node in ast.nodes:
				self.generate_x86_code(node, _dict_vars)
			return
		elif isinstance(ast, Discard):
			# Nothing to do. Just go to the next node.
			self.generate_x86_code(ast.expr, _dict_vars)
			return
		elif isinstance(ast, Const):
			# put constant in general register eax for later assignment (in our flattener, constants are always the RHS of an assignment
			self.__generated_code += "movl $" + str(ast.value) + ", %eax\n" 
			return
		elif isinstance(ast, Add):
			#process LHS, move to %edx
			self.generate_x86_code(ast.left, _dict_vars)
			self.__generated_code += "movl %eax, %edx\n"
			#process RHS
			self.generate_x86_code(ast.right, _dict_vars)
			#add
			self.__generated_code += "addl %edx, %eax\n"
			return
		elif isinstance(ast, UnarySub):
			# negate value and leave in %eax
			self.generate_x86_code(ast.expr, _dict_vars)
			self.__generated_code += "negl %eax\n"
			return
		elif isinstance(ast, CallFunc):
			# CallFunc always refers to an input() (in P0, at least).
			self.__generated_code += "call input\n"
			return
		elif isinstance(ast, Printnl):
			#process children
			self.generate_x86_code(ast.nodes[0], _dict_vars)
			
			# get value stored in %eax and push for call to print
			self.__generated_code += "pushl %eax\n"
			self.__generated_code += "call print_int_nl\n"
			self.__generated_code += "addl $4, %esp\n"
			return
		elif isinstance(ast, Assign):
			# Get the name of the variable being assigned to (l value)
			var_name = ast.nodes[0].name
			
			#emit our expression (RHS)
			self.generate_x86_code(ast.expr, _dict_vars)
					
			#now, the result of that should be stored in %eax, so do the assignment
			try:
				var_offset = _dict_vars[var_name]
				self.__generated_code += "movl %eax, -"+str(var_offset)+"(%ebp)\n"
			except KeyError:
				#this means that the variable was not yet assigned
				var_offset = self._update_dict_vars(var_name)
				self.__generated_code += "movl %eax, -"+str(var_offset)+"(%ebp)\n"
	
			return
		elif isinstance(ast, Name):
			# retrieve var from stack and place into %eax
			# NOTE: this will need to handle function names soon, so this will break in that case! ~ symbol table :S
			try:
				self.__generated_code += "movl -" + str(_dict_vars[ast.name]) + "(%ebp), %eax\n"			
			except KeyError:
				raise Exception("Error: Unassigned variable encountered!")
	
			return
		else:
			raise Exception("Error: Unrecognized node/object type.")
	def __init__(self,codefile):
		parse_lex = lexer.ParserLexer()
		self.generate_x86_code(self.flatten(parse_lex.parseFile(codefile)),self.__dict_vars)
		self._encapsulate_generated_code()

#mycode = sys.stdin.readlines()
#test = csci4555_compiler(string.join(mycode,"\n"))
#print test.get_generated_code()
myfile = sys.argv[1]
basename = myfile[:len(myfile)-3]
compileObj = csci4555_compiler(myfile)
file = open(basename+".s","w")
file.write(compileObj.get_generated_code())
file.close()
