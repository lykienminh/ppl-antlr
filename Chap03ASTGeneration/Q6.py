# class Binary(Expr):  #op:string;left:Expr;right:Expr

# class Id(Expr): #value:string

# class IntLiteral(Expr): #value:int

# class BooleanLiteral(Expr): #value:boolean

from functools import reduce

class ASTGeneration(MPVisitor):

    # program: exp EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.exp())

    # exp: (term ASSIGN)* term;
    # -> right-associative
    def visitExp(self,ctx:MPParser.ExpContext):
        terms = [self.visit(x) for x in ctx.term()]
        assigns = [x.getText() for x in ctx.ASSIGN()]

        right = terms[-1]

        for i in range(len(assigns)):
            op = assigns[len(assigns) - 1 - i]
            left = terms[len(terms) - 1 - i - 1]
            right = Binary(op, left, right)

        return right 

    # term: factor COMPARE factor | factor;
    def visitTerm(self,ctx:MPParser.TermContext): 
        if ctx.getChildCount() == 1:
            return self.visit(ctx.factor(0))

        left = self.visit(ctx.factor(0))
        right = self.visit(ctx.factor(1))

        return Binary(ctx.COMPARE().getText(), left, right)

    # factor: operand (ANDOR operand)*; 
    # -> left-associative
    def visitFactor(self,ctx:MPParser.FactorContext):
        operands = [self.visit(x) for x in ctx.operand()]
        andors = [x.getText() for x in ctx.ANDOR()]

        left = operands[0]
        for i in range(len(andors)):
            op = andors[i]
            right = operands[i + 1]
            left = Binary(op, left, right)
        
        return left 

    # operand: ID | INTLIT | BOOLIT | '(' exp ')'; 
    def visitOperand(self,ctx:MPParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.BOOLIT():
            return BooleanLiteral(ctx.BOOLIT().getText() == 'True')
        return self.visit(ctx.exp()) 
