from x86 import *
import random
class P3RemoveStructuredControlFlow:
	__labelNumber = 0
	__myIR = None
	__randPrefix = None
	def __makeLabel(self):
		self.__labelNumber += 1
		return "label"+str(self.__labelNumber) + '_' + str(self.__randPrefix) 
	def removeIfStructure(self,ifx86Node):
		myNewInstructionList = []
		elseLabel = self.__makeLabel()
		endLabel = self.__makeLabel()
		myNewInstructionList += self.removeIfs(ifx86Node.operandList[0])
		#for testInstruction in ifx86Node.operandList[0]:
		#	myNewInstructionList += self.removeIfs(testInstruction)
		myNewInstructionList += [Jne(elseLabel)]
		myNewInstructionList += self.removeIfs(ifx86Node.operandList[1])
		#for thenInstruction in ifx86Node.operandList[1]:
		#	myNewInstructionList += self.removeIfs(thenInstruction)
		myNewInstructionList += [Jmp(endLabel)]
		myNewInstructionList += [Label(elseLabel)]
		myNewInstructionList += self.removeIfs(ifx86Node.operandList[2])
		#for elseInstruction in ifx86Node.operandList[2]:
		#	myNewInstructionList += self.removeIfs(elseInstruction)
		myNewInstructionList += [Label(endLabel)]
		
		return myNewInstructionList #list of flat instructions
	def removeWhileStructure(self, node):
		myNewInstructionList = []
		beginLabel = "W_"+self.__makeLabel()
		endLabel = "W_"+self.__makeLabel()
		myNewInstructionList += [Label(beginLabel)]
		myNewInstructionList += self.removeIfs(node.operandList[0])
		#for testInstruction in node.operandList[0]:
		#	myNewInstructionList += self.removeIfs(testInstruction)
		myNewInstructionList += [Jne(endLabel)]
		myNewInstructionList += self.removeIfs(node.operandList[1])
		#for bodyInstruction in node.operandList[1]:
		#	myNewInstructionList += self.removeIfs(bodyInstruction)
		myNewInstructionList += [Jmp(beginLabel)]
		myNewInstructionList += [Label(endLabel)]
		return myNewInstructionList
	def __init__(self):
		random.seed()
		self.__randPrefix = random.randint(0,9999)
	def removeIfs(self, x86IR):
		myReturnIr = []
		for instruction in x86IR:
			if isinstance(instruction, Ifx86):
				myReturnIr += self.removeIfStructure(instruction)
			elif isinstance(instruction, Whilex86):
				myReturnIr += self.removeWhileStructure(instruction)
			else:
				myReturnIr += [instruction]
		return myReturnIr

if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	from p2closure import *
	from p2flattener import *
	from Myx86Selector import *
	from InterferenceGraph import *
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
	print "-"*20 + "x86IR Colored" + "-"*20
	ir_list = InterferenceGraph(ir_list[0]).allocateRegFunc(ir_list)
	Myx86Selector().prettyPrint(func)
	print "-"*20 + "x86IR Without Ifs" + "-"*20
	no_ifs = P1Removex86Ifs(ir_list).removeIfs()
	print InterferenceGraph(no_ifs).emitColoredIR()

#if __name__ == "__main__":
#	from p1explicate import *
#	from p1flattener import *
#	from Myx86Selector import *
#	import sys
#	import InterferenceGraph
#	explicated_ast = P1Explicate().visit(compiler.parse(sys.argv[1]))
#	flattened_ast = P1ASTFlattener().visit(explicated_ast)
#	ir =  Myx86Selector().generate_x86_code(flattened_ast)
#	graph = InterferenceGraph.InterferenceGraph(ir)
#	graph.allocateRegisters()
#	color_ir = graph.getIR()
#	removedthingsir = P1Removex86Ifs(color_ir).removeIfs() 
#	graph.setIR(removedthingsir)
#	print graph.emitColoredIR()

