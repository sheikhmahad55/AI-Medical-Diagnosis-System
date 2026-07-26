import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("dataset/diabetes.csv")

# Features and Target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "models/diabetes_model.pkl")

print("Model trained successfully!")