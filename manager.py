import subprocess;
dataSizes = (100, 1000, 10000, 100000)
fileName = input("Enter C++ file name with address: ")
for d in dataSizes:
    result = subprocess.run([fileName], 
                            input= f"{d}\n",
                            capture_output= True, 
                            text= True)
    print(result.stdout.splitlines()[1])