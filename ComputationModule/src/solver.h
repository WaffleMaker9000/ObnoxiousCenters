#include <vector>
#include <algorithm>
#include <iostream>
#include "sort.h"
#include <fstream>
#include <sstream>

using namespace std;

class matrix
{
private:
    vector<vector<float>> matrix_;
    vector<vector<int>> swaps_;
    vector<int> lmin_header;
    vector<float> lmin;
    int width_;
    int height_;
    void sort_rows();
    float find_min_in_col(int col);
    void construct_lmin();
public:
    void print_matrix();
    int read_matrix(string filename);
    matrix(string filename);
    vector<int> solve(int p);
    void print_lmin();
    vector<int> solve_dacpm(int p);
    ~matrix();
};
