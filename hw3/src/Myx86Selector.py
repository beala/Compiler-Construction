#!/usr/bin/python

#Myx86Selector.py
from compiler.ast import *
import compiler
import sys
import string
import x86

class Myx86Selector:
	#class variables
	__dict_vars = {} #dictionary (associative array) of variable names to memory locations relative to ebp
	__ir = []
	__currentTmpVar = 0;

	#class methods		
	def _update_dict_vars(self, var_name):
		if self.__dict_vars.has_key(var_name):
			return self.__dict_vars.get(var_name)

		self.__dict_vars[var_name] = x86.varNode(var_name)
		return self.__dict_vars.get(var_name)
	
	def _update_dict_vars(self, var_name, var_node):
		if self.__dict_vars.has_key(var_name):
			return self.__dict_vars.get(var_name)

		self.__dict_vars[var_name] = var_node
		return self.__dict_vars.get(var_name)

	def makeTmpVar(self):
		new_tmp_name = "__tmpIR" + currentTmpVar
		self.__currentTmpNode = x86.VarNode( new_tmp_name )
		self.__currentTmpVar = self.__currentTmpVar + 1
		self._update_dict_vars(new_tmp_name, self.__currentTmpNode)
		return self.__currentTmpNode

	def getTmpVar(self):
		return self.__currentTmpNode
	
    #TODO: Do something about this.
	#def _encapsulate_generated_code(self):
	#	self.__generated_code = ".globl main\nmain:\npushl %ebp\nmovl %esp, %ebp\nsubl $"+str(self.__stack_offset)+",%esp\n" + self.__generated_code + "movl $0, %eax\nleave\nret\n"
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
			# self.__generated_code += "movl $" + str(ast.value) + ", %eax\n"
			self.__ir.add(x86.Movl(x86.ConstNode(ast.value),self.makeTmpVar()) 
			return
		elif isinstance(ast, Add):
			#process LHS, move to %edx
			self.generate_x86_code(ast.left, _dict_vars)
			expr1 = self.makeTmpVar()
			self.__ir.add(x86.Movl(self.getTmpVar(),operand1))
			#process RHS
			self.generate_x86_code(ast.right, _dict_vars)
			#add
			self.__ir.add(x86.Addl(expr1, self.getTmpVar()))
			return
		elif isinstance(ast, UnarySub):
			# negate value and leave in %eax
			self.generate_x86_code(ast.expr, _dict_vars)
			self.__ir.add(x86.Negl(self.getTmpVar()))
			return
		elif isinstance(ast, CallFunc):
			# CallFunc always refers to an input() (in P0, at least).
			self.__ir.add(x86.Call('input'))
			return
		elif isinstance(ast, Printnl):
			#process children
			self.generate_x86_code(ast.nodes[0], _dict_vars)
			
			# get value stored in %eax and push for call to print
			self.__ir.add(x86.Pushl(self.getTempVar()))
			self.__ir.add(x86.Call("print_int_nl"))
			self.__ir.add(x86.Addl(x86.ConstNode(4),x86.Register('esp')))
			return
		elif isinstance(ast, Assign):
			# Get the name of the variable being assigned to (l value)
			var_name = ast.nodes[0].name
			
			#emit our expression (RHS)
			self.generate_x86_code(ast.expr, _dict_vars)
					
			#now, the result of that should be stored in %eax, so do the assignment
			var_LHSnode = self._update_dict_vars(var_name)
			#self.__generated_code += "movl %eax, -"+str(var_offset)+"(%ebp)\n"
			__ir.add(x86.Movl(self.getTmpVar(), var_LHSnode))
			return
		elif isinstance(ast, Name):
			# retrieve var from stack and place into %eax
			# NOTE: this will need to handle function names soon, so this will break in that case! ~ symbol table :S
			self.__ir.add(x86.Movl(self._update_dict_vars(ast.name),self.makeTempVar()))
			return
		else:
			raise Exception("Error: Unrecognized node/object type.")
	def __init__(self,codefile):
		self.generate_x86_code(self.flatten(compiler.parseFile(codefile)),self.__dict_vars)
		self._encapsulate_generated_code()
