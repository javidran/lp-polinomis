grammar Polygon;

root : expr EOF;

expr : ID ASSIG expr
    | POINTS
    ;

NUM : ('-')? ('0'..'9')+ ;
POINT : NUM NUM ;
POLYGON : '[' POINT* ']';
PNUM : ('0'..'9')+ ;
COLOR : '{' NUM NUM NUM '}' ;
ASSIG : ':=';
ID : ('a'..'z' | 'A'..'Z' | '_' | '0'..'9')+;
WS : [ \n]+ -> skip ;