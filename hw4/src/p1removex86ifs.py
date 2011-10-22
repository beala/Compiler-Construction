from x86 import *

class P1Removex86Ifs:
	__labelNumber = 0
	__myIR = None
	def __makeLabel(self):
		self.__labelNumber += 1
		return "label"+str(self.__labelNumber)
	def removeIfStructure(self,ifx86Node):
		myNewInstructionList = []
		elseLabel = self.__makeLabel()
		endLabel = self.__makeLabel()

		for testInstruction in ifx86Node.operandList[0]:
			if isinstance(testInstruction, Ifx86):
				myNewInstructionList += self.removeIfStructure(testInstruction)
			else:
				myNewInstructionList += [testInstruction]
		myNewInstructionList += [Jne(elseLabel)]
		for thenInstruction in ifx86Node.operandList[1]:
			if isinstance(thenInstruction, Ifx86):
				myNewInstructionList += self.removeIfStructure(thenInstruction)
			else:
				myNewInstructionList += [thenInstruction]
		myNewInstructionList += [Jmp(endLabel)]
		myNewInstructionList += [Label(elseLabel)]
		for elseInstruction in ifx86Node.operandList[2]:
			if isinstance(elseInstruction, Ifx86):
				myNewInstructionList += self.removeIfStructure(elseInstruction)
			else:
				myNewInstructionList += [elseInstruction]
		myNewInstructionList += [Label(endLabel)]
		
		return myNewInstructionList #list of flat instructions

	def __init__(self,x86IR):
		self.__myIR = x86IR

	def removeIfs(self):
		myReturnIr = []
		for instruction in self.__myIR:
			if isinstance(instruction, Ifx86):
				myReturnIr += self.removeIfStructure(instruction)
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

