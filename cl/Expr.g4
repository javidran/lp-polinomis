grammar Expr;

root : expr EOF ;

expr : expr MES expr
    | NUM
    ;

NUM : ('-')? ('0'..'9')+ ;
POINT : NUM NUM;
MES : '+' ;
WS : [ \n]+ -> skip ;