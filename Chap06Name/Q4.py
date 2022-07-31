class StaticCheck(Visitor):

    # class Program: #decl:List[Decl]
    def visitProgram(self,ctx:Program,o:object):
        o = [[]]
        for decl in ctx.decl:
            self.visit(decl, o)

    # class VarDecl(Decl): #name:str,typ:Type
    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredVariable(ctx.name)
        o[0] += [ctx.name]

    # class ConstDecl(Decl): #name:str,val:Lit
    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredConstant(ctx.name)
        o[0] += [ctx.name]

    # class FuncDecl(Decl): #name:str,param:List[VarDecl],body:Tuple(List[Decl],List[Expr])
    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredFunction(ctx.name)
        o[0] += [ctx.name]

        env = [[]] + o
        for decl in ctx.param:
            self.visit(decl, env)
        
        for decl in ctx.body[0]:
            self.visit(decl, env)

        for expr in ctx.body[1]:
            self.visit(expr, env)

    def visitIntType(self,ctx:IntType,o:object):pass

    def visitFloatType(self,ctx:FloatType,o:object):pass

    def visitIntLit(self,ctx:IntLit,o:object):pass

    # class Id(Expr): #name:str
    def visitId(self,ctx:Id,o:object):
        for env in o:
            if ctx.name in env: return
        raise UndeclaredIdentifier(ctx.name)
