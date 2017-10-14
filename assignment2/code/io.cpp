#include "io.h"
#include "diagram_shape.h"
#include "diagram.h"

void readInput(string fileName, vector<Diagram> &diagrams){
  ifstream infile;
  string data;
  infile.open(fileName);
  string diagramID;

  if (infile.is_open()){
    while (getline(infile, data)){
      cout << "data" << '\n';
      /*dgrm = Diagram();
      istringstream ss(data);
      getline(ss, id);
      if (id == '\n'){
        continue;
      }
      dgrm.diagram_name = id;
      getShapes(ss);
      getRelations(ss);*/

    }
  }
}
