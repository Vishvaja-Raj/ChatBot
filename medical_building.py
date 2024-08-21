import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Load your CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df['text'], df['label']

file_path = 'medical_data.csv'  # Replace with your CSV file path
texts, labels = load_data(file_path)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Initialize Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

# Evaluate the model
pred_labels = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, pred_labels)
report = classification_report(y_test, pred_labels, target_names=['Non-Medical', 'Medical'])

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# Save the model and vectorizer
os.makedirs('model_files', exist_ok=True)
joblib.dump(model, 'model_files/medical_model.pkl')
joblib.dump(vectorizer, 'model_files/vectorizer.pkl')
print("Model and vectorizer saved to model_files/")
