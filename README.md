# DAA Assignment Automation

A Python tool that automates the repetitive parts of **Design & Analysis of Algorithms (DAA)** assignments:

- Run C++ programs on multiple data sizes
- Run each size multiple times
- Calculate average execution time
- Compare multiple algorithms
- Generate a performance graph
- Collect program outputs
- Generate a formatted PDF containing the assignment

## 🎥 Demonstration

[![Watch the video](https://youtube.com)](https://youtu.be/h2melDyn_tI)

---

## 1. Setup

### Requirements

- Python 3
- C++ compiler (e.g. MinGW/G++)
- `matplotlib`
- `reportlab`

Install the Python packages:

```bash
pip install matplotlib reportlab
```

Clone/download this repository and keep the files together:

```text
project/
├── manager.py
├── pdf_generator.py
├── info.txt
└── Sample programs for testing/
    ├── sortings.cpp
    └── sortings.exe
```

---

## 2. How Your C++ Program Must Work

This is the **most important requirement**.

The Python manager runs your `.exe` automatically and sends the **data size through standard input**.

Your C++ program should therefore accept one integer:

```cpp
int n;
cin >> n;
```

For example, if Python is testing `10000`, your program receives:

```text
10000
```

### Required Output Format

The Python program identifies algorithms using:

```text
Type: <algorithm name>
Ticks: <time>
```

Example:

```text
Type: Merge Sort
Ticks: 152
```

If you are comparing multiple algorithms:

```text
Type: Merge Sort
Ticks: 152

Type: Quick Sort
Ticks: 97

Type: Heap Sort
Ticks: 131
```

### Important

The words `Type:` and `Ticks:` are used by the Python parser.

If your program outputs something different, either change your C++ output or modify the parser in `manager.py`.

---

## 3. Example C++ Program

```cpp
#include <iostream>
#include <chrono>

using namespace std;
using namespace std::chrono;

int main()
{
    int n;
    cin >> n;

    auto start = high_resolution_clock::now();

    // Your algorithm here

    auto end = high_resolution_clock::now();

    auto ticks =
        duration_cast<nanoseconds>(end - start).count();

    cout << "Type: My Algorithm" << endl;
    cout << "Ticks: " << ticks << endl;

    return 0;
}
```

Compile it:

```bash
g++ algorithm.cpp -o algorithm.exe
```

You can still run the C++ program normally:

```bash
algorithm.exe
```

It will wait for the data size:

```text
10000
```

---

## 4. Running the Python Manager

Run:

```bash
python manager.py
```

It will ask:

```text
Enter C++ exe file name with address:
```

Example:

```text
C++\algorithm.exe
```

Then:

```text
Enter data sizes to run (eg: 100, 1000 etc) as tuple:
(100, 1000, 10000, 100000)
```

Then:

```text
Num of times to run program per data size:
5
```

This means:

```text
100       → 5 runs
1000      → 5 runs
10000     → 5 runs
100000    → 5 runs
```

The average of the runs is used for the final results.

---

## 5. Comparing Multiple Algorithms

Your C++ program can benchmark multiple algorithms in a single execution.

For example:

```cpp
cout << "Type: Linear Search" << endl;
cout << "Ticks: " << linearTime << endl;

cout << "Type: Binary Search" << endl;
cout << "Ticks: " << binaryTime << endl;

cout << "Type: Direct Search" << endl;
cout << "Ticks: " << directTime << endl;
```

The Python manager automatically detects each `Type:` and creates separate results for them.

The generated graph will contain a separate line for each algorithm.

---

## 6. Data Sizes

You can enter any suitable data sizes:

```text
(100, 1000, 10000, 100000)
```

or:

```text
(100, 500, 1000, 5000, 10000)
```

Choose sizes appropriate for your algorithm.

Very slow algorithms may take a long time with large inputs.

The graph uses **equal spacing between tested data sizes**, so sizes such as `100`, `1000`, `10000`, and `1000000` remain readable.

---

## 7. Assignment PDF

After benchmarking, `manager.py` asks for:

```text
Assignment number
Assignment name
Assignment statement
Theory
Time complexity
Space complexity
Complexity analysis / conclusion
```

The generated PDF contains:

1. Assignment information
2. Assignment statement
3. Theory
4. C++ code
5. Program output
6. Complexity analysis
7. Performance results table
8. Performance graph

The PDF is generated as:

```text
Assignment_<number>.pdf
```

For example:

```text
Assignment_3.pdf
```

---

## 8. Theory & Complexity

This project currently **does not use an AI API**.

Before entering the theory, `manager.py` displays a small prompt you can copy into Claude/ChatGPT and ask it to generate concise content.

You then enter:

```text
Theory:
...

Time complexity:
...

Space complexity:
...

Complexity analysis / conclusion:
...
```

This keeps the project free from API costs and API-key setup.

---

## 9. Custom C++ Benchmarks

You normally **do not need to modify the Python code** for every new algorithm.

Just make your C++ program follow the input/output contract:

### Input

```text
<data size>
```

### Output

```text
Type: <algorithm name>
Ticks: <number>
```

For example, for a sorting assignment:

```text
Type: Merge Sort
Ticks: 120

Type: Quick Sort
Ticks: 95

Type: Heap Sort
Ticks: 110
```

Then compile your program and give its `.exe` path to `manager.py`.

---

## 10. Using a Different C++ Output Format

If your existing code produces:

```text
Algorithm: Quick Sort
Time: 95
```

you can either change the C++ output to:

```text
Type: Quick Sort
Ticks: 95
```

or modify the parser in `manager.py`.

The relevant section is:

```python
if line.startswith("Type: "):
    category = line.removeprefix("Type: ").strip()

elif line.startswith("Ticks"):
    ticks = int(line.split(":")[1])
```

Change this if you want to support your own output format.

---

## 11. Student Information

Edit `info.txt` to contain the information you want displayed in the PDF.

Example:

```text
Name: Your Name
Enrollment Number: Your Enrollment Number
Course: B.Tech CSE
Subject: Design and Analysis of Algorithms
```

---

## Project Structure

```text
project/
│
├── manager.py
├── pdf_generator.py
├── info.txt
│
├── performance.png
├── Assignment_1.pdf
│
└── Sample programs for testing/
    ├── sortings.cpp
    └── sortings.exe
```

---

## Contributing

This project is made for students and is open source.

Useful future improvements could include:

- Automatic C++ compilation
- Better cross-platform support
- Automatic screenshots
- GUI
- More graph options
- Config files
- Assignment templates
- Optional AI integration

Feel free to open an issue or pull request if you have improvements.

---

## ⭐ If This Helped

If this saves you from manually running the same algorithm 20 times and making graphs in Excel, consider giving the repository a ⭐.
