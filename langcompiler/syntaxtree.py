class AST:
    def __init__(self, children=[]):
        self.children = children

    def __repr__(self):
        return f'{self.children}'
    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
    def __eq__(self, other):
        return hash(self)==hash(other)
class Constant:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<Constant: {self.value}>'
    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(hash(getattr(self,arg))))
        s = f"{self.__class__.__name__} {' ,'.join(arr)}"
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
    def __eq__(self, other):
        return hash(self)==hash(other)
class Integer(Constant):
    def __repr__(self):
        return self.value


class Boolean(Constant):
    def __repr__(self):
        return f"<Boolean {self.value}>"


class Variable(Constant):
    def __init__(self,value,scope=None):
        self.scope = scope
        self.value = value
        self.otype = -1
    def __repr__(self):
        return f"<Variable ({self.value})>"


class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<BinaryOp({self.op})({self.left}, {self.right})>'

    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'<Unary: ({self.op}, {self.expr})>'

    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
class Assignment(BinaryOp):
    def __init__(self,left,right,vtype=None):
        self.left = left
        self.right = right
        self.vtype = vtype
    def __repr__(self):
        return f'<Assignment ({self.left}, {self.right}, {self.vtype})>'
class MethodCall:
    def __init__(self,object,function,args):
        self.object = object
        self.function = function
        self.args = args
    def __repr__(self):
        return f"<Method Call {self.object}.{self.function} ({self.args})"
class Class:
    def __init__(self,name,block):
        self.name = name
        self.block = block
    def __repr__(self):
        return f"<Class {self.name} {self.block}>"
class Block(AST):
    def __repr__(self):
        return ', '.join([repr(x) for x in self.children if x != None])
class List:
    def __init__(self,data):
        self.data = data
    def __repr__(self):
        return  f"List <{', '.join([repr(x) for x in self.data])}>"
class If():
    def __init__(self, condition, true, false):
        self.condition = condition
        self.true = true
        self.false = false

    def __repr__(self):
        return f"<If {self.condition} then {self.true} else {self.false}>"

    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
class While():
    def __init__(self, condition, loop):
        self.condition = condition
        self.loop = loop

    def __repr__(self):
        return f"<While {self.condition} do {self.loop}>"

    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")

class For():
    def __init__(self, variable, start, end, loop):
        self.variable = variable
        self.start = start
        self.end = end
        self.loop = loop

    def __repr__(self):
        return f"<For {self.variable} in {self.start} to {self.end} do {self.loop}>"

    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
class Function():
    def __init__(self, name, params, block,ftype, closure=None):
        self.name = name
        self.params = params
        self.block = block
        self.closure = closure
        self.ftype = ftype
    def __repr__(self):
        params = ', '.join(map(repr,self.params))
        return f"Function ({self.ftype}) {self.name} ({params}) {self.block}"
    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")

class Return:
    def __init__(self, data=None):
        self.data = data

    def __repr__(self):
        return f"return {self.data}"
    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        print(hash(f"{self.__class__.__name__} {' ,'.join(arr)}"))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")
class Property:
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"<Property {self.left}.{self.right}>"
class Call():
    def __init__(self, args, callee=None,caller=None):
        self.callee = callee
        self.caller = caller
        self.args = args

    def __repr__(self):
        args = ', '.join(map(repr, self.args))
        return f"<Call ({args}){self.caller}.{self.callee}>"
    def __hash__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return hash(f"{self.__class__.__name__} {' ,'.join(arr)}")