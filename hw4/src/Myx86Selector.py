#!/usr/bin/python

#Myx86Selector.py
from compiler.ast import *
import compiler
import sys
import string
import x86
import os
from p2explicate import *
from p2flattener import *
import p1ast
import base64
from p2getlocals import *
class Myx86Selector:
	#class variables
	__dict_vars = {} #dictionary (associative array) of variable names to memory locations relative to ebp
	__currentTmpVar = 0
	_currentLabelNum = 0
	_calleeSaveRegisters = [x86.Register('ebx'),x86.Register('esi'),x86.Register('edi')]
	def emitSetVarNodeText(self,mySet):
		myList = []
		for item in mySet:
			myList.append(str(item))
		return ','.join(myList)
	def emitx86Text(self):
		#emit x86 code
		myString = ""
		for instruction in self.__ir:
			#myString = myString + '\t\tliveset('+self.emitSetVarNodeText(instruction.liveSetBefore)+')\n'
			myString = myString + '\t'+str(instruction)+'\n'
			#myString = myString + '\t\tliveset('+self.emitSetVarNodeText(instruction.liveSetAfter)+')\n'
		return myString
	def calculateLiveSets(self):
		previousLiveSet = set()
		for instruction in reversed(self.__ir):
			previousLiveSet = instruction.doCalculateLiveSet(previousLiveSet)
		
	def _update_dict_vars(self, var_name):
		if self.__dict_vars.has_key(var_name):
			return self.__dict_vars.get(var_name)

		self.__dict_vars[var_name] = x86.VarNode(var_name)
		return self.__dict_vars.get(var_name)
	
	def _update_dict_vars_node(self, var_name, var_node):
		if self.__dict_vars.has_key(var_name):
			return self.__dict_vars.get(var_name)

		self.__dict_vars[var_name] = var_node
		return self.__dict_vars.get(var_name)

	def makeTmpVar(self):
		new_tmp_name = "__tmpIR" + str(self.__currentTmpVar)
		self.__currentTmpNode = x86.VarNode( new_tmp_name )
		self.__currentTmpVar = self.__currentTmpVar + 1
		self._update_dict_vars_node(new_tmp_name, self.__currentTmpNode)
		return self.__currentTmpNode

	def getTmpVar(self):
		return self.__currentTmpNode

	def _makeLabel():
		return 'label' + str(self._currentLabelNum)	

    #TODO: Do something about this.
	#def _encapsulate_generated_code(self):
	#	self.__generated_code = ".globl main\nmain:\npushl %ebp\nmovl %esp, %ebp\nsubl $"+str(self.__stack_offset)+",%esp\n" + self.__generated_code + "movl $0, %eax\nleave\nret\n"
	def generate_x86_code(self, ast):
		myIRList = []
		if isinstance(ast, Module):
			# Nothing to do. Just go to the next node.
			myIRList += self.generate_x86_code(ast.node)
			return myIRList
		elif isinstance(ast, Function):
			myIRList = []
			#preamble
			myIRList.append(x86.FunctionLabel(ast.name.name))
			myIRList.append(x86.Pushl(x86.Register('ebp')))
			myIRList.append(x86.Movl(x86.Register('esp'),x86.Register('ebp')))
			
			#allocate spillage stack-space
			localList = set(getLocals(ast))
			myIRList.append(x86.Subl(x86.ConstNode(len(localList)*4),x86.Register('esp')))
			
			#push callee-save registers
			for register in self._calleeSaveRegisters:
				myIRList.append(x86.Pushl(register))
			
			#move parameters to local location
			counter = 8
			for arg in ast.argnames:
				myIRList.append(x86.Movl(x86.MemLoc(counter), self._update_dict_vars(arg)))	
				counter += 4
			#recurse for body
			myIRList += self.generate_x86_code(ast.code)
			#cleanup (restoring callee-save registers among other things)
			for register in reversed(self._calleeSaveRegisters):
				myIRList.append(x86.Popl(register))
			myIRList.append(x86.Addl(x86.ConstNode(len(localList)*4),x86.Register('esp')))
			myIRList.append(x86.Leave())
			myIRList.append(x86.Ret())
			return myIRList
		elif isinstance(ast, CallUserDef):
			myIRList = []
			#push arguments
			for arg in reversed(ast.args):
				myIRList += self.generate_x86_code(arg)
				myIRList.append(x86.Pushl(self.getTmpVar()))
			#call function
			myIRList += self.generate_x86_code(ast.node)
			myIRList.append(x86.CallStar(self.getTmpVar()))
			#pop arguments
			myIRList.append(x86.Addl(x86.ConstNode(len(ast.args)*4),x86.Register('esp')))
			myIRList.append(x86.Movl(x86.Register('eax'),self.makeTmpVar()))
			return myIRList		
		elif isinstance(ast, CreateClosure):
			myIRList = []
			myIRList += self.generate_x86_code(ast.env)
			myIRList.append(x86.Pushl(self.getTmpVar()))
			myIRList.append(x86.Pushl(x86.AddressLabel(ast.name.name)))
			myIRList.append(x86.Call('create_closure'))
			myIRList.append(x86.Movl(x86.Register('eax'),self.makeTmpVar()))
			myIRList.append(x86.Addl(x86.ConstNode(8),x86.Register('esp')))
			return myIRList
		elif isinstance(ast, GetFreeVars):
			myIRList = []
			myIRList += self.generate_x86_code(ast.name)
			myIRList.append(x86.Pushl(self.getTmpVar()))
			myIRList.append(x86.Call('get_free_vars'))
			myIRList.append(x86.Movl(x86.Register('eax'), self.makeTmpVar()))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, GetFunPtr):
			myIRList = []
			myIRList += self.generate_x86_code(ast.name)
			myIRList.append(x86.Pushl(self.getTmpVar()))
			myIRList.append(x86.Call('get_fun_ptr'))
			myIRList.append(x86.Movl(x86.Register('eax'), self.makeTmpVar()))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Return):
			ir_list = self.generate_x86_code(ast.value)
			return ir_list + [x86.Movl(self.getTmpVar(),x86.Register('eax'))]
		elif isinstance(ast, Stmt):
			for node in ast.nodes:
				myIRList += self.generate_x86_code(node)
			return myIRList
		elif isinstance(ast, Discard):
			# Nothing to do. Just go to the next node.
			myIRList += self.generate_x86_code(ast.expr)
			return myIRList
		elif isinstance(ast, If):
			x86Test = self.generate_x86_code(ast.tests[0][0])
			resultTmpVar = self.getTmpVar()
			x86Then = self.generate_x86_code(ast.tests[0][1])
			x86Else = self.generate_x86_code(ast.else_)
			compareInstruct = [x86.Pushl(resultTmpVar), x86.Call('is_true'), x86.Cmpl(x86.ConstNode(1),x86.Register('eax'))]
			myIRList.append(x86.Ifx86(x86Test + compareInstruct,[x86.Addl(x86.ConstNode(4), x86.Register('esp'))]+x86Then,x86Else))
			return myIRList
		elif isinstance(ast, IsCompare):
			myIRList += self.generate_x86_code(ast.expr)
			expr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.ops[0][1])
			expr2 = self.getTmpVar()
			newVar = self.makeTmpVar()
			# ConstNode(5) == True with Bool tag applied ( 1 << 2 + 1 = 5)
			# ConstNode(1) == False with Bool tag applied ( 0 << 2 + 1 = 1)
			myIRList.append(x86.Ifx86([x86.Cmpl(expr,expr2)], [x86.Movl(x86.ConstNode(1), newVar)], [x86.Movl(x86.ConstNode(0), newVar)])) 
			return myIRList
		
		elif isinstance(ast, BigCompare):
			myIRList += self.generate_x86_code(ast.expr) # The LHS of the compare
			lhs_expr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.ops[0][1]) # The RHS of the compare
			rhs_expr = self.getTmpVar()
			myIRList.append(x86.Pushl(lhs_expr))
			myIRList.append(x86.Pushl(rhs_expr))
			if ast.ops[0][0] == '==':
				myIRList.append(x86.Call('equal'))
			elif ast.ops[0][0] == '!=':
				myIRList.append(x86.Call('not_equal'))
			newVar = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'),newVar))
			return myIRList
		
		elif isinstance(ast, IntegerCompare):
			myIRList += self.generate_x86_code(ast.expr) # The LHS of the compare
			lhs_expr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.ops[0][1]) # The RHS of the compare
			rhs_expr = self.getTmpVar()
			newVar = self.makeTmpVar()
			if ast.ops[0][0] == '==':
				myIRList.append(x86.Ifx86([x86.Cmpl(lhs_expr,rhs_expr)], [x86.Movl(x86.ConstNode(1), newVar)], [x86.Movl(x86.ConstNode(0), newVar)])) 
			elif ast.ops[0][0] == '!=':
				myIRList.append(x86.Ifx86([x86.Cmpl(lhs_expr,rhs_expr)], [x86.Movl(x86.ConstNode(0), newVar)], [x86.Movl(x86.ConstNode(1), newVar)])) 
			return myIRList

		elif isinstance(ast, Or):
			myIRList += self.generate_x86_code(ast.nodes[0])
			lExpr = self.getTmpVar()
			myIRList.append(x86.Pushl(lExpr))
			myIRList.append(x86.Call('is_true'))
			myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(1),x86.Register('eax'))],[x86.Movl(lExpr, self.makeTmpVar())],self.generate_x86_code(ast.nodes[1]) + [x86.Movl(self.getTmpVar(), self.makeTmpVar())]))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
			##
			#myIRList += self.generate_x86_code(ast.nodes[1])
			#rExpr = self.getTmpVar()
			#resultVar = self.makeTmpVar()
			#myIRList.append(x86.Pushl(lExpr))
			#myIRList.append(x86.Call('is_true'))
			#myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(1),x86.Register('eax'))], [x86.Movl(lExpr, resultVar)], [x86.Movl(rExpr, resultVar)]))
			#myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			#return myIRList
		elif isinstance(ast, And):
			myIRList += self.generate_x86_code(ast.nodes[0])
			lExpr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.nodes[1])
			rExpr = self.getTmpVar()
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Pushl(lExpr))
			myIRList.append(x86.Call('is_true'))
			myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(0),x86.Register('eax'))], [x86.Movl(lExpr, resultVar)], [x86.Movl(rExpr, resultVar)]))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, ProjectTo):
			myIRList += self.generate_x86_code(ast.arg)
			argExpr = self.getTmpVar()
			myIRList.append(x86.Pushl(argExpr))
			myIRList += self.generate_x86_code(ast.typ)
			typExpr = self.getTmpVar()	
			resultVar = self.makeTmpVar()
			if (isinstance(typExpr,Const) and typExpr.value == 0):
				myIRList.append(x86.Call('project_int'))
			elif (isinstance(typExpr,Const) and typExpr.value == 1):
				myIRList.append(x86.Call('project_bool'))
			elif (isinstance(typExpr,Const) and (typExpr.value == 3 or typExpr.value == 2)):
				myIRList.append(x86.Call('project_big'))
			else:
				myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(0),typExpr)], [x86.Call('project_int')], \
								[x86.Ifx86([x86.Cmpl(x86.ConstNode(1),typExpr)], [x86.Call('project_bool')], \
								[x86.Ifx86([x86.Cmpl(x86.ConstNode(2),typExpr)], [x86.Call('project_big')], \
								[x86.Ifx86([x86.Cmpl(x86.ConstNode(3),typExpr)], [x86.Call('project_big')], \
								[])])])]))
			myIRList.append(x86.Movl(x86.Register('eax'),resultVar))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, InjectFrom):
			myIRList += self.generate_x86_code(ast.arg)
			argExpr = self.getTmpVar()
			myIRList.append(x86.Pushl(argExpr))
			myIRList += self.generate_x86_code(ast.typ)
			typExpr = self.getTmpVar()
			resultVar = self.makeTmpVar()
			if (isinstance(typExpr,Const) and typExpr.value == 0):
				myIRList.append(x86.Call('inject_int'))
			elif (isinstance(typExpr,Const) and typExpr.value == 1):
				myIRList.append(x86.Call('inject_bool'))
			elif (isinstance(typExpr,Const) and (typExpr.value == 3 or typExpr.value == 2)):
				myIRList.append(x86.Call('inject_big'))
			else:
				myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(0),typExpr)], [x86.Call('inject_int')], \
						[x86.Ifx86([x86.Cmpl(x86.ConstNode(1),typExpr)], [x86.Call('inject_bool')], \
						[x86.Ifx86([x86.Cmpl(x86.ConstNode(2),typExpr)], [x86.Call('inject_big')], \
						[x86.Ifx86([x86.Cmpl(x86.ConstNode(3),typExpr)], [x86.Call('inject_big')], \
						[])])])]))
			myIRList.append(x86.Movl(x86.Register('eax'),resultVar))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Subscript):
			if ast.flags == 'OP_ASSIGN':
				toStore = self.getTmpVar()
				myIRList.append(x86.Pushl(toStore))
			myIRList += self.generate_x86_code(ast.expr)
			argExpr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.subs[0])
			subExpr = self.getTmpVar()
			resultVar = self.makeTmpVar()

			if ast.flags == 'OP_APPLY':
				# Call get subscript
				myIRList.append(x86.Pushl(subExpr))
				myIRList.append(x86.Pushl(argExpr))
				myIRList.append(x86.Call('get_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(8), x86.Register('esp')))
			elif ast.flags == 'OP_ASSIGN':
				#Call set sub
				#myIRList.append(x86.Pushl(toStore))
				myIRList.append(x86.Pushl(subExpr))
				myIRList.append(x86.Pushl(argExpr))
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(12), x86.Register('esp')))
			myIRList.append(x86.Movl(x86.Register('eax'), resultVar))
			return myIRList
		elif isinstance(ast, List):
			currentElement = 0
			myIRList.append(x86.Pushl(x86.ConstNode(len(ast.nodes) << 2)))
			myIRList.append(x86.Call('create_list'))
			newList = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'),newList))
			myIRList.append(x86.Addl(x86.ConstNode(4),x86.Register('esp')))
			myIRList.append(x86.Pushl(newList))
			myIRList.append(x86.Call('inject_big'))
			myIRList.append(x86.Movl(x86.Register('eax'),newList))
			myIRList.append(x86.Addl(x86.ConstNode(4),x86.Register('esp')))
			for element in ast.nodes:
				myIRList += self.generate_x86_code(element)
				myIRList.append(x86.Pushl(self.getTmpVar()))
				myIRList.append(x86.Pushl(x86.ConstNode(currentElement << 2)))
				myIRList.append(x86.Pushl(newList))
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(12),x86.Register('esp')))
				currentElement += 1
			newNewList = self.makeTmpVar()
			myIRList.append(x86.Pushl(newList))
			myIRList.append(x86.Call('project_big'))
			myIRList.append(x86.Movl(x86.Register('eax'),newNewList))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Dict):
			myIRList.append(x86.Call('create_dict'))
			newPtrDict = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'), newPtrDict))
			myIRList.append(x86.Pushl(newPtrDict))
			myIRList.append(x86.Call('inject_big'))
			newDictPyobj = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'), newDictPyobj))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			for element in ast.items:
				myIRList += self.generate_x86_code(element[1])
				valTmp = self.getTmpVar()
				myIRList += self.generate_x86_code(element[0])
				keyTmp = self.getTmpVar()
				myIRList.append(x86.Pushl(valTmp))
				myIRList.append(x86.Pushl(keyTmp))
				myIRList.append(x86.Pushl(newDictPyobj))
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(12), x86.Register('esp')))
			newNewList = self.makeTmpVar()
			myIRList.append(x86.Pushl(newDictPyobj))
			myIRList.append(x86.Call('project_big'))
			myIRList.append(x86.Movl(x86.Register('eax'),newNewList))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, GetTag):
			myIRList += self.generate_x86_code(ast.arg)
			argExpr = self.getTmpVar()
			myIRList.append(x86.Pushl(argExpr))
			myIRList.append(x86.Call('tag'))
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'),resultVar))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Const):
			# put constant in general register eax for later assignment (in our flattener, constants are always the RHS of an assignment
			# self.__generated_code += "movl $" + str(ast.value) + ", %eax\n"
			myIRList.append(x86.Movl(x86.ConstNode(ast.value),self.makeTmpVar())) 
			return myIRList
		elif isinstance(ast, UnarySub):
			# negate value and leave in %eax
			myIRList += self.generate_x86_code(ast.expr)
			myIRList.append(x86.Negl(self.getTmpVar()))
			return myIRList
		elif isinstance(ast, CallFunc):
			# CallFunc always refers to an input() (in P0, at least).
			myIRList.append(x86.Call(ast.node.name))
			myIRList.append(x86.Movl(x86.Register('eax'),self.makeTmpVar()))
			return myIRList
		elif isinstance(ast, Printnl):
			#process children
			myIRList += self.generate_x86_code(ast.nodes[0])
			
			# get value stored in %eax and push for call to print
			myIRList.append(x86.Pushl(self.getTmpVar()))
			myIRList.append(x86.Call("print_any"))
			myIRList.append(x86.Addl(x86.ConstNode(4),x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Assign):
			# Get the name of the variable being assigned to (l value)
			if isinstance(ast.nodes[0], AssName):
				var_name = ast.nodes[0].name
			
				#emit our expression (RHS)
				myIRList += self.generate_x86_code(ast.expr)
					
				#now, the result of that should be stored in %eax, so do the assignment
				var_LHSnode = self._update_dict_vars(var_name)
				#self.__generated_code += "movl %eax, -"+str(var_offset)+"(%ebp)\n"
				myIRList.append(x86.Movl(self.getTmpVar(), var_LHSnode))
			elif isinstance(ast.nodes[0], Subscript):
				#generate code for our RHS and get temp var
				myIRList += self.generate_x86_code(ast.expr)
				myTmpVar = self.getTmpVar()
	
				#generate code for our subscript and get temp var
				myIRList += self.generate_x86_code(ast.nodes[0].subs[0])
				mySubs = self.getTmpVar()
				
				#generate code for our element and get temp var
				myIRList += self.generate_x86_code(ast.nodes[0].expr)
				myExpr = self.getTmpVar()
				#push RHS, subscript, element
				myIRList.append(x86.Pushl(myTmpVar))
				myIRList.append(x86.Pushl(mySubs))
				myIRList.append(x86.Pushl(myExpr))
				#call set_subscript
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(12),x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Name):
			if(ast.name == 'True'):
				myIRList.append(x86.Movl(x86.ConstNode(1), self.makeTmpVar()))	
			elif(ast.name == 'False'):
				myIRList.append(x86.Movl(x86.ConstNode(0), self.makeTmpVar()))
			else:
				# retrieve var from stack and place into %eax
				# NOTE: this will need to handle function names soon, so this will break in that case! ~ symbol table :S
				myIRList.append(x86.Movl(self._update_dict_vars(ast.name),self.makeTmpVar()))
			return myIRList
		
		elif isinstance(ast, p1ast.IntegerAdd):
			lExpr_list = self.generate_x86_code(ast.left)
			lExpr_var = self.getTmpVar()
			rExpr_list = self.generate_x86_code(ast.right)
			rExpr_var = self.getTmpVar()
			
			myIRList += lExpr_list + rExpr_list
			myIRList.append(x86.Addl(lExpr_var, rExpr_var))
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Movl(rExpr_var, resultVar))
			return myIRList
		
		elif isinstance(ast, p1ast.BigAdd):
			lExpr_list = self.generate_x86_code(ast.left)
			lExpr_var = self.getTmpVar()
			rExpr_list = self.generate_x86_code(ast.right)
			rExpr_var = self.getTmpVar()
			
			myIRList += lExpr_list + rExpr_list
			myIRList.append(x86.Pushl(rExpr_var))
			myIRList.append(x86.Pushl(lExpr_var))
			myIRList.append(x86.Call('add'))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			big_result_pyobj = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'), big_result_pyobj))
			return myIRList
		else:
			print ast
			raise Exception("Error: Unrecognized node/object type %s:" % ast.__class__.__name__)
	def __init__(self):
		pass	

	# Debug Functions: #############################################################################
	def prettyPrint(self, ir_to_print, indents=0):
		for instruction in ir_to_print:
			if isinstance(instruction, x86.Ifx86):
				print "\t" * indents + "If: " + str(instruction.operandList[0])
				self.prettyPrint(instruction.operandList[1], indents+1)
				print "\t" * indents + "Else:"
				self.prettyPrint(instruction.operandList[2], indents+1)
				print "\t" * indents + "EndIf"
			else:
				print "\t" * indents + str(instruction)



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
	print "-"*20 + "x86IR" + "-"*20
	ir_list = []
	for func in flattened:
		ir_list += [Myx86Selector().generate_x86_code(func)]
	for func in ir_list:
		Myx86Selector().prettyPrint(func)

#if __name__ == "__main__":
#	import os
#	if os.path.isfile(sys.argv[1]):
#		explicated_ast = P1Explicate().visit(compiler.parseFile(sys.argv[1]))
#	else:
#		explicated_ast = P1Explicate().visit(compiler.parse(sys.argv[1]))
#	flattened_ast = P1ASTFlattener().visit(explicated_ast)
#	ir_list = Myx86Selector().generate_x86_code(flattened_ast)
#	print "-" * 20 + "Pretty Print" + "-" * 20
#	Myx86Selector().prettyPrint(ir_list)
