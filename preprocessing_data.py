import pandas as pd
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# Load data hasil scraping
df = pd.read_csv("tokopedia_reviews.csv")

# Tampilkan contoh data
print("data dari csv: ")
print(df.head())

# Inisialisasi stopword remover & stemmer
stopword_factory = StopWordRemoverFactory()
stopword_remover = stopword_factory.create_stop_word_remover()
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

# Fungsi preprocessing
def clean_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Hapus karakter spesial
    text = stopword_remover.remove(text)  # Hapus stopword
    text = stemmer.stem(text)  # Stemming
    return text

# Terapkan ke data
df["clean_review"] = df["review"].astype(str).apply(clean_text)

slang_dict = {
    "yg": "yang",
    "bgt": "banget",
    "tdk": "tidak",
    "gk": "gak",
    "trs": "terus",
    "bnr2": "benar-benar",
    "kayu2": "kayu-kayu",
    "sukaaa": "sukaaa"
}

def normalize_slang(text):
    words = text.split()
    words = [slang_dict[word] if word in slang_dict else word for word in words]
    return " ".join(words)

df["clean_review"] = df["clean_review"].apply(normalize_slang)

df.to_csv("tokopedia_reviews_preprocessing.csv", index=False)
print("preprocessing selesai")