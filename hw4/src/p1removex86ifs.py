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
		myNewInstructionList += [x86.Jne(elseLabel)]
		for thenInstruction in ifx86Node.operandList[1]:
			if isinstance(thenInstruction, Ifx86):
				myNewInstructionList += self.removeIfStructure(thenInstruction)
			else:
				myNewInstructionList += [thenInstruction]
		myNewInstructionList += [x86.Label(elseLabel)]
		for elseInstruction in ifx86Node.operandList[2]:
			if isinstance(elseInstruction, Ifx86):
				myNewInstructionList += self.removeIfStructure(elseInstruction)
			else:
				myNewInstructionList += [elseInstruction]
		myNewInstructionList += [x86.Label(endLabel)]
		
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
	from p1explicate import *
	from p1flattener import *
	from Myx86Selector import *
	import sys
	explicated_ast = P1Explicate().visit(compiler.parse(sys.argv[1]))
	flattened_ast = P1ASTFlattener().visit(explicated_ast)
	ir =  Myx86Selector(flattened_ast).getIR()
	print P1Removex86Ifs(ir).removeIfs() 
