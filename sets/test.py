
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Load data from CSV file (assuming the column name is "Level" without a space)
data = pd.read_csv("data1234.csv")

# Split the combined column into "Level" and "EventID"
data[["Level", "EventID"]] = data["Level;EventID"].str.split(";", expand=True)

# Separate features (X) and target variable (y)
X = data.drop("Level", axis=1)
y = data["Level"]

# Verileri eğitim ve test kümelerine bölün
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Özellik ölçeklendirme (gerekirse)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 2. Model Seçimi ve Çapraz Doğrulama

# Değerlendirilecek modellerin bir listesini oluşturun
models = [
    LogisticRegression(random_state=42),
    RandomForestClassifier(random_state=42),
    SVC(random_state=42)
]

# Her model için çapraz doğrulama gerçekleştirin
for model in models:
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    print(f"Model: {model.__class__.__name__}")
    print(f"Çapraz doğrulama skorları: {scores}")
    print(f"Ortalama doğruluk: {np.mean(scores)}")

# 3. Model Değerlendirme ve Geliştirme

# En yüksek ortalama doğruluğa sahip modeli belirlemek için çapraz doğrulama sonuçlarını analiz edin.
# Seçilen modelin performansını daha da optimize etmek için hiperparametre ayarlamayı düşünün.
# Doğruluk hala yetersizse, alternatif modelleri veya özellik mühendisliği tekniklerini keşfedin.