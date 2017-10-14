#include <sstream>

#include "io.h"
#include "diagram_shape.h"
#include "diagram.h"


string findInput(string line){
  string ID = "ID";
  string SHAPE = "SHAPE";
  string RELATION = "RELATION";
  if (isupper(line[0])){
    return ID;
  }
  else {
    for (int i = 0; i < line.size(); i++){
      if (line[i] == '='){
        return SHAPE;
      }
    }
    if (line[0] != '\0'){
      return RELATION;
    }
  }
  return "EMPTY";
} 

void readInput(string fileName, vector<Diagram> &diagrams){
  //All these variables aren't really necessary but it makes reading
  //the code easier.
  ifstream infile;
  string data;
  string shape;
  infile.open(fileName);
  string diagramID;
  string ID = "ID";
  string SHAPE = "SHAPE";
  string RELATION = "RELATION";
  string line = "";
  string type = "";
  string junk;
  string shapeId;
  string shapeType;
  string size;

  //relationship string
  string rel;

  //x-coord
  int x;

  //y-coord
  int y;

  //scc numSides
  int numSides;
  Diagram dgrm;
  dgrm = Diagram();
  if (infile.is_open()){
    while (getline(infile, data)){
      //while loop goes though line by line
      istringstream ss(data);
      getline(ss, line, '\n');
      type = findInput(line);
      if (type == ID){
        dgrm.diagram_name = line;
      }
      else if (type == SHAPE){
        //fill in all diagram shape stuff and then push it into dgrm
        DiagramShape dShape;
        dShape = DiagramShape();
        stringstream st(line);
        st >> shapeId;
        dShape.id = shapeId;
        switch(shapeId[0]) {
          case 'c': dShape.type = CIRCLE;
                    break;
          case 'd': dShape.type = DOT;
                    break;
          case 'r': dShape.type = RECTANGLE;
                    break;
          case 't': dShape.type = TRIANGLE;
                    break;
          case 's':
                    if (shapeId[1] == 'c'){
                      dShape.type = SCC;
                    } 
                    else {
                      dShape.type = SQUARE;
                    }
                    break;
        }
        getline(st, junk, '\'');
        getline(st, size, '\'');
        switch(size[0]) {
          case 's': dShape.size = SMALL;
                    break;
          case 'm': dShape.size = MEDIUM;
                    break;
          case 'l': dShape.size = LARGE;
                    break;
        }
        st >> junk;
        st >> x;
        dShape.x = x;
        st >> junk;
        st >> y;
        dShape.y = y;
        st >> junk;
        if (dShape.type == 5){
          st >> numSides;
          dShape.numSides = numSides;
        }
        dgrm.shapes.push_back(dShape);
      }
      else if (type == RELATION) {
        Relation relation;
        relation = Relation();
        stringstream st(line);
        //getline(st, junk, "(");
        getline(st, rel, '(');
        switch(rel[0]) {
          case 'o': relation.relationType = OVERLAP;
                    break;
          case 'l': relation.relationType = LEFT_OF;
                    break;
          case 'a': relation.relationType = ABOVE;
                    break;
          case 'i': relation.relationType = INSIDE;
                    break;          
        }
        string firstRShape;
        string secondRShape;
        getline(st, firstRShape, ',');
        relation.firstShape = firstRShape;
        st.ignore();
        getline(st, secondRShape, ')');
        relation.secondShape = secondRShape;
        dgrm.relations.push_back(relation);
      }
      else {
        diagrams.push_back(dgrm);
        dgrm = Diagram();
        //clear diagram and keep going
        continue;
      }
      //getShapes(ss);
      //getRelations(ss);
    }
  }
}


