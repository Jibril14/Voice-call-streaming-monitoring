import torch
from speechbrain.inference.interfaces import foreign_class

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="speechbrain")
warnings.filterwarnings("ignore", module="torchaudio")
warnings.filterwarnings("ignore", message=".*torchaudio.*deprecated.*")

# Load model and download model
classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier"
    # run_opts={"device": "cuda"}  # I install Pytouch cpu not GPU
)


# Run classification
out_prob, score, index, text_lab = classifier.classify_file("sample.wav")

print("Predicted label:", text_lab)
print(f"\nPredicted Emotion: {text_lab[0]} (Confidence: {score.item():.3f})")

# Print All probabilities per class
labels = classifier.hparams.label_encoder.decode_torch(torch.arange(out_prob.shape[-1]))
probs = out_prob.squeeze().tolist()

print("Emotion Probabilities:")
for label, prob in zip(labels, probs):
    print(f"{label:<10}: {prob:.3f}")



# import torch
# import librosa
# from datasets import load_dataset
# from transformers import HubertForSequenceClassification, Wav2Vec2FeatureExtractor

# def map_to_array(example):
#     speech, _ = librosa.load(example["file"], sr=16000, mono=True)
#     example["speech"] = speech
#     return example

# # load a demo dataset and read audio files
# dataset = load_dataset("anton-l/superb_demo", "er", split="session1")
# dataset = dataset.map(map_to_array)

# model = HubertForSequenceClassification.from_pretrained("superb/hubert-base-superb-er")
# feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("superb/hubert-base-superb-er")

# # compute attention masks and normalize the waveform if needed
# inputs = feature_extractor(dataset[:4]["speech"], sampling_rate=16000, padding=True, return_tensors="pt")

# logits = model(**inputs).logits
# predicted_ids = torch.argmax(logits, dim=-1)
# labels = [model.config.id2label[_id] for _id in predicted_ids.tolist()]


