
from langcompiler.syntaxtree import (
    AST,
    Assignment,
    BinaryOp,
    Boolean,
    Integer,
    UnaryOp,
    Variable,
    Block,
    If,
    While,
    For,
    Function,
    Return,
    Call,
    List, Class, Property,

)
from lexer import Token, Lexer
from typing import Sequence

"""
BNF Representation / Formal Grammar
| - or
* - 0 or more (optional)
+ - 1 or more (required)
Terminals are represented by CAPITALS.

program := line* EOF
block := LBRACE line* RBRACE
line := (assignment
      | if_st
      | while_st
      | for_st
      | expr
      | NEWLINE
      | return_st
      | function
      )+
function := DEF identifier LPAREN params? RPAREN block
params := identifier (COMMA identifier)*
args := expr (COMMA expr)*

assignment := identifier identifier EQUALS expr
for_st := FOR variable IN expr TO expr block
while_st := WHILE expr block
if_st := IF expr block elif_st* else_st?
elif_st := ELIF expr block
else_st := ELSE block

identifier := a-zA-Z+
compares := "==" | "!=" | ">=" | "<="

expr := compare
compare := (term compares term) | term
term := factor ((PLUS | MINUS) factor)*
factor := unary ((MULTIPLY | DIVIDE) unary)*
unary := ((PLUS | MINUS) unary) | atom
atom := (number | group | variable | boolean) trailer*
return := RETURN expr?
boolean := TRUE | FALSE
group := LPAREN expr RPAREN
number := NUMBER
variable := identifier

trailer := LPAREN args RPAREN
"""


class Parser:
    def __init__(self, tokens: Sequence[str]):
        self.tokens = tokens
        self.pos = 0
        self.tree = AST()
        self.line_num = 0

    @property
    def cur_type(self):
        return self.cur_token.token_type

    @property
    def cur_value(self):
        return self.cur_token.value

    @property
    def cur_token(self):
        return self.tokens[self.pos]

    def peek(self, n=1):
        if self.pos + n >= len(self.tokens):
            return None
        return self.tokens[self.pos + n].token_type

    def advance(self):
        self.pos += 1

    def program(self):
        final = []
        while self.cur_type != Token.EOF:
            line = self.line()

            final.append(line)

            # if self.peek() != None:
            #   self.advance()
        return final

    def block(self):
        """
        block: LBRACE line* RBRACE
        """
        children = []
        self.consume(Token.LBRACE)

        # and self.cur_type != Token.EOF
        while self.cur_type != Token.RBRACE:
            temp = self.line()
            if temp != None:
                children.append(temp)
        self.consume(Token.RBRACE)
        return Block(children)

    def line(self):
        if self.cur_type == Token.EQUALS:
            raise Exception("Unexpected: =")
            return
        elif self.cur_type ==Token.CLASS:
            return self.class_st()
        elif self.cur_type == Token.IDENTIFIER and self.peek()==Token.IDENTIFIER and self.peek(2)==Token.LPAREN:
            return self.define_st()
        elif self.cur_type == Token.IDENTIFIER and self.peek()==Token.IDENTIFIER and self.peek(2)==Token.EQUALS:
            return self.assignment_w_type()
        elif self.cur_type == Token.IDENTIFIER and self.peek()==Token.EQUALS:
            return self.assignment_wo_type()
        elif self.cur_type == Token.FOR:
            return self.for_st()
        elif self.cur_type == Token.IF:
            return self.if_st()
        elif self.cur_type == Token.WHILE:
            return self.while_st()
        elif self.cur_type == Token.NEWLINE:
            self.advance()
        elif self.cur_type == Token.RETURN:
            return self.return_st()
        else:
            return self.expr()

    def return_st(self):
        self.consume(Token.RETURN)
        if self.cur_type!=Token.NEWLINE:
            data = self.expr()
            return Return(data)
        return Return()

    def class_st(self):
        self.consume(Token.CLASS)
        name = self.cur_value
        self.consume(Token.IDENTIFIER)
        block = self.block()
        return Class(name,block)
    def define_st(self):
        ftype = self.cur_value
        self.consume(Token.IDENTIFIER)
        identifier = self.cur_value
        self.consume(Token.IDENTIFIER)
        self.consume(Token.LPAREN)
        params = []
        if self.cur_type == Token.IDENTIFIER:
            params = self.parameters()
        self.consume(Token.RPAREN)
        block = self.block()
        return Function(identifier, params, block,ftype=ftype)

    def arguments(self):
        f = [self.expr()]
        while self.cur_type == Token.COMMA:
            self.consume(Token.COMMA)
            f.append(self.expr())
        return f

    def parameters(self):
        f = []
        vtype = self.cur_value
        self.consume(Token.IDENTIFIER)
        nname = self.cur_value
        self.consume(Token.IDENTIFIER)
        v = Variable(nname)
        v.vtype = vtype
        f.append(v)
        while self.cur_type == Token.COMMA:
            self.consume(Token.COMMA)
            vtype= self.cur_value
            self.consume(Token.IDENTIFIER)
            nname = self.cur_value
            self.consume(Token.IDENTIFIER)
            v = Variable(nname)
            v.vtype = vtype
            f.append(v)
        return f

    def for_st(self):
        self.consume("FOR")
        identifier = self.cur_token
        self.consume(Token.IDENTIFIER)
        self.consume(Token.IN)
        start = self.expr()
        self.consume(Token.TO)
        end = self.expr()
        return For(identifier, start, end, self.block())

    def while_st(self):
        self.consume("WHILE")
        condition = self.expr()
        block = self.block()
        return While(condition, block)
    def assignment_w_type(self):
        vtype = self.cur_value
        self.consume(Token.IDENTIFIER)
        identifier = self.cur_value
        self.consume(Token.IDENTIFIER)
        self.consume(Token.EQUALS)
        value = self.expr()
        return Assignment(left=Variable(identifier), right=value,vtype=vtype)
    def assignment_wo_type(self):
        identifier = self.cur_value
        self.consume(Token.IDENTIFIER)
        self.consume(Token.EQUALS)
        value = self.expr()
        return Assignment(left=Variable(identifier), right=value)
    # def for_st(self):
    #   self.consume("FOR")
    #   return

    def if_st(self):
        self.consume("IF")
        condition = self.expr()
        t_block = self.block()
        f_block = Block()
        if self.cur_type == Token.ELIF:
            f_block = Block([self.elif_st()])
        elif self.cur_type == Token.ELSE:
            self.consume("ELSE")
            f_block = self.block()

        return If(condition, t_block, f_block)

    def elif_st(self):
        self.consume("ELIF")
        condition = self.expr()
        t_block = self.block()
        f_block = Block()
        if self.cur_type == Token.ELIF:
            f_block = Block([self.elif_st()])
        elif self.cur_type == Token.ELSE:
            self.consume("ELSE")
            f_block = self.block()
        return If(condition, t_block, f_block)

    def group(self):
        """
        group: LPAREN bexpr RPAREN
        """
        self.consume("LPAREN")
        node = self.expr()
        self.consume("RPAREN")
        return node


    def expr(self):
        if self.cur_type=="LBRACKET":
            node =  self.list()
        else:
            node = self.compare()
        return node
    def list(self):
        self.consume("LBRACKET")
        if self.cur_type=="RBRACKET":
            self.consume("RBRACKET")
            return List(data=[])
        data = [self.expr()]
        while self.cur_type == Token.COMMA:
            self.consume(Token.COMMA)
            data.append(self.expr())
        self.consume("RBRACKET")
        return List(data=data)
    def method_call(self,node):
        self.consume(Token.PERIOD)
        func = Variable(self.cur_value)
        self.consume(Token.IDENTIFIER)
        if self.cur_type==Token.LPAREN:
            self.consume(Token.LPAREN)
            args = [] if self.cur_type == Token.RPAREN else self.arguments()
            node = Call(args, func,node)
            self.consume(Token.RPAREN)
            return node
        else:
            node = Property(node,func)
            return node

    def atom(self):
        """
        atom: number | group
        """
        node = None
        if self.cur_type == Token.NUMBER:
            node = self.number()
        if self.cur_type == Token.LPAREN:
            node = self.group()
        if self.cur_type == Token.IDENTIFIER:
            node = self.variable()
        if self.cur_type == Token.BOOLEAN:
            node = self.boolean()
        while self.cur_type in (Token.LPAREN,Token.PERIOD):
            if self.cur_type == Token.LPAREN:
                node = self.trailer(node)
            else:
                node = self.method_call(node)
        if node==None:
            raise Exception(f"Unexpected: {self.cur_value} on line {self.cur_token.line}")
        return node

    def term(self):
        """
        term: factor ((PLUS | MINUS) factor)*
        """
        node = self.factor()
        while self.cur_type in ['PLUS', 'MINUS']:
            op = self.cur_type
            self.consume(['PLUS', 'MINUS'])
            node = BinaryOp(op=op, left=node, right=self.factor())
        return node

    def factor(self):
        """
        factor: unary (MULTIPLY | DIVIDE) factor*
        """
        node = self.unary()
        while self.cur_type in ['MULTIPLY', 'DIVIDE']:
            op = self.cur_type
            self.consume(['MULTIPLY', 'DIVIDE'])
            node = BinaryOp(op=op, left=node, right=self.unary())
        return node

    def unary(self):
        """
        unary: ((PLUS | MINUS) unary) | number
        """
        if self.cur_type in ['PLUS', 'MINUS']:
            op = self.cur_value
            self.consume(['PLUS', 'MINUS'])
            return UnaryOp(op=op, expr=self.unary())
        return self.atom()

    def trailer(self, callee):
        if self.cur_type == Token.LPAREN:
            self.consume(Token.LPAREN)
            args = [] if self.cur_type == Token.RPAREN else self.arguments()
            node = Call(args, callee)
            self.consume(Token.RPAREN)
            return node

    def compare(self):
        node = self.term()
        while self.cur_type == "COMPARE":
            op = self.cur_value
            self.consume("COMPARE")
            node = BinaryOp(op=op, left=node, right=self.term())
        return node

    def consume(self, token_type):
        if type(token_type) == list and self.cur_type in token_type:
            self.advance()
            return False
        elif type(token_type) == list:
            raise Exception(f"Expected one of {token_type}. Received: {self.cur_token}")
        if self.cur_type != token_type:
            raise Exception(f"Expected {token_type}. Received: {self.cur_token}")
        self.advance()
        return True

    def variable(self):
        node = Variable(self.cur_value)
        self.consume(Token.IDENTIFIER)
        return node

    def number(self):
        node = Integer(self.cur_value)
        self.consume(Token.NUMBER)
        return node

    def boolean(self):
        node = Boolean(self.cur_value)
        self.consume(Token.BOOLEAN)
        return node

    def parse(self):
        # try:
        tree = self.program()
        self.tree.children = tree + self.tree.children
        return self.tree
        # except Exception as e:
        #     print(f"{e}")


    def eat(self, token_type: str):
        pass


"""

while false {
  123
}

i = 0
while i < 5 {
  i = i + 1
  i
}

x = 7
while x * 2 > 10 {
  x = x - 1
  x * 4
}
"""