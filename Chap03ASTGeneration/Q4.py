class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        # int a, b; float x;
        # [[VarDecl(a, IntType), VarDecl(b, IntType)], [VarDecl(x, FloatType)]] => flatten
        vardecls = [self.visit(x) for x in ctx.vardecl()]
        return Program([x for z in vardecls for x in z])

    def visitVardecl(self,ctx:MPParser.VardeclContext):
        mptype = self.visit(ctx.mptype())
        ids = self.visit(ctx.ids())
        return [VarDecl(x, mptype) for x in ids]

    def visitMptype(self,ctx:MPParser.MptypeContext):
        return IntType() if ctx.INTTYPE() else FloatType()

    def visitIds(self,ctx:MPParser.IdsContext):
        ids = ctx.ID()
        return [Id(x.getText()) for x in ids]

# =================================================================================================

# program: vardecl+ EOF;
# vardecl: mptype ids ';' ;
# mptype: INTTYPE | FLOATTYPE;
# ids: ID (',' ID)*; 
# INTTYPE: 'int';
# FLOATTYPE: 'float';
# ID: [a-z]+ ;
