from p3ast import *

class TailCall(CallFunc):
	 def __repr__(self):
		return "TailCall(" + str(self.node) + " ," + str(self.args) + ")"
