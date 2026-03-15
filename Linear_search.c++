#include <iostream>
using namespace std;
int main() {
    int arr[5] = {4, 7, 1, 9, 5};
    int key;
    bool found = false;
    cout << "Enter number to search: ";
    cin >> key;
    for(int i = 0; i < 5; i++) {
        if(arr[i] == key) {
            cout << "Element found at index " << i;
            found = true;
            break;
        }
    }
    if(!found) {
        cout << "Element not found";
    }
    return 0;
}
