import pandas as pd
from docker_calc import Calculator  # Assuming your Calculator class is in calculator.py

# Create a Calculator instance (multiply by 3)
calc = Calculator(3, 1)

# List to store the times table results
results = []

# Generate the 3 times table
for i in range(1, 11):  # 1 to 10
    calc.b = i  # Set the multiplier to i
    results.append({
        'Number': i,
        'Result': calc.do_product()
    })

# Create a DataFrame
df = pd.DataFrame(results)

# Print the DataFrame (this will be shown in the container logs)
print(df)
