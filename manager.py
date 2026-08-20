import subprocess;
RUNS = 5

# dataSizes = (100, 1000, 10000, 100000, 1000000)
dataSizes = (100, 1000, 10000)

# fileName = input("Enter C++ exe file name with address: ")
fileName = "C++\\sortings.exe"
results = {}
for d in dataSizes:
    ticks_by_category = {}

    for i in range(RUNS):            
        cpp_result = subprocess.run([fileName], 
                                input= f"{d}\n",
                                capture_output= True, 
                                text= True)
        if cpp_result.returncode != 0:
            print("C++ program failed!")
            print(cpp_result.stderr)
            exit()
        output = cpp_result.stdout
        if i == 0: category = ""
        for line in output.splitlines():
            if line.startswith("Type: "):
                category = line.removeprefix("Type: ").strip()
                if i == 0: ticks_by_category[category] = []

            elif line.startswith("Ticks"):
                ticks = int(line.split(":")[1])
                ticks_by_category[category].append(ticks)

    results[d] = ticks_by_category

print("\n\tRESULTS (Size and Avgerage Ticks)\n")
print(f"{'Size':10}|", end="")
for i in results[dataSizes[0]]:
    print(f"{i:20}", end="|")
print()
for i in results:
    print(f"{str(i).ljust(10):10}", end= "|")

    for j in results[i]:
        average = sum(results[i][j])/ len(results[i][j])
        print(f"{str(average).ljust(20):20}", end="|")

    print()