class ASTGeneration(MPVisitor):
    # program: exp EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return Program(self.visit(ctx.exp()))

    # exp: term ASSIGN exp | term;
    def visitExp(self,ctx:MPParser.ExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.term())
        left = self.visit(ctx.term())
        right = self.visit(ctx.exp())
        return Binary(ctx.ASSIGN().getText(), left, right)

    # term: factor COMPARE factor | factor;
    def visitTerm(self,ctx:MPParser.TermContext): 
        if ctx.getChildCount() == 1:
            # Although factor have 1 in this case => but we still use ctx.factor(0)
            # Because ctx.factor() return a list in this case
            return self.visit(ctx.factor(0))
        left = self.visit(ctx.factor(0))
        right = self.visit(ctx.factor(1))
        return Binary(ctx.COMPARE().getText(), left, right) 

    # factor: factor ANDOR operand | operand; 
    def visitFactor(self,ctx:MPParser.FactorContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.operand())
        left = self.visit(ctx.factor())
        right = self.visit(ctx.operand())
        return Binary(ctx.ANDOR().getText(), left, right)

    # operand: ID | INTLIT | BOOLIT | '(' exp ')';
    def visitOperand(self,ctx:MPParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText())) 
        elif ctx.BOOLIT():
            return BooleanLiteral(ctx.BOOLIT().getText() == 'True')
        return self.visit(ctx.exp())
