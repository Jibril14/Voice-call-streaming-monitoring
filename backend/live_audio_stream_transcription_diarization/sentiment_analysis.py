from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from scipy.special import expit  # sigmoid for multi-label

# MODEL = "SamLowe/roberta-base-go_emotions"
MODEL = "michellejieli/emotion_text_classifier"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


def get_emotions(text: str, top_n: int = 1):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**encoded).logits[0].cpu().numpy()
    probs = expit(logits) 
    # retrieve labels
    label_mapping = model.config.id2label  # maps index to emotion name
    
    # Sort by descending probability
    sorted_idx = np.argsort(probs)[::-1]
    results = {}
    for idx in sorted_idx[:top_n]:
        label = label_mapping[idx]
        prob = float(probs[idx])
        results[label] = prob

    return results

if __name__ == "__main__":
    # Example
    text = " of your Vallowabally time. I'm very busy by calling on Sunday. I am not really happy"
    print(get_emotions(text, top_n=1))
