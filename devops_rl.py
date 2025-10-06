import pandas as pd

# Load saved Q-table
q_table = pd.read_csv("q_table.csv", index_col=0)

# Best action (greedy policy) per state
policy = q_table.idxmax(axis=1)
print("Learned Policy:\n", policy)
