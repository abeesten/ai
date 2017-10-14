//Diagram.h

#ifndef diagram_h
#define diagram_h

#include <vector>

#include "diagram_shape.h"

using namespace std;

enum RelationType {LEFT_OF, RIGHT_OF, ABOVE, BELOW, INSIDE, OVERLAP};

struct Relation {
public:
  //stores ids of realted shapes
  string otherShape_id;
  RelationType relation_type;
};

class Diagram;

class Diagram{
public:
  string diagram_name;
  vector<DiagramShape> shapes;
  vector<Relation> relations;
}
