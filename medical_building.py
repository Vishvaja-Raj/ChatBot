import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 1: Load and Preprocess the Data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df['text'].tolist(), df['label'].tolist()

file_path = 'medical_data.csv'  # Replace with your CSV file path
texts, labels = load_data(file_path)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

# Step 2: Initialize and Fit Vectorizer
vectorizer = CountVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# Train the Random Forest classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_vectors, y_train)

# Evaluate the model
y_pred = classifier.predict(X_test_vectors)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=['Non-Medical', 'Medical'])

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# Step 3: Save the Model and Vectorizer
model_file = 'random_forest_model.pkl'
vectorizer_file = 'count_vectorizer.pkl'

joblib.dump(classifier, model_file)
joblib.dump(vectorizer, vectorizer_file)

print(f"Model saved as {model_file}")
print(f"Vectorizer saved as {vectorizer_file}")
