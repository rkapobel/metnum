#include <iostream>
#include <math.h>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <new>
#include <regex>
#include <iterator>
#include "sparseMatrix.h"

using namespace std;

SparseMatrix<double> rank(Matrix<double> M, double c, double d);
double uniform_rand(double a, double b);

const int number_line = 3;

int main(int argc, char** argv) {

	if (argc < 6) {
		printf("Usage: %s algorithm: 0 (pageRank) 1 (alternative) / teletransportation probability / instance type: 0 (web pages) 1 (deportes) / input file / tolerance / result (optional)\n", argv[0]);
		return 0;
	}
	
	ifstream inputFile(argv[4]);

	if (!inputFile.good()) {
		printf("Non-existant input file.\n");
		return 0;
	}

    FILE * pFile = NULL;
    
    if (argc == 7) {
        pFile = fopen(argv[6],"w");
    }
    
    cout << "alg: " << (*argv[1] - '0') << endl;
	int alg = (int) (*argv[1] - '0');
	if (alg != 0 && alg != 1) {
		printf("Error: Invalid algorithm.\n");
		return 0;
	}
	
	cout << "c: " << atof(argv[2]) << endl;
	double c = (double) atof(argv[2]);
	if (c < 0 || c > 1) {
		printf("Error: Invalid teletransportation probability.\n");
		return 0;
	}
	
	cout << "inst: " << (*argv[3] - '0') << endl;
	int inst = (int) (*argv[3] - '0');
	if (inst != 0 && inst != 1) {
		printf("Error: Invalid instance type.\n");
		return 0;
	}

	cout << "tolerance: " << atof(argv[5]) << endl;
	double e = (double) atof(argv[5]);
	if (e < 0 || e > 1) {
		printf("Error: Invalid tolerance.\n");
		return 0;
	}
		
    int nodes = 0;
    int edges = 0;
  
  	string line;
	getline(inputFile, line);
	sscanf(line.c_str(),"%d %d", &nodes, &edges);
 
    cout << "nodes: " << nodes << " edges: " << edges << endl;
    Matrix<double> M(nodes, nodes);

    if (inst == 0){
        if (alg == 0){
           int i = 0;           
           while(i < edges){
                int node_from = 0;
                int node_to = 0;
                
	            getline(inputFile, line);
	            sscanf(line.c_str(),"%d %d", &node_from, &node_to);
	            cout << "node_from: " << node_from << " node_to: " << node_to << endl;
	            M(node_to-1, node_from-1) = 1;
                i++;
           }
        }else{
            // group algorithm webs
        }
    }else{
        if (alg == 0){
            // page rank sports
        }else{
            // group algorithm sports
        }
    }
    
    M.printMatrix();
    
    //Depending on input data, create a matrix with the input file and call rank with matrix a values

	return 0;
}

Matrix<double> rank(Matrix<double>& M, double c, double d) {
    //work work work (https://en.wikipedia.org/wiki/PageRank buen codigo en matlab, es simple, el laburo esta en parsear todo)
    srand(45);

    double n = M.rows();
    Matrix<double> E(M.rows(), M.rows(), (1 - c)*1/n); // PRE: rows == columns
    Matrix<double> M_hat = M*c - E;
    SparseMatrix<double> A(M_hat);
    SparseMatrix<double> x(M.rows());
    
    for (int i = 0; i < M.rows(); i++) {
        x(i) = uniform_rand(0, 1);
    }
    
    SparseMatrix<double> last_x(M.rows());
    
    double delta = 0;
    
    do {
        last_x = x;
        x = A*x;
        delta = x.L1(last_x);
    }while (delta > d);
    
    printf("delta is %3.3f ", delta); //Deberia devolverse.
    
    return x.descompress();
}

double uniform_rand(double a, double b) {
    return ((b-a)*((double)rand()/RAND_MAX))+a;
}
