import MyFlattener
import compiler
import sys
print MyFlattener.P0FlattenAST().visit(compiler.parseFile(sys.argv[1]))
