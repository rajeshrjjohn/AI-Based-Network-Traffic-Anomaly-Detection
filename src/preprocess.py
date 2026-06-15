import pandas as pd

normal = pd.read_csv("data/processed/traffic_features.csv")
attack = pd.read_csv("data/processed/attack_features.csv")

normal["label"] = 0
attack["label"] = 1

dataset = pd.concat([normal,attack], ignore_index=True)

dataset.to_csv("data/processed/final_dataset.csv",index=False)

print(dataset.head())
print("\nDataset Shape:", dataset.shape)
print("\nDataset Saved Successfully!")

