import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# load dataset
data = pd.read_csv("../dataset/training.csv")

# collect all symptoms
symptoms = set()

for col in data.columns[1:]:
    symptoms.update(data[col].dropna())

symptoms = list(symptoms)

# create symptom matrix
X = pd.DataFrame(0, index=data.index, columns=symptoms)

for i, row in data.iterrows():
    for col in data.columns[1:]:
        if pd.notna(row[col]):
            X.loc[i, row[col]] = 1

# disease column
y = data["Disease"]

# train Random Forest model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# save model
pickle.dump(model, open("model.pkl", "wb"))

# save symptoms
pickle.dump(symptoms, open("symptoms.pkl", "wb"))

print("Model trained successfully")