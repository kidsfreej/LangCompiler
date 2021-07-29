from string import ascii_letters, digits


class Token:
    # > < >= <= != ==
    CLASS = "CLASS"
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"
    NEWLINE = "NEWLINE"
    EQUALS = "EQUALS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    BOOLEAN = "BOOLEAN"
    COMPARE = "COMPARE"
    NOT = "NOT"
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    TO = "TO"
    DEF = "DEF"
    RETURN = "RETURN"
    COMMA = "COMMA"
    AND = "AND"
    OR = "OR"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    PERIOD = "PERIOD"
    def __init__(self, type_: str, value: str,line):
        self.token_type = type_
        self.value = value
        self.line = line
    def __repr__(self):
        value = self.value
        if self.token_type == Token.COMPARE:
            value = f"'{value}'"
        return f'<{self.token_type}: {value}>'  # #


class Lexer:
    Operators = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE"
    }

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

        self.line = 1
        self.column = 0
        if len(text) == 0:
            raise ValueError('We interpreted it and the output is ')
        self.tokens = []

    @property
    def cur_char(self):
        return self.text[self.pos]

    @property
    def is_not_eof(self):
        return self.pos < len(self.text)

    def print_tokens(self):
        s = "Tokens:\n"
        for token in self.tokens:
            s += f'{token}\n'
        print(s)

    def advance(self, n=1):
        self.pos += n

    def number(self):
        """Handles reading a number, such as 5."""
        value = ""
        while self.is_not_eof and (self.cur_char.isdigit() or self.cur_char == "."):
            value += self.cur_char
            self.advance()
        self.tokens.append(Token(Token.NUMBER, value,self.line))

    def identifier(self):
        idName = ""
        names = ["for", "in", "to", "while", "else", "if", "elif", "def"]
        while self.is_not_eof and self.cur_char in ascii_letters:
            idName += self.cur_char
            self.advance()

        if idName == "true":
            self.tokens.append(Token(Token.BOOLEAN, Token.TRUE,self.line))
        elif idName == "false":
            self.tokens.append(Token(Token.BOOLEAN, Token.FALSE,self.line))
        elif idName in names:
            self.tokens.append(Token(idName.upper(), idName.upper(),self.line))
        elif idName == "def":
            self.tokens.append(Token(Token.DEF, Token.DEF,self.line))
        elif idName == "return":
            self.tokens.append(Token(Token.RETURN, Token.RETURN,self.line))
        elif idName=="and":
            self.tokens.append(Token(Token.COMPARE,Token.AND,self.line))
        elif idName=="class":
            self.tokens.append(Token(Token.CLASS, Token.CLASS, self.line))
        elif idName == "or":
            self.tokens.append(Token(Token.COMPARE, Token.OR, self.line))
        else:
            self.tokens.append(Token(Token.IDENTIFIER, idName,self.line))

    def peek(self, n=1):
        if self.pos + n >= len(self.text):
            return None
        return self.text[self.pos + n]

    def match(self, data):
        for i in range(len(data)):
            if self.peek(i) != data[i]:
                return False
        return True

    def lex(self):
        while self.is_not_eof:
            char = self.text[self.pos]
            if char.isdigit():
                self.number()
            elif char in ' \t\r\f':
                self.advance()
            elif char == "\n":
                self.tokens.append(Token(Token.NEWLINE, "NEWLINE",self.line))
                self.line+=1
                self.advance()
            elif char == ",":
                self.tokens.append(Token(Token.COMMA, Token.COMMA,self.line))
                self.advance()
            elif char == "{":
                self.tokens.append(Token(Token.LBRACE, "{",self.line))
                self.advance()
            elif char=="[":
                self.tokens.append(Token(Token.LBRACKET,"[",self.line))
                self.advance()
            elif char=="]":
                self.tokens.append(Token(Token.RBRACKET,"]",self.line))
                self.advance()
            elif char == "}":
                self.tokens.append(Token(Token.RBRACE, "}",self.line))
                self.advance()
            elif char == "=":
                if self.match("=="):
                    self.advance(2)
                    self.tokens.append(Token(Token.COMPARE, "==",self.line))
                    continue
                self.tokens.append(Token(Token.EQUALS, "==",self.line))
                self.advance()
            elif char == "<":
                if self.match("<="):
                    self.advance(2)
                    self.tokens.append(Token(Token.COMPARE, "<=",self.line))
                    continue
                self.advance()
                self.tokens.append(Token(Token.COMPARE, "<",self.line))
            elif char == ">":
                if self.match(">="):
                    self.advance(2)
                    self.tokens.append(Token(Token.COMPARE, ">=",self.line))
                    continue
                self.advance()
                self.tokens.append(Token(Token.COMPARE, ">",self.line))
            elif char == "!":
                if self.match("!="):
                    self.advance(2)
                    self.tokens.append(Token(Token.COMPARE, "!=",self.line))
                    continue
                self.advance()
                self.tokens.append(Token(Token.NOT, "!",self.line))
                continue
            elif char in ascii_letters:
                self.identifier()
            elif char == "(":
                self.tokens.append(Token(Token.LPAREN, "(",self.line))
                self.advance()
            elif char == ")":
                self.tokens.append(Token(Token.RPAREN, ")",self.line))
                self.advance()
            elif char=='.':
                self.tokens.append(Token(Token.PERIOD,'.',self.line))
                self.advance()
            elif char in Lexer.Operators:
                type_ = Lexer.Operators[char]
                self.tokens.append(Token(type_, char,self.line))
                self.advance()
            else:
                print(f'Invalid character \'{char}\'')
                self.advance()
        self.tokens.append(Token(Token.EOF, "EOF",self.line))