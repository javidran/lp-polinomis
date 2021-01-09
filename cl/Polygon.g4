grammar Polygon;

root : (assig | printsmth | area | perimeter | vertices | centroid | inside | equal | draw | color)* EOF;

string: QUOTE STRING QUOTE;

point: RNUM RNUM;

polygon : LPARENTHESIS polygon RPARENTHESIS     #priority
    | LBRACKET point* RBRACKET                  #newpolygon
    | polygon INTERSECT polygon                 #intersection
    | polygon UNION polygon                     #convexunion
    | RANDOM NATNUM                             #random
    | assignedid                                #polygonid
    ;

assig: ID ASSIG polygon;

assignedid: ID;

printsmth : PRINT polygon
    | PRINT string
    ;

area: AREA polygon;

perimeter: PERIMETER polygon;

vertices: VERTICES polygon;

centroid: CENTROID polygon;

inside: INSIDE polygon COMMA polygon;

equal: EQUAL polygon COMMA polygon;

draw: DRAW string (COMMA polygon)+;

colornum: NUM NUM NUM;

color: COLOR polygon COMMA LCLAUDATOR colornum RCLAUDATOR;


RNUM : ('-')? NUM ;
NUM : NATNUM ('.' NATNUM)? ;
NATNUM : [0-9]+ ;

LPARENTHESIS : '(';
RPARENTHESIS : ')';
LBRACKET : '[' ;
RBRACKET : ']' ;
LCLAUDATOR : '{';
RCLAUDATOR : '}';

ASSIG : ':=';
INTERSECT : '*';
UNION : '+';
BOUNDING : '#';
RANDOM: '!';
COMMA: ',';
QUOTE: '"';

PRINT: 'print';
AREA: 'area';
PERIMETER: 'perimeter';
VERTICES: 'vertices';
CENTROID: 'centroid';
COLOR: 'color';
INSIDE: 'inside';
EQUAL: 'equal';
DRAW: 'draw';

STRING : [0-9A-Za-z._\-]+ ;
ID : [a-zA-Z] [a-zA-Z0-9_]* ;
COMMENT : '//' ~[\r\n]* -> skip ;
WS : [ \r\n\t]+ -> skip ;