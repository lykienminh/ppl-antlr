class ASTGenerator(CSELVisitor):

    # Visit a parse tree produced by CSELParser#program.
    # program: decl+ EOF;
    def visitProgram(self, ctx:CSELParser.ProgramContext):
        decls = [self.visit(x) for x in ctx.decl()]

        return Program([x for y in decls for x in y])

    # Visit a parse tree produced by CSELParser#cseltype.
    # cseltype: INT | FLOAT | BOOLEAN;
    def visitCseltype(self, ctx:CSELParser.CseltypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        return BooleanType();

    # Visit a parse tree produced by CSELParser#decl.
    # decl: vardecl decltail | constdecl decltail | funcdecl decltail;
    def visitDecl(self, ctx:CSELParser.DeclContext):
        decltail = self.visit(ctx.decltail())
        if ctx.vardecl():
            return self.visit(ctx.vardecl()) + decltail
        if ctx.constdecl():
            return self.visit(ctx.constdecl()) + decltail
        return self.visit(ctx.funcdecl()) + decltail

    # Visit a parse tree produced by CSELParser#decltail.
    # decltail: vardecl decltail | constdecl decltail | funcdecl decltail | ; 
    def visitDecltail(self, ctx:CSELParser.DecltailContext):
        if ctx.getChildCount() == 0:
            return []
        
        decltail = self.visit(ctx.decltail())
        if ctx.vardecl():
            return self.visit(ctx.vardecl()) + decltail
        elif ctx.constdecl():
            return self.visit(ctx.constdecl()) + decltail
        return self.visit(ctx.funcdecl()) + decltail

    # Visit a parse tree produced by CSELParser#vardecl.
    # vardecl: LET single_vardecls SEMI;
    def visitVardecl(self, ctx:CSELParser.VardeclContext):
        return self.visit(ctx.single_vardecls())

    # Visit a parse tree produced by CSELParser#single_vardecls.
    # single_vardecls: single_vardecl single_vardecltail;
    def visitSingle_vardecls(self, ctx:CSELParser.Single_vardeclsContext):
        single_vardecl = self.visit(ctx.single_vardecl())
        single_vardecltail = self.visit(ctx.single_vardecltail())
        return single_vardecl + single_vardecltail

    # Visit a parse tree produced by CSELParser#single_vardecl.
    # single_vardecl: ID COLON cseltype;
    def visitSingle_vardecl(self, ctx:CSELParser.Single_vardeclContext):
        return [VarDecl(Id(ctx.ID().getText()), self.visit(ctx.cseltype()))]

    # Visit a parse tree produced by CSELParser#single_vardecltail.
    # single_vardecltail: COMMA single_vardecl single_vardecltail | ;
    def visitSingle_vardecltail(self, ctx:CSELParser.Single_vardecltailContext):
        if ctx.getChildCount() == 0:
            return []

        single_vardecl = self.visit(ctx.single_vardecl())
        single_vardecltail = self.visit(ctx.single_vardecltail())
        return single_vardecl + single_vardecltail

    # Visit a parse tree produced by CSELParser#constdecl.
    # constdecl: CONST single_constdecl SEMI;
    def visitConstdecl(self, ctx:CSELParser.ConstdeclContext):
        return self.visit(ctx.single_constdecl())

    # Visit a parse tree produced by CSELParser#single_constdecl.
    # single_constdecl: ID COLON cseltype EQ expr;
    # class ConstDecl(Decl): # id: Id, typ: Type, value: Expr
    def visitSingle_constdecl(self, ctx:CSELParser.Single_constdeclContext):
        typ = self.visit(ctx.cseltype())
        value = self.visit(ctx.expr())
        return [ConstDecl(Id(ctx.ID().getText()), typ, value)]

    # Visit a parse tree produced by CSELParser#expr.
    # expr: INTLIT | FLOATLIT | BOOLEANLIT;
    def visitExpr(self, ctx:CSELParser.ExprContext):
        if ctx.INTLIT():
            return IntLit(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLit(float(ctx.FLOATLIT().getText()))
        return BooleanLit(ctx.BOOLEANLIT().getText() == 'True')

    # Visit a parse tree produced by CSELParser#funcdecl.
    # funcdecl: FUNCTION ID LR paramlist RR SEMI;
    def visitFuncdecl(self, ctx:CSELParser.FuncdeclContext):
        return [FuncDecl(Id(ctx.ID().getText()), self.visit(ctx.paramlist()))]

    # Visit a parse tree produced by CSELParser#paramlist.
    # paramlist: single_vardecls | ;
    def visitParamlist(self, ctx:CSELParser.ParamlistContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.single_vardecls())

# =================================================================================================
# SEMI: ';';
# COLON: ':';
# COMMA: ',';
# LR: '(';
# RR: ')';
# EQ: '=';
# INT: 'Int';
# FLOAT: 'Float';
# BOOLEAN: 'Boolean';
# INTLIT: [0-9]+;
# FLOATLIT: [0-9]+ '.' [0-9]+;
# BOOLEANLIT: 'True' | 'False';
# ID: [a-zA-Z]+;
# WS: [ \t\r\n\f]+ -> skip;
# and AST classes as follows:
# class Program(ABC): # decl: List[Decl]
# class Type(ABC): pass
# class IntType(Type)
# class FloatType(Type)
# class BooleanType(Type)
# class LHS(ABC): pass
# class Id(LHS): # name: str
# class Decl(ABC): pass
# class VarDecl(Decl): # id: Id, typ: Type
# class ConstDecl(Decl): # id: Id, typ: Type, value: Expr
# class FuncDecl(Decl): # name: Id, param: List[VarDecl]
# class Exp(ABC): pass
# class IntLit(Exp): # value: int
# class FloatLit(Exp): # value: float
# class BooleanLit(Exp): # value: bool
