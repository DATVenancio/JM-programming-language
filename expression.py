# Calculate (A+B)*(C/D) and check if result is greater or lower than 10
A = int(input("Enter value for A: "))
B = int(input("Enter value for B: "))
C = int(input("Enter value for C: "))
D = int(input("Enter value for D: "))
result: int = 0
result = (A + B) * (C / D)
if result > 10:
    print("The result " + str(result) + " is greater than 10" + "\n", end="")
else:
    print("The result " + str(result) + " is lower than or equal to 10" + "\n", end="")