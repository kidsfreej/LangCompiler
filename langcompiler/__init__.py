from  langcompiler.lexer import Lexer
from langcompiler.parser import Parser
from langcompiler.syntaxtree import BinaryOp, UnaryOp, Integer, Assignment, Variable, Boolean, If, While, For, Function, \
    Call, Return, List, Class, Property

class Instruction:
    def __init__(self):
        pass
    def __repr__(self):
        arr = []
        for arg in self.__init__.__code__.co_varnames[1:]:
            arr.append(repr(getattr(self,arg)))
        return f"{self.__class__.__name__} {' ,'.join(arr)}"
class Mov(Instruction):
    def __init__(self,new,og):
        self.new = new
        self.og = og
class Add(Instruction):
    def __init__(self,reg,addend):
        self.reg =reg
        self.addend = addend
class Push(Instruction):
    def __init__(self,to_push):
        self.to_push = to_push
class CallInst(Instruction):
    def __init__(self,function):
        self.function = function
class Sub(Instruction):
    def __init__(self,reg,subtrahend):
        self.reg = reg
        self.subtrahend = subtrahend
class IMul(Instruction):
    def __init__(self,reg,factor):
        self.reg = reg
        self.factor = factor
class Je(Instruction):
    def __init__(self,location):
        self.location = location
class Jne(Je):
    pass
class Jl(Je):
    pass
class Cmp(Instruction):
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
class Jmp(Instruction):
    def __init__(self,loc):
        self.loc = loc
class Label:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"{self.name}:"
class Movzx(Mov):
    pass

class And(Instruction):
    def __init__(self,l,r):
        self.l =l
        self.r =r
class Or(Instruction):
    def __init__(self,l,r):
        self.l =l
        self.r =r
class Cmp(Instruction):
    def __init__(self,l,r):
        self.l = l
        self.r = r
class Lea(Cmp):
    pass

class Sete(Instruction):
    def __init__(self,l):
        self.l = l
class Setne(Sete):
    pass
class Setl(Sete):
    pass
class Setg(Sete):
    pass
class Setge(Sete):
    pass
class Setle(Sete):
    pass
class Scope:
    def __init__(self, parent, flag=False):
        self.parent = parent
        self.variables = {}
        self.flag= flag
        if flag:
            self.local_variable_mem_counter = 4
    def define(self, variable, data=None):
        found = self.find(variable)
        if found == False:
            self.variables[variable] = data
            return
        found.variables[variable] = data

    def find(self, variable):
        next = self
        while variable not in next.variables:

            if next.parent==None:
                raise Exception(f"Undeclared {variable}")
            next = next.parent
        v_keys = list(next.variables.keys())
        return v_keys[v_keys.index(variable)]
    def check_and_retrieve(self,variable):
        next = self
        while variable not in next.variables:

            if next.parent==None:
                return False
            next = next.parent
        v_keys = list(next.variables.keys())
        return v_keys[v_keys.index(variable)]
    def check(self, variable):
        next = self
        while variable not in next.variables:

            if next.parent==None:
                return False
            next = next.parent
        return True

    def recycle(self, variable):
        self.variables.pop(variable)

    def get_local_variable_mem_counter(self):
        next = self
        while not next.flag:
            next = next.parent
        return next.local_variable_mem_counter
    def get_flagged_scope(self):
        next = self
        while not next.flag:
            next = next.parent
        return next
    def __repr__(self):
        return f"Scope<{self.variables}>"
    def __hash__(self):
        return hash(None)
class AsmFunction:
    def __init__(self, name,params=None, scope=None, code=None,ftype=None):
        if code is None:
            code = []
        self.ftype  =ftype
        self.name = name
        self.scope = scope
        self.code = code
        self.params = params
    def __repr__(self):
        return f"<AsmFunction {self.name} {self.scope}>"
    def __hash__(self):
        return hash(hash(type(self))+hash(self.name))
    def __eq__(self, other):
        return hash(self)==hash(other)
class AsmParams:
    def __init__(self,param_pairs):
        self.param_pairs = param_pairs
    def __repr__(self):
        return ', '.join([x[0]+" "+x[1] for x in self.param_pairs])
    def __hash__(self):
        f = ""
        for x in self.param_pairs:
            f+=str(hash((self.param_pairs[0],self.param_pairs[1])))
        return hash(f)
    def __eq__(self, other):
        return hash(self)==hash(other)
class AsmClass:
    def __init__(self, name, scope=None, code=None, variables=None, variable_types=None, functions=None,
                 assignments=None, definitions=None, size=0):
        if definitions is None:
            definitions = []
        if assignments is None:
            assignments = []
        if functions is None:
            functions = []
        if variable_types is None:
            variable_types = {}
        if variables is None:
            variables = {}
        self.name = name
        self.scope = scope
        self.variable_types = variable_types
        self.code = code
        self.variables = variables
        self.functions = functions
        self.definitions = definitions
        self.assignments = assignments
        self.size = size
    def __repr__(self):
        return f"<AsmClass {self.name}>"
    def __hash__(self):
        return hash(hash(type(self))+hash(self.name))
    def __eq__(self, other):
        return hash(self)==hash(other)
class Leave(Instruction):
    pass
class Ret(Instruction):
    pass
beginning = f"""
extern _print
global _mains
section .text
_mains:
"""
class Compiler:
    def __init__(self):
        self.property_function_ids = {}
        self.property_functions_counter = 0

        self.string_labels = {}
        self.classes = set()
        self.stack_local_mem= 4
        self.init_code = []
        self.code = []
        self.local_variables = {}
        self.temp_var_counter = 0

        self.object_index = 4
        self.types = {"function":-4,"null_terminator":-2,"int":0,"bool":1,"void":2,"list":3}
        self.type_sizes = {"int": 4, "bool": 4, "void": 4, "list": 16}
        self.labels = set()
        self.label_counter = 0
    def squash(self,code):
        c = f"sub esp, {self.stack_local_mem}\n"
        return "push esp\nmov ebp,esp\n"+c+code+"leave\nret\n"
    def get_type(self,t,scope):

        if t not in self.types:
            0/0
            print(f"eror: unkown type {t}")
            return None
        return self.types[t]
    def get_type_size(self,t,scope):

        if t not in self.type_sizes:
            print(f"eror: unkown type {t}")
            0/0
            return None
        return self.type_sizes[t]
    def rename_variable(self,v,nv,scope):
        new_v = Variable(nv,v.scope)
        t_p = self.get_type_variable(v,v.scope)
        t_c = self.create_fake_type_variable(new_v,v.scope)
        v.scope.variables[new_v] = v.scope.variables.pop(v)
        v.scope.variables[t_c] = v.scope.variables.pop(t_p)
        v.value = nv
        return new_v
    def create_fake_type_variable(self,ogv,scope):
        return Variable(ogv,scope)
    def class_func_to_name(self,class_name,func_name):
        return f"a{class_name}a{func_name}"
    def assign_parameter_space(self,name,scope,n):
        t_var = Variable(name,scope)
        t_type_var = Variable(t_var,scope)
        scope.variables[t_var] = (1+n)*8
        scope.variables[t_type_var] =  (1+n)*8+4
        return t_var

    def create_type(self,t,size,scope):
        self.types[t] = len(self.types)
        self.type_sizes[t] = size
    def create_named_variable(self,name,scope,code,vtype=None,create_type=True,size=4):
        t_var = Variable(name,scope)
        t_var.vtype = vtype
        flagged_scope = scope.get_flagged_scope()
        scope.variables[t_var] = -flagged_scope.local_variable_mem_counter
        flagged_scope.local_variable_mem_counter+=size
        if create_type:
            type_var = self.create_type_variable(t_var,scope,code)
            if vtype!=None:
                if type(vtype)==Variable:
                    code.append(Mov("eax",vtype))
                    code.append(Mov(type_var,"eax"))
                else:
                    code.append(Mov(type_var, vtype))
        return t_var

    def create_temporary_variable(self,scope,code,vtype=None,size=4):
        t_var  = self.create_named_variable("!"+str(self.temp_var_counter),scope,code,vtype=vtype,size=size)
        self.temp_var_counter+=1
        return t_var
    def create_type_variable(self,ogv,scope,code):
        if ogv==None:
            0/0
        return self.create_named_variable(ogv,scope,code,vtype=None,create_type=False)
    def get_type_variable(self,ogv,scope):
        return scope.find(Variable(ogv))
    def variable_to_relative(self,v,isLea=False):
        if v not in v.scope.variables:
            return ""
        return f"{'DWORD' if not isLea else ''}[ebp{'' if v.scope.variables[v]<0 else '+' }{v.scope.variables[v]}]"
    def check_variable(self,node,scope):

        if not scope.find(node):
            if node.value!="!failed":
                print(f""
                      f"error screw you unfound variable hold on we are refinding it variable: {node.value}")
            return True
        return False
    def create_string_label(self,s):
        l = self.create_label()
        self.string_labels[s] = l
        return l
    def fetch_or_create_string_label(self,s):
        if s not in self.string_labels:
            return self.create_string_label(s)
        return self.string_labels[s]
    def verify_type_two_variables(self,v1t,v2t,scope, code):
        v1 = scope.find(v1t)
        v2 = scope.find(v2t)
        code.append(Mov('eax',self.get_type_variable(v1, scope)))
        code.append(Cmp('eax',self.get_type_variable(v2, scope)))
        l = self.create_label()
        code.append(Je(l))
        code.append(Push(self.get_type_variable(v2, scope)))
        code.append(CallInst("_error"))
        code.append(Add("esp",4))
        code.append(l)
    def verify_type_one_variable(self,vtt,t,scope, code):
        vt = scope.find(self.create_fake_type_variable(vtt,scope))
        code.append(Mov('eax',vt))
        code.append(Cmp('eax',t))
        l = self.create_label()
        code.append(Je(l))
        code.append(Push(vt))
        code.append(CallInst("_error"))
        code.append(Add("esp",4))
        code.append(l)
    def ast_params_to_asm_params(self,node):
        f_param_arr=[]
        params = node.params
        for param in params:
            f_param_arr.append([param.vtype,param.value])
        return AsmParams(f_param_arr)
    def asm_function_to_label(self,node,scope):
        found = scope.find(node)
        return Label("f"+found.name+str(id(found.scope)))
    def create_label(self):
        self.labels.add(Label("b"+str(self.label_counter)))
        self.label_counter+=1
        return Label("b"+str(self.label_counter - 1))


    def visit_property(self, node, scope, code, c_class):
        # fix me


        v = self.visit_expr(node.left,scope,code, c_class)
        self.asm_call("_getHashmapAsm",code,[self.property_function_ids[node.right],scope.find(self.create_fake_type_variable(v,scope))])
        t_var = self.create_temporary_variable(scope,code)
        type_t_var = scope.find(self.create_fake_type_variable(t_var,scope))
        code.append(Mov("ecx","DWORD[eax+8]"))
            # ecx is relative
        code.append(Sub(v,"ecx"))
        code.append(Mov("ecx",v))
        code.append(Mov("ecx","DWORD[ecx]"))
        code.append(Mov(t_var,"ecx"))
        code.append(Mov("ecx", "DWORD[eax+12]"))
        code.append(Mov(type_t_var,"ecx"))

        return t_var

    def visit_return(self,node,scope,code,func, c_class):
        if func==None:
            0/0
            print("Unexpected return")
            return

        if func.ftype!="void":
            if  node.data!=None:
                t_var = self.visit_expr(node.data,scope,code, c_class)
                self.verify_type_one_variable(t_var,self.get_type(func.ftype,scope),scope,code)
                code.append(Mov("eax",t_var))
                code.append(Jmp(Label("leaveret")))
            else:
                print(f"error: return type of {func.ftype}, found null")
        else:
            if node.data != None:
                print("error: expected no return value")
    def visit_assignment(self,node,scope,code, c_class):
        variable = self.visit_expr(node.right, scope, code, c_class)
        left = node.left


        if type(node.left)==Property:
            # If it is a property
            # fix me
            if left ==Variable("left"):
                self.asm_call("_getHashmapAsm", code, [self.property_function_ids[node.left.right],
                                                       scope.find(self.create_fake_type_variable(left, scope))])
            else:
                left = self.visit_expr(node.left.left,scope,code, c_class)
                self.asm_call("_getHashmapAsm",code,[self.property_function_ids[node.left.right],scope.find(self.create_fake_type_variable(left,scope))])


            code.append(Mov("ecx","DWORD[eax+8]"))
                # ecx is relative
            code.append(Sub(left,"ecx"))
            code.append(Mov("ecx",left))
            code.append(Mov("eax",variable))
            code.append(Mov("DWORD[ecx]","eax"))

        else:
            # If class
            if node.vtype !=None:
                self.verify_type_one_variable(variable, self.get_type(node.vtype, scope), scope,code)
                t_var = self.rename_variable(variable, left.value, scope)
                code.append(Mov(scope.find(self.create_fake_type_variable(t_var,scope)), self.get_type(node.vtype,scope)))
            else:
                found = scope.find(node.left)
                self.verify_type_two_variables(variable,found, scope,code)
                code.append(Mov("eax",variable))
                code.append(Mov(found,"eax"))
    def visit_while(self,node,scope,code,func, c_class):
        new_scope = Scope(scope)
        start_l = self.create_label()
        code.append(start_l)
        t_var = self.visit_expr(node.condition,scope,code, c_class)
        self.verify_type_one_variable(t_var,self.get_type("bool",scope),scope,code)
        end_l = self.create_label()
        code.append(Cmp(t_var, 0))
        code.append(Je(end_l))
        self.visit_block(node.loop, new_scope, code,c_class,func)
        code.append(Jmp(start_l))
        code.append(end_l)

    def visit_unary(self,node, scope,code, c_class):
        if node.op == "-":
            t_var = self.visit_expr(node.expr, scope, code, c_class)
            self.verify_type_one_variable(t_var, self.get_type("int", scope), scope,code)
            code.append(Mov("eax", t_var))
            code.append(IMul("eax", -1))
            code.append(Mov(t_var, "eax"))
            return t_var
        if node.op == "+":
            t_var = self.visit_expr(node.expr, scope, code, c_class)
            self.verify_type_one_variable(t_var, self.get_type("int", scope), scope,code)
            return t_var
    def visit_if(self,node,scope,code,func, c_class):
        new_scope = Scope(scope)
        t_var = self.visit_expr(node.condition,scope,code, c_class)
        code.append(Cmp(t_var,0))
        l = self.create_label()
        code.append(Je(l))
        self.visit_block(node.true,new_scope,code,c_class,func)
        code.append(l)
    def visit_binary(self,node, scope,code, c_class):

        if node.op=="AND":
            l = self.visit_expr(node.left, scope, code, c_class)
            r = self.visit_expr(node.right, scope, code, c_class)
            self.verify_type_one_variable(l,self.get_type("bool", scope), scope,code)
            self.verify_type_one_variable(r,self.get_type("bool", scope), scope,code)
            if type(l) == Variable:
                code.append(Mov("eax",r))
                code.append(And(l,"eax"))
            else:
                code.append(And(l,r))
            return l
        if node.op=="OR":
            l = self.visit_expr(node.left, scope, code, c_class)
            r = self.visit_expr(node.right, scope, code, c_class)
            self.verify_type_one_variable(l,self.get_type("bool", scope), scope,code)
            self.verify_type_one_variable(r,self.get_type("bool", scope), scope,code)
            if type(l) == Variable:
                code.append(Mov("eax",r))
                code.append(Or(l,"eax"))
            else:
                code.append(Or(l,r))
            return l
        if node.op in ["==","!=","<",">","<=",">="]:
            set_byte_instruction = None
            if node.op=="==":
                set_byte_instruction = Sete
            elif node.op == "!=":
                set_byte_instruction = Setne
            elif node.op == "<":
                set_byte_instruction = Setl
            elif node.op == ">":
                set_byte_instruction = Setg
            elif node.op == ">=":
                set_byte_instruction = Setge
            elif node.op == "<=":
                set_byte_instruction = Setle

            t_var = self.create_temporary_variable(scope,code,self.get_type("bool",scope))
            l = self.visit_expr(node.left, scope, code, c_class)
            r = self.visit_expr(node.right, scope, code, c_class)
            self.verify_type_two_variables(r,l, scope,code)
            if type(l) == Variable:
                code.append(Mov("eax",r))
                code.append(Cmp(l,"eax"))
            else:
                code.append(Cmp(l,r))
            code.append(set_byte_instruction("al"))
            code.append(Movzx("eax","al"))
            code.append(Mov(t_var,"eax"))
            return t_var
        if node.op=="==":
            t_var = self.create_temporary_variable(scope,code,self.get_type("bool",scope))
            l = self.visit_expr(node.left, scope, code, c_class)
            r = self.visit_expr(node.right, scope, code, c_class)
            self.verify_type_two_variables(r,l, scope,code)
            if type(l) == Variable:
                code.append(Mov("eax",r))
                code.append(Cmp(l,"eax"))
            else:
                code.append(Cmp(l,r))
            code.append(Sete("al"))
            code.append(Movzx("eax","al"))
            code.append(Mov(t_var,"eax"))
            return t_var
        op = Add if node.op == "PLUS" else (Sub if node.op == "MINUS" else IMul)
        r =  self.visit_expr(node.right, scope, code, c_class)
        l =  self.visit_expr(node.left, scope, code, c_class)
        self.verify_type_one_variable(l,self.get_type("int",scope),scope,code)
        self.verify_type_one_variable(r,self.get_type("int",scope),scope,code)
        code.append(Mov("eax",l))
        code.append(op("eax",r))
        code.append(Mov(r,"eax"))
        return r
    def visit_expr(self,node, scope,code, c_class):

        if type(node)==Property:
            return self.visit_property(node,scope,code, c_class)
        if type(node)==Variable:
            if node.value == "this":
                if c_class == None:
                    print("Error: Nice try, but the 'this' keyword is reserved for classes")
                else:
                    return scope.find(Variable("this"))
            if node.value=="null":
                t_var = self.create_temporary_variable(scope, code)
                t_type = self.get_type_variable(t_var, scope)
                code.append(Mov(t_var,0))
                code.append(Mov(t_type,-1))
                return t_var

            nnode = scope.find(node)
            t_var = self.create_temporary_variable(scope,code)
            n_type = self.get_type_variable(nnode,scope)
            t_type = self.get_type_variable(t_var,scope)
            code.append(Mov("eax",n_type))
            code.append(Mov(t_type,"eax"))
            code.append(Mov("eax",nnode))
            code.append(Mov(t_var,"eax"))
            return t_var
        if type(node)==Boolean:
            t_var = self.create_temporary_variable(scope,code,self.get_type("bool",scope))
            code.append(Mov(t_var,1 if node.value=='TRUE' else 0))
            return t_var
        if type(node)==BinaryOp:
            return self.visit_binary(node, scope, code, c_class)
        if type(node)==Call:
            return self.visit_call(node, scope, code, c_class)
        if type(node)==UnaryOp:
            return self.visit_unary(node, scope, code, c_class)
        if type(node)==Integer:
            t_var = self.create_temporary_variable(scope,code, self.get_type("int",scope))
            code.append(Mov(t_var,node.value))
            return t_var
        if type(node)==List:
            return self.visit_list(node,scope,code, c_class)
        print(type(node))
        print(type(node))
        print(type(node))
        print(type(node))
        print(type(node))
        0/0
    def visit_list(self,node,scope,code, c_class):
        t_var = self.create_temporary_variable(scope,code,self.get_type("list",scope),size=16)
        code.append(Lea("eax",t_var))
        code.append(Push("eax"))
        code.append(CallInst("_initList"))
        return t_var
    def visit_class_function_definition(self,asmnode,scope,code,asmclass):
        if asmnode not in self.property_function_ids:
            self.property_function_ids[asmnode] =self.property_functions_counter
            self.property_functions_counter+=1
        self.asm_call("_addHashmapAsm", self.init_code, [self.property_function_ids[asmnode] ,self.get_type(asmclass.name,scope),self.asm_function_to_label(asmnode,scope),-4])

    def visit_property_definition(self,node,scope,code,asmclass):
        if node.left not in self.property_function_ids:
            self.property_function_ids[node.left] =self.property_functions_counter
            self.property_functions_counter+=1
        self.asm_call("_addHashmapAsm", self.init_code, [self.property_function_ids[node.left],self.get_type(asmclass.name,scope),asmclass.variables[node.left],self.get_type(node.vtype,scope)])
        variable = self.visit_expr(node.right,scope,code, asmclass)
        # if declared in constructonator. useless for most things
        self.verify_type_one_variable(variable, self.get_type(node.vtype, scope), scope, code)
        code.append(Mov("eax",variable))
        code.append(Mov("ecx",f"DWORD[ebp+8]"))
        code.append(Mov(f"DWORD[ecx-{asmclass.variables[node.left]}]","eax"))
    def visit_class(self,node,classnode,scope,code, c_class):
        pass
    def visit_define(self, node, asmnode, scope, code, asses=None, asmclass=None):
        if asses is None:
            asses = []
        for ass in asses:
            # this happens when we are in a constructor
            self.visit_property_definition(ass,scope,code,asmclass)
        if asmclass!=None:
            # this happens when we are declaring function in a class
            self.visit_class_function_definition(asmnode,scope,code,asmclass)
        i = 0
        for param in asmnode.params.param_pairs:
            t_var = self.assign_parameter_space(param[1],scope,i)
            self.verify_type_one_variable(t_var,self.get_type(param[0],scope),scope,code)
            i+=1
        code.append(Cmp(f"DWORD[ebp+{12+i*4}]",-2))
        jl = self.create_label()
        code.append(Jne(jl))
        code.append(Push(-2))
        code.append(Call("_error"))
        code.append(jl)
        self.visit_block(node.block,scope,code,asmclass,asmnode)
        code.insert(0, Sub("esp",scope.local_variable_mem_counter-4))
        code.insert(0,Mov("ebp","esp"))
        code.insert(0,Push("ebp"))

        if asmnode.name == "main":
            code.insert(0, Label("_mains"))
        else:
            code.insert(0, self.asm_function_to_label(asmnode,scope))
        code.append(Leave())
        code.append(Ret())
    def visit_block(self,node,scope,code,c_class,func=None):
        for line in node.children:
            a = self.visit_line(line,scope,code,func, c_class)
            if a ==True:
                return a
    def visit_call(self,node, scope,code, c_class):
        asm_class = scope.check_and_retrieve(AsmClass(node.callee.value))
        if node.caller ==None and asm_class !=False:
            # if init function for class
            t_var = self.create_temporary_variable(scope,code,self.get_type(asm_class.name,scope))
            func = asm_class.scope.find(AsmFunction(self.class_func_to_name(asm_class.name,node.callee.value)))
            code.append(Push(asm_class.size))
            code.append(CallInst("_mem_alloc"))
            code.append(Add("esp",4))
            code.append(Mov(t_var,"eax"))
            code.append(Push(self.get_type(asm_class.name,scope)))
            code.append(Push("eax"))

            for i in range(len(node.args) - 1, -1, -1):
                t_var = self.visit_expr(node.args[i], scope, code, c_class)
                code.append(Push(self.get_type_variable(t_var, scope)))
                code.append(Push(t_var))


            code.append(CallInst(self.asm_function_to_label(func,asm_class.scope)))
            code.append(Add("esp",4))
            return t_var
        if node.callee == Variable("print"):
            t_var = self.visit_expr(node.args[0], scope, code, c_class)
            self.verify_type_one_variable(t_var,self.get_type("int",scope), scope,code)
            code+=[Mov("eax",t_var),Push("eax"),CallInst("_print"),Add("esp",4)]

        elif node.callee==Variable("input"):
            t_var = self.create_temporary_variable(scope,code,self.get_type("int",scope))
            code+=[CallInst("_input"),Mov(t_var,"eax")]
            return t_var
        else:
            if node.caller !=None:
                v = self.visit_expr(node.caller, scope, code, c_class)
                self.asm_call("_getHashmapAsm", code, [self.property_function_ids[self.],
                                                       scope.find(self.create_fake_type_variable(v, scope))])
                t_var = self.create_temporary_variable(scope, code)
                type_t_var = scope.find(self.create_fake_type_variable(t_var, scope))
                code.append(Mov("ecx", "DWORD[eax+8]"))
                # ecx is relative
                code.append(Sub(v, "ecx"))
                code.append(Mov("ecx", v))
                code.append(Mov("ecx", "DWORD[ecx]"))
                code.append(Mov(t_var, "ecx"))
                code.append(Mov("ecx", "DWORD[eax+12]"))
                code.append(Mov(type_t_var, "ecx"))
            else:

            # update later. remember to remove verify type variable
                found = scope.find(AsmFunction(node.callee.value))
                if len(found.params.param_pairs)==len(node.args):
                    ret_var = self.create_temporary_variable(scope, code, self.get_type(found.ftype, scope))
                    for i in range(len(found.params.param_pairs)-1,-1,-1):
                        t_var = self.visit_expr(node.args[i],scope,code, c_class)
                        self.verify_type_one_variable(t_var,self.get_type(found.params.param_pairs[i][0],scope),scope,code)
                        code.append(Push(self.get_type_variable(t_var,scope)))
                        code.append(Push(t_var))

                    code.append(CallInst(self.asm_function_to_label(AsmFunction(node.callee.value),scope)))
                    code.append(Add("esp",8*len(node.args)))
                    if found.ftype != "void":
                        code.append(Mov(ret_var,"eax"))
                    return ret_var

                else:
                    print(f"error: expected {len(found.params.param_pairs)} args, found {len(node.args)} for function {found.name}")


    def asm_call(self,name,code,params):
        code+= [Push(param) for param in params[::-1]]
        code.append(Call(name))
        code.append(Add("esp",4*len(params)))
    def visit_line(self,node, scope,code,func, c_class):
        if type(node)==While:
            self.visit_while(node,scope,code,func, c_class)
        if type(node) == Assignment:
            self.visit_assignment(node, scope, code, c_class)
        if type(node)==If:
            self.visit_if(node,scope,code,func, c_class)
        if type(node)==Call:
            self.visit_call(node, scope, code, c_class)
        if type(node)==Return:
            self.visit_return(node,scope,code,func, c_class)

    # def visit_class_assignments(self,asm_class,scope,code):
    def visit_ast_children(self,children,rcode):
        env_scope = Scope(None, True)

        for node in children:
            if type(node)==Function:
                func_scope = Scope(env_scope, True)
                code = []
                asm_func = AsmFunction(node.name,self.ast_params_to_asm_params(node),func_scope,code,node.ftype)
                env_scope.variables[asm_func]=True
            if type(node)==Class:
                class_scope = Scope(env_scope, True)
                code = []
                asm_class = AsmClass(node.name,class_scope,code)
                self.classes.add(node.name)
                env_scope.variables[asm_class]=True
                for line in node.block.children:
                    if type(line) == Function:
                        func_scope = Scope(class_scope, True)
                        func_code = []
                        asm_func = AsmFunction(self.class_func_to_name(node.name,line.name), self.ast_params_to_asm_params(line), func_scope, func_code,line.ftype)
                        class_scope.variables[asm_func] = True
                        asm_class.functions.append(asm_func)
                    if type(line)==Assignment:
                        if line.left not in [x.left for x in asm_class.assignments]:
                            asm_class.assignments.append(line)
                self.create_type(node.name,len(asm_class.assignments)*4,class_scope)
        for node in children:

            if type(node)==Function:
                asm_func = env_scope.find(AsmFunction(node.name))
                self.visit_define(node,asm_func,asm_func.scope,asm_func.code)
                rcode+=asm_func.code
            if type(node) == Class:
                asm_class = env_scope.find(AsmClass(node.name))
                for line in node.block.children:
                    if type(line) == Function:
                        t_this = Variable("this")
                        t_this.scope = asm_class.scope
                        ty_t_this = Variable(Variable("this"))
                        ty_t_this.scope = asm_class.scope

                        asm_class.scope.variables[t_this] = 8
                        asm_class.scope.variables[ty_t_this] = 12
                        asm_func = asm_class.scope.find(AsmFunction(self.class_func_to_name(asm_class.name,line.name)))
                        # is constructor
                        if line.name==asm_class.name:
                            i = 0

                            for ass in asm_class.assignments:

                                asm_class.variable_types[ass.left] = ass.vtype
                                asm_class.variables[ass.left]= i
                                i+=4
                            asm_class.size = i

                            self.visit_define(line,asm_func,asm_class.scope,asm_func.code,asm_class.assignments,asm_class)
                            rcode += asm_func.code
                        else:
                            self.visit_define(line, asm_func, asm_func.scope, asm_func.code,asmclass=asm_class)
                            rcode += asm_func.code


    def compile(self,node):
        env_scope = Scope(None,True)

        self.visit_ast_children(node.children,self.code)
        self.stack_local_mem = env_scope.local_variable_mem_counter-4
    def to_asm(self,fcode):
        f = ""
        self.init_code.insert(0,Label("_inits"))
        self.init_code.append(Call("_mains"))
        self.init_code.append(Leave())
        self.init_code.append(Ret())
        code = self.init_code+fcode
        for line in code:
            true_args = []
            if type(line)==Label:
                f+=repr(line)+"\n"
            else:
                f += (line.__class__.__name__.lower() if line.__class__.__name__.lower()!="callinst" else "call")+" "
                args = [getattr(line,argv) for argv in line.__init__.__code__.co_varnames[1:]]
                for arg in args:
                    if type(arg)==str:
                        true_args.append(arg)
                    elif type(arg)==Variable:
                        if arg.scope ==None:
                            print("line that errors: ",line)

                        true_args.append(self.variable_to_relative(arg,type(line)==Lea))
                    elif type(arg)==int:
                        true_args.append(str(arg))
                    elif type(arg)==Integer:
                        true_args.append(arg.value)
                    elif type(arg)==Label:
                        true_args.append(repr(arg)[:-1])

                f+=', '.join(true_args)+"\n"
        return f
if __name__ == '__main__':
    with open("compileme.lang","r") as f:
        text= f.read()
    lexer = Lexer(text=text)
    lexer.lex()
    print(lexer.tokens)
    parse = Parser(lexer.tokens).parse()
    print(parse)
    c = Compiler()
    c.compile(parse)
    # print("hello")
    # for cc in c.code:
    #     print(cc)
    with open("E:/assemblystuff/asm.asm","w") as f:
        f.write("""

extern _print
global _mains
global _inits
extern _error
extern _input

extern _getHashmapAsm
extern _reprListReal
extern _initList
extern _appendList
extern _freeList
extern _deepfreeList
extern _addHashmapAsm
extern _callFunc
extern _mem_alloc
section .text
leaveret:
leave
ret

\n
"""+c.to_asm(c.code))



