#include <iostream>
#include <ctime>

using namespace std;

int main()
{
    int n;

    cout << "Enter data size: ";
    cin >> n;
    cout << endl;

    clock_t start1 = clock();

    // Simulated algorithm
    long sum = 0;
    long long product = 1;

    for (int i = 0; i < n; i++)
    {
        sum += i;
    }
    clock_t end1 = clock();

    clock_t start2 = clock();
    for (int i = 0; i < n; i++)
    {
        product *= i;
    }
    clock_t end2 = clock();

    double ticks1 = (double)(end1 - start1);
    double ticks2 = (double)(end2 - start2);

    cout << "Type: Sum " << sum << endl;
    cout << "Ticks= " << ticks1 << endl
         << endl;

    cout << "Type: Product " << product << endl;
    cout << "Ticks: " << ticks2 << endl;

    return 0;
}