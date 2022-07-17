# Count non-terminal node
class ASTGeneration(MPVisitor):
    # program: vardecls EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.vardecls()) + 2

    # vardecls: vardecl vardecltail;
    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail()) + 2

    # vardecltail: vardecl vardecltail | ;
    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        if ctx.getChildCount() == 0:
            return 0
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail()) + 2

    # vardecl: mptype ids ';' ;
    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        return self.visit(ctx.mptype()) + self.visit(ctx.ids()) + 2
    
    # mptype: INTTYPE | FLOATTYPE;
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return 0
    
    # ids: ID ',' ids | ID; 
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.getChildCount() == 1: 
            return 0
        return self.visit(ctx.ids()) + 1
