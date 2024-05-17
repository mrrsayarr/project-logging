import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model_and_save():
    # Veri setini yükle
    data = pd.read_csv("../sets/data1234.csv", sep=";")

    # Veriyi işle
    data['EventID'] = pd.to_numeric(data['EventID'])

    # Bağımsız ve bağımlı değişkenleri ayır
    X = data[["EventID"]]
    y = data["Level"]

    # Karar ağacı sınıflandırıcı modelini oluştur ve eğit
    model = DecisionTreeClassifier(min_samples_leaf=6)
    model.fit(X, y)

    # Eğitilmiş modeli bir dosyaya kaydet
    joblib.dump(model, "trained_model.joblib")
    print("Model başarıyla kaydedildi.")


def load_and_predict(event_id):
    # Özellik isimleri olmayan bir DataFrame oluştur
    X = pd.DataFrame({"EventID": [event_id]})

    # Eğitilmiş modeli yükle
    model = joblib.load("trained_model.joblib")

    # EventID'ye göre verinin seviyesini tahmin et
    predicted_level = model.predict(X)

    return predicted_level[0]

    # Test verileri üzerinde doğruluğu değerlendir
    # y_pred = model.predict(X)
    # accuracy = accuracy_score(y, y_pred)

    # print("Model Doğruluğu:", accuracy)


# Eğitim adımını yorumdan çıkarın ve bir kez çalıştırın
# train_model_and_save()
# MODEL EGITIMI ICIN BURAYI ACMAN LAZIM, KAYDEDINCE KAPATABILIRSIN


