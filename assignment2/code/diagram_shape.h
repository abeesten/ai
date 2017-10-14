//diagram_shape.h

#ifndef diagram_shape_h
#define diagram_shape_h

#include <vector>
#include <string>

using namespace std;

class DiagramShape;

enum ShapeType {CIRCLE, DOT, SQUARE, RECTANGLE, TRIANGLE, SCC};
enum SizeType {SMALL, MEDIUM, LARGE};

class DiagramShape {
public:
  //diagram name
  string id;

  //x-coordinate of center
  int x;

  //y-coordinate of center
  int y;

  //number of size of SCC
  int numSides;

  //shapetype
  ShapeType type;

  SizeType size;
};

#endif
