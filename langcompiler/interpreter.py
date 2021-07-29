from langcompiler.syntaxtree import BinaryOp, UnaryOp, Integer, Assignment, Variable, Boolean, If, While, For, Function, Call


class Scope:
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}

    def define(self, variable, data=None):
        found = self.find(variable)
        if found == False:
            self.variables[variable] = data
            return
        found.variables[variable] = data

    def find(self, variable):
        if variable not in self.variables:
            if self.parent == None:
                return False
            return self.parent.find(variable)
        else:
            return self

    def get(self, variable):
        if variable not in self.variables:
            if self.parent == None:
                raise Exception("Variable does not exist.")
            return self.parent.get(variable)
        return self.variables[variable]

    def recycle(self, variable):
        self.variables.pop(variable)

    def __repr__(self):
        return f"Scope<{self.variables}>"


class Interpreter:
    def __init__(self, tree):
        self.tree = tree

    def visit_expr(self, node, scope):
        if type(node) == BinaryOp:
            return self.visit_binary(node, scope)
        return self.visit_unary(node, scope)

    def visit_binary(self, node, scope):
        # 1 + (2 + (3 + 4))
        left = self.visit_expr(node.left, scope)
        right = self.visit_expr(node.right, scope)
        # if we have PLUS, add left and right
        # return node.left + node.right
        if node.op == "PLUS":
            return left + right
        elif node.op == "MINUS":
            return left - right
        elif node.op == "MULTIPLY":
            return left * right
        elif node.op == "DIVIDE":
            return left / right
        elif node.op == "<":
            return left < right
        elif node.op == ">":
            return left > right
        elif node.op == ">=":
            return left >= right
        elif node.op == "<=":
            return left <= right
        elif node.op == "==":
            return left == right

    def visit_unary(self, node, scope):
        if type(node) == Integer:
            return self.visit_number(node, scope)
        if type(node) == Variable:
            return self.visit_identifier(node, scope)
        if type(node) == Boolean:
            return self.visit_boolean(node, scope)
        expr = self.visit_expr(node.expr, scope)
        # Make positive/negative
        n = 1 if node.op == '+' else -1
        return n * expr

    def visit_number(self, node, scope):
        return int(node.value)

    def visit_boolean(self, node, scope):
        return True if node.value == "TRUE" else False

    def visit_identifier(self, node, scope):
        return scope.get(node.value)

    def visit_assignment(self, node, scope):
        scope.define(node.left, self.visit_expr(node.right, scope))

    def visit_function(self, node, scope):
        node.closure = scope
        scope.define(node.name, node)

    def visit_call(self, node, scope):
        callee = self.visit_expr(node.callee)
        if type(callee) == Function:
            # add(x,y) -> add(1,2) --> Scope({x: 1, y: 2})
            # Number of parameters is called function arity
            if len(callee.params) != len(node.args):
                raise Exception(f"Expected {len(callee.params)} parmaeters got {len(node.args)}")
            new_scope = Scope(callee.closure)
            for param, arg in zip(callee.params, node.args):
                new_scope.define(param, self.visit_expr(arg))



        else:
            raise Exception(f"Function expected got {type(callee)}")

    def visit_for(self, node, scope):
        new_scope = Scope(scope)
        var_name = node.variable.value
        start = self.visit_expr(node.start, scope)
        end = self.visit_expr(node.end, scope)
        new_scope.define(var_name, start)
        for i in range(start, end):
            new_scope.define(var_name, i)
            block_scope = Scope(new_scope)
            self.visit_block(node.loop, block_scope)

    def visit_while(self, node, scope):
        while condition := self.visit_expr(node.condition, scope):
            if type(condition) != bool:
                raise Exception(f"Expected boolean, got {type(condition)}")
            self.visit_block(node.loop, Scope(scope))

    def visit_if(self, node, scope):
        condition = self.visit_expr(node.condition, scope)
        if type(condition) != bool:
            raise Exception(f"Expected boolean, got {type(condition)}")
        if condition:
            self.visit_block(node.true, scope)
        else:
            self.visit_block(node.false, scope)

    def visit_block(self, node, scope):
        for child in node.children:
            self.visit_line(child, scope)

    def visit_line(self, node, scope):
        if node != None:
            if type(node) == Assignment:
                self.visit_assignment(node, scope)
            elif type(node) == If:
                self.visit_if(node, scope)
            elif type(node) == For:
                self.visit_for(node, scope)
            elif type(node) == While:
                self.visit_while(node, scope)
            else:
                print(self.visit_expr(node, scope))

    def interpret(self):
        global_scope = Scope(parent=None)
        for node in self.tree.children:
            self.visit_line(node, global_scope)
        print(f'Variables: {global_scope}')