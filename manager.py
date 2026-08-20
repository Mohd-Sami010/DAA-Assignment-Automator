import subprocess;

fileName = input("Enter C++ exe file name with address: ")
dataSizes = eval(input("Enter data sizes to run (eg: 100, 1000 etc) as tuple: "))
runs_per_datasize = int(input("Num of times to run program per data size: "))
results = {}
averages = {}
outputs = []

# Experimenting
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
            if i == 0: 
                output_lines = output.splitlines()
                output_lines[0] += str(d)
                outputs.append(output_lines)
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

    print("Saving to CSV...")
    categories = list(averages[dataSizes[0]].keys())
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Size"] + categories)
        for size in dataSizes:
            row = [size]
            for category in categories:
                row.append(averages[size][category])
            writer.writerow(row)
def plot_graph():
    import matplotlib.pyplot as plt # type: ignore
    print("\nPlotting Graph...")
    categories = list(averages[dataSizes[0]].keys())
    for category in categories:
        ticks = []
        for size in dataSizes:
            ticks.append(averages[size][category])
        plt.plot(dataSizes, ticks, marker = "o", label = category)

    plt.xlabel("Data Size")    
    plt.ylabel("Average Time (ticks)")
    plt.title("Algorithm Performance")
    plt.legend()
    plt.grid()

    plt.savefig("performance.png")
    plt.close()
    print("Graph saved as performance.png")

print("\nRunning experiments on",fileName, "using data sizes: ", dataSizes, "\n")
run_experiment()
# Averages
for size in results:
    averages[size] = {}

    for category in results[size]:
        averages[size][category] = (
            sum(results[size][category])
            / len(results[size][category])
        )

print_result_table()
# save_to_csv()
plot_graph()

def make_assignment():
    # Making Assignment
    assignment_number = int(input("Enter Assignment number: "))
    assignment_name = input("Enter Assignment name: ")
    assignment_statement = input("Enter assignment statement (eg: Analyze Linear search..):")
    theory = input("Enter theory: ")
    time_complexity = input("Enter time complexity: ")
    space_complexity = input("Enter space complexity: ")
    complexity_analysis = input("Enter complexity analysis / conclusion: ")
    code = []
    code = ""
    with open(fileName[:-3]+"cpp", "r") as file:
        for line in file.readlines():
            code += line
    from pdf_generator import generate_pdf
    generate_pdf(
    assignment_number,
    assignment_name,
    assignment_statement,
    theory,
    time_complexity,
    space_complexity,
    complexity_analysis,
    code,
    outputs,
    averages,
    "performance.png"
)
make_assignment()
