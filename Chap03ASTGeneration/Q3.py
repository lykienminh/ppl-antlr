class ASTGeneration(MPVisitor):
    # program: vardecls EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        vardecls = self.visit(ctx.vardecls())

        return Program(vardecls)

    # vardecls: vardecl vardecltail;
    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        vardecl = self.visit(ctx.vardecl())
        vardecltail = self.visit(ctx.vardecltail())

        return vardecl + vardecltail

    # vardecltail: vardecl vardecltail | ;
    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        if ctx.getChildCount() == 0: 
            return []

        vardecl = self.visit(ctx.vardecl())
        vardecltail = self.visit(ctx.vardecltail())

        return vardecl + vardecltail

    # vardecl: mptype ids ';' ;
    # int a, b; => [VarDecl(Id(a), IntType), VarDecl(Id(b), IntType)]
    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        mptype = self.visit(ctx.mptype())
        ids = self.visit(ctx.ids())
        # list comprehension
        return [VarDecl(x, mptype) for x in ids]
    
    # mptype: INTTYPE | FLOATTYPE;
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return IntType() if ctx.INTTYPE() else FloatType()
    
    # ids: ID ',' ids | ID; 
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.getChildCount() == 1: 
            return [Id(ctx.ID().getText())]
        return [Id(ctx.ID().getText())] + self.visit(ctx.ids())
