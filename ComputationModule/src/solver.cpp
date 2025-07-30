#include "solver.h"

// Constructor
matrix::matrix(string filename)
{
    int ret = read_matrix(filename);
    this->swaps_.resize(this->height_);
    for (int i = 0; i < height_; i++)
    {
        this->swaps_[i].resize(this->width_);
    }
}

// Load matrix and its size
int matrix::read_matrix(string filename)
{
    ifstream file(filename);
    if (!file.is_open())
        return 1;
    
    file >> this->width_ >> this->height_;

    this->matrix_.resize(this->height_);
    for (int i = 0; i < height_; i++)
    {
        this->matrix_[i].resize(this->width_);
    }
    
    for(size_t i = 0; i < this->height_; ++i)
    {
        for(size_t j = 0; j < this->width_; ++j)
            file >> this->matrix_[i][j];
    }   

    return 0;
}

// Sorts rows of the matrix using bubblesort
void matrix::sort_rows()
{
    for (int i = 0; i < height_; i++)
    {
        swaps_[i] = sort_bubble_with_swaps(matrix_[i]);
    }
    
}

// Prints matrix to console
void matrix::print_matrix()
{
    for (int i = 0; i < height_; i++)
    {
        for (int j = 0; j < width_; j++)
        {
            cout << matrix_[i][j] << " ";
        }
        cout << endl;
    }
}

// Solve and return results of the MaxMax algorithm
vector<int> matrix::solve(int p)
{   
    sort_rows();

    float max = matrix_[0][p - 1];
    int max_index = 0;
    for (int i = 0; i < height_; i++)
    {
        if (matrix_[i][p - 1] > max)
        {
            max = matrix_[i][p - 1];
            max_index = i;
        }
    }
    
    vector<int> result(p);
    for (int i = 0; i < p; i++)
    {
        result[i] = swaps_[max_index][i];
    }
    return result;   
}

// Locates the row index with the minimum value in a given column
float matrix::find_min_in_col(int col)
{
    float min = this->matrix_[(col + 1) % width_][col];
    for (int i = 0; i < this->height_; i++)
    {
        if (this->matrix_[i][col] != 0 && this->matrix_[i][col] < min)
        {
            min = this->matrix_[i][col];
        }
    }
    return min;
}

// Creates the LMIN matrix
void matrix::construct_lmin()
{
    this->lmin.resize(this->width_);
    this->lmin_header.resize(this->width_);
    for (int i = 0; i < this->width_; i++)
    {
        lmin_header[i] = i + 1;
        lmin[i] = find_min_in_col(i);
    }    
}

// Prints LMIN to console
void matrix::print_lmin()
{
    for (int i = 0; i < this->width_; i++)
    {
        cout << this->lmin_header[i] << " ";
    }
    cout << "\n";
    for (int i = 0; i < this->width_; i++)
    {
        cout << this->lmin[i] << " ";
    }
    cout << "\n";
}

// Solve and return the results of the MaxMin algorithm
vector<int> matrix::solve_dacpm(int p)
{
    this->construct_lmin();
    
    this->lmin_header = sort_bubble_with_swaps(lmin);
    
    vector<int> res;
    res.reserve(p);
    for (int i = 0; i < p; i++)
    {
        res.push_back(lmin_header[i]); 
    }
    return res;
}

matrix::~matrix()
{
}