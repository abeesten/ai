// readInput

#ifndef io_hpp
#define io_hpp

#include <stdio.h>
#include <vector>
#include <fstream>
#include <iostream>

#include "diagram.h"

using namespace std;

//Fills in a vector  and their relation along with
void readInput(string fileName, vector <Diagram> &diagrams);

#endif
