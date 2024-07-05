#include <iostream>

void reverseArray(int arr[], int n) {
    int start = 0;
    int end = n - 1;

    while (start < end) {
        // Swap elements at start and end indices
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;

        // Move indices towards the center
        start++;
        end--;
    }
}

int main() {
    int n;
    
    std::cin >> n;

    int arr[n];
    for (int i = 0; i < size; i++) {
        std::cin >> arr[i];
    }

   

    reverseArray(arr, n);

    
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}