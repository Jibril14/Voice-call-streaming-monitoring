import torch
from speechbrain.inference.interfaces import foreign_class

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="speechbrain")
warnings.filterwarnings("ignore", module="torchaudio")
warnings.filterwarnings("ignore", message=".*torchaudio.*deprecated.*")


def classify_emotion(audio_path: str):
    """
    Classify emotion from a given audio file using SpeechBrain's Wav2Vec2 IEMOCAP model.

    Args:
        audio_path (str): Path to the .wav audio file.
    """

    classifier = foreign_class(
        source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier",
        run_opts={"device": "cpu"}  # Use CPU since I didn't install GPU Pytorch 
    )

    # classification
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)

    labels = classifier.hparams.label_encoder.decode_torch(torch.arange(out_prob.shape[-1]))
    probs = out_prob.squeeze().tolist()
    emotion_probs = {label: float(prob) for label, prob in zip(labels, probs)}


    # Return structured data
    return {
        "predicted_label": text_lab[0],
        "confidence": float(score.item()),
        "probabilities": emotion_probs
    }


if __name__ == "__main__":
    print("Working")
    result_dict = classify_emotion("sample.wav")
    # Print results
    print(f"\nPredicted Emotion: {result_dict['predicted_label']} (Confidence: {result_dict['confidence']})")
    print("\nEmotion Probabilities:")
    for label, prob in result_dict['probabilities'].items():
        print(f"{label:<10}: {prob:.3f}")


