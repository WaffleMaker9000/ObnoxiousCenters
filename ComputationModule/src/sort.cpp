#include "sort.h"

// From geeksforgeeks at https://www.geeksforgeeks.org/bubble-sort-algorithm/,
// modified to return a vector of the swaps that occur
vector<int> sort_bubble_with_swaps(vector<float>& arr) {
    int n = arr.size();
    bool swapped;
    vector<int> swaps(n);

    for (int i = 0; i < n; i++)
    {
        swaps[i] = i;
    }

    for (int i = 0; i < n - 1; i++) {
        swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] < arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swap(swaps[j], swaps[j + 1]);
                swapped = true;
            }
        }
      
        // If no two elements were swapped, then break
        if (!swapped)
            break;
    }
    return swaps;
}

