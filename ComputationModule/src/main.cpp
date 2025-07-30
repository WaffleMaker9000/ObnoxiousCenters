#include "solver.h"


int main(int argc, char const *argv[])
{
    if (argc < 3)
    {
        return 1;
    }

    // Parse arguments and load matrix
    string filename = argv[1];
    int p = atoi(argv[2]);
    matrix m = matrix(filename);
    
    // Solve and print results of DACPM
    vector<int> res = m.solve_dacpm(p);
    for (size_t i = 0; i < p; i++)
    {
        cout << res[i] << " ";
    }
    cout << "\n";
    
    // Solve and print results of MaxMin
    res = m.solve(p);
    for (size_t i = 0; i < p; i++)
    {
        cout << res[i] << " ";
    }
    cout << "\n";
}
