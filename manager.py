import subprocess;

# dataSizes = (100, 1000, 10000, 100000, 1000000)
dataSizes = (100, 1000, 10000, 30000)

# fileName = input("Enter C++ exe file name with address: ")
fileName = "C++\\sortings.exe"
runs_per_datasize = int(input("Num of times to run program per data size: "))
results = {}
averages = {}

def print_result_table():
    print("\n\tRESULTS (Data Size and Average Ticks)\n")
    header = f"{'Size':10}|"
    for i in results[dataSizes[0]]:
        header += f"{i:20}|"
    print(header, "\n", "-" * len(header), sep="")
    for i in results:
        print(f"{str(i).ljust(10):10}", end= "|")

        for j in results[i]:
            average = sum(results[i][j])/ len(results[i][j])
            print(f"{str(average).ljust(20):20}", end="|")

        print()
def run_experiment():
    for d in dataSizes:
        ticks_by_category = {}

        print("Running on Data size: ", d)
        for i in range(runs_per_datasize):            
            print(f"Running Experiment-{i+1}...")
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
        print()
        results[d] = ticks_by_category
def save_to_csv():
    import csv
    categories = list(averages[dataSizes[0]].keys())
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Size"] + categories)
        for size in dataSizes:
            row = [size]
            for category in categories:
                row.append(averages[size][category])
            writer.writerow(row)

print("\nRunning experiments on",fileName, "using data sizes: ", dataSizes, "\n")
run_experiment()
print_result_table()

# Averages
for size in results:
    averages[size] = {}

    for category in results[size]:
        averages[size][category] = (
            sum(results[size][category])
            / len(results[size][category])
        )
save_to_csv()