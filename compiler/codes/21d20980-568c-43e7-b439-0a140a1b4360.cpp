#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> nums(n);  // Fixed: Resize the vector to size n
        
        // Read the elements into nums
        for (int i = 0; i < n; i++) {
            cin >> nums[i];
        }
        
        reverse(nums.begin(), nums.end());
        
        // Output the reversed array
        for (int i = 0; i < n; i++) {
            cout << nums[i] << " ";
        }
        cout << endl;
    }
    return 0;
}