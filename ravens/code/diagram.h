//Diagram.h

#ifndef diagram_h
#define diagram_h

#include <vector>

#include "diagram_shape.h"

using namespace std;

enum RelationType {LEFT_OF, ABOVE, INSIDE, OVERLAP};

struct Relation {
public:
  //stores ids of related shapes
  string firstShape;
  string secondShape;
  RelationType relationType;
};

class Diagram;

class Diagram{
public:
  string diagram_name;
  vector<DiagramShape> shapes;
  vector<Relation> relations;
};

#endif
