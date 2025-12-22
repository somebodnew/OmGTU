import math
from collections import Counter

def process_text(text):
    text = text.lower()
    text = ''.join([ch for ch in text if ch.isalpha() and 'а' <= ch <= 'я'])
    return text

def kgrams(text, k):
    return [text[i:i+k] for i in range(len(text)-k+1)]

def entropy_k(text, k):
    grams = kgrams(text, k)
    total = len(grams)
    freq = Counter(grams)
    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def main():
    original_text = """Когда вода всемирного потопа\nВернулась вновь в границы берегов\nИз пены уходящего потока\nНа берег тихо выбралась любовь\nИ растворилась в воздухе до срока\nА срока было сорок сороков."""  
    text = process_text(original_text)
    print(" Открытый текст (ОТ)\n\n",original_text,"\n\n",sep='')
    print(" Закрытый текст (ЗТ)\n\n",text,"Изначальный текст (ОТ)","\n",sep='')
    results = []
    print("\n", " Результат","\n",sep='')
    for k in range(1, 6):
        Hk = entropy_k(text, k)
        results.append((k, Hk/k))
        print(f"k={k}: H_k/k = {Hk/k:.3f}")
    
    
    
main()
