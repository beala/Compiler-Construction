#!/usr/bin/python

#Myx86Selector.py
from compiler.ast import *
import compiler
import sys
import string
import x86
import os
from p1explicate import *
from p1flattener import *
import base64

class Myx86Selector:
	#class variables
	__dict_vars = {} #dictionary (associative array) of variable names to memory locations relative to ebp
	__currentTmpVar = 0
	__currentTmpVarPostfix = ""
	_currentLabelNum = 0
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
		new_tmp_name = "__tmpIR" + str(self.__currentTmpVar) + str(self.__currentTmpVarPostfix)
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
			x86Then = self.generate_x86_code(ast.tests[0][1])
			x86Else = self.generate_x86_code(ast.else_)
			myIRList.append(x86.Ifx86(x86Test,x86Then,x86Else))
			return myIRList
		elif isinstance(ast, Compare):
			myIRList += self.generate_x86_code(ast.expr)
			expr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.ops[0][1])
			expr2 = self.getTmpVar()
			#myIRList.append(x86.Cmpl(expr, expr2))
			newVar = self.makeTmpVar()
			#myNewLabel = self._makeLabel()
			#myEndLabel = self._makeLabel()
			#if ast.ops[0] == '==':
			#	myIRList.append(x86.Je(myNewLabel))
			#elif ast.ops[0] == '!=':
			#	myIRList.append(x86.Jne(myNewLabel))
			#myIRList.append(x86.Movl(x86.ConstNode(0), newVar))
			#myIRList.append(x86.Jmp(myEndLabel))
			#myIRList.append(x86.Movl(x86.ConstNode(1), newVar))
			#myIRList.append(x86.Label(myNewLabel))
			
			if ast.ops[0] == '==':
				myIRList.append(x86.Ifx86([x86.Cmpl(expr,expr2)], [x86.Movl(x86.constNode(0), newVar)], [x86.Movl(x86.constNode(1), newVar)])) 
			elif ast.ops[0] == '!=':
				myIRList.append(x86.Ifx86([x86.Cmpl(expr,expr2)], [x86.Movl(x86.ConstNode(1), newVar)], [x86.Movl(x86.ConstNode(0), newVar)])) 			
			return myIRList

		elif isinstance(ast, Or):
			myIRList += self.generate_x86_code(ast.nodes[0])
			lExpr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.nodes[1])
			rExpr = self.getTmpVar()
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Pushl(lExpr))
			myIRList.append(x86.Call('is_true'))
			myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(1),x86.Register('eax'))], [x86.Movl(lExpr, resultVar)], [x86.Movl(rExpr, resultVar)]))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
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
			myIRList += self.generate_x86_code(ast.typ)
			typExpr = self.getTmpVar()	
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Pushl(argExpr))
			if (isinstance(typExpr,Const) and typExpr.value == 0):
				myIRList.append(x86.Call('project_int'))
			elif (isinstance(typExpr,Const) and typExpr.value == 1):
				myIRList.append(x86.Call('project_bool'))
			elif (isinstance(typExpr,Const) and typExpr.value == 3):
				myIRList.append(x86.Call('project_big'))
			else:
				myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(0),typExpr)], [x86.Call('project_int')], \
								[x86.Ifx86([x86.Cmpl(x86.ConstNode(1),typExpr)], [x86.Call('project_bool')], \
								[x86.Ifx86([x86.Cmpl(x86.ConstNode(3),typExpr)], [x86.Call('project_big')], \
								[])])]))
			myIRList.append(x86.Movl(x86.Register('eax'),resultVar))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, InjectFrom):
			myIRList += self.generate_x86_code(ast.arg)
			argExpr = self.getTmpVar()
			myIRList += self.generate_x86_code(ast.typ)
			typExpr = self.getTmpVar()
			resultVar = self.makeTmpVar()
			myIRList.append(x86.Pushl(argExpr))
			if (isinstance(typExpr,Const) and typExpr.value == 0):
				myIRList.append(x86.Call('inject_int'))
			elif (isinstance(typExpr,Const) and typExpr.value == 1):
				myIRList.append(x86.Call('inject_bool'))
			elif (isinstance(typExpr,Const) and typExpr.value == 3):
				myIRList.append(x86.Call('inject_big'))
			else:
				myIRList.append(x86.Ifx86([x86.Cmpl(x86.ConstNode(0),typExpr)], [x86.Call('inject_int')], \
						[x86.Ifx86([x86.Cmpl(x86.ConstNode(1),typExpr)], [x86.Call('inject_bool')], \
						[x86.Ifx86([x86.Cmpl(x86.ConstNode(3),typExpr)], [x86.Call('inject_big')], \
						[])])]))
			myIRList.append(x86.Movl(x86.Register('eax'),resultVar))
			myIRList.append(x86.Addl(x86.ConstNode(4), x86.Register('esp')))
			return myIRList
		elif isinstance(ast, Subscript):
			if ast.flags == 'OP_ASSIGN':
				toStore = self.getTmpVar()

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
				myIRList.append(x87.Addl(x86.ConstNode(8), x86.Register('esp')))
			elif ast.flags == 'OP_ASSIGN':
				#Call set sub
				myIRList.append(x86.Pushl(toStore))
				myIRList.append(x86.Pushl(subExpr))
				myIRList.append(x86.Pushl(argExpr))
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x87.Addl(x86.ConstNode(12), x86.Register('esp')))
			myIRList.append(x86.Movl(x86.Register('eax'), resultVar))
			return myIRList
		elif isinstance(ast, List):
			currentElement = 0
			myIRList.append(x86.Pushl(x86.ConstNode(len(ast.nodes) << 2)))
			myIRList.append(x86.Call('create_list'))
			newList = self.makeTmpVar()
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
			myIRList.append(x86.Movl(newList,newNewList))
			return myIRList
		elif isinstance(ast, Dict):
			myIRList.append(x86.Call('create_dict'))
			newDict = self.makeTmpVar()
			myIRList.append(x86.Movl(x86.Register('eax'), newDict))
			for element in ast.items:
				myIRList += self.generate_x86_code(element[0])
				keyTmp = self.getTmpVar()
				myIRList += self.generate_x86_code(element[1])
				valTmp = self.getTmpVar()
				myIRList.append(x86.Pushl(valTmp))
				myIRList.append(x86.Pushl(keyTmp))
				myIRList.append(x86.Pushl(newDict))
				myIRList.append(x86.Call('set_subscript'))
				myIRList.append(x86.Addl(x86.ConstNode(12), x86.Register('esp')))
			newNewList = self.makeTmpVar()
			myIRList.append(x86.Movl(newDict, newNewList))
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
		elif isinstance(ast, Add):
			#process LHS, move to %edx
			myIRList += self.generate_x86_code(ast.left)
			expr1 = self.getTmpVar()
			expr2 = self.makeTmpVar()
			myIRList.append(x86.Movl(expr1,expr2))
			#process RHS
			myIRList += self.generate_x86_code(ast.right)
			#add
			myIRList.append(x86.Addl(self.getTmpVar(),expr2))
			myIRList.append(x86.Movl(expr2,self.makeTmpVar()))
			return myIRList
		elif isinstance(ast, UnarySub):
			# negate value and leave in %eax
			myIRList += self.generate_x86_code(ast.expr)
			myIRList.append(x86.Negl(self.getTmpVar()))
			return myIRList
		elif isinstance(ast, CallFunc):
			# CallFunc always refers to an input() (in P0, at least).
			myIRList.append(x86.Call('input'))
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
			var_name = ast.nodes[0].name
			
			#emit our expression (RHS)
			myIRList += self.generate_x86_code(ast.expr)
					
			#now, the result of that should be stored in %eax, so do the assignment
			var_LHSnode = self._update_dict_vars(var_name)
			#self.__generated_code += "movl %eax, -"+str(var_offset)+"(%ebp)\n"
			myIRList.append(x86.Movl(self.getTmpVar(), var_LHSnode))
			return myIRList
		elif isinstance(ast, Name):
			# retrieve var from stack and place into %eax
			# NOTE: this will need to handle function names soon, so this will break in that case! ~ symbol table :S
			myIRList.append(x86.Movl(self._update_dict_vars(ast.name),self.makeTmpVar()))
			return myIRList
		else:
			print ast
			raise Exception("Error: Unrecognized node/object type %s:" % ast.__class__.__name__)
	def __init__(self):
		self.__currentTmpVarPostfix = base64.b64encode(os.urandom(5))

if __name__ == "__main__":
	explicated_ast = P1Explicate().visit(compiler.parse(sys.argv[1]))
	flattened_ast = P1ASTFlattener().visit(explicated_ast)
	ir_list = Myx86Selector().generate_x86_code(flattened_ast)
	for element in ir_list:
		print element
