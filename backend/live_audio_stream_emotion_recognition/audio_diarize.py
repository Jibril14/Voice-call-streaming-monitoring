import whisperx
# from whisperx.diarize import DiarizationPipeline

import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger("whisperx").setLevel(logging.ERROR)



def audio_diarize(audio_file: str = "sample.wav"):
    device = "cpu"
    batch_size = 16 # reduce if low on GPU mem
    compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("base", device, compute_type=compute_type)

    # save model to local path (optional)
    model_dir = "/models_folder"
    model = whisperx.load_model("base", device, compute_type=compute_type, download_root=model_dir)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    # print("Transcript Result:", result)
    # print("Transcript Segment:", result["segments"]) 
    segments = result["segments"]
    result = " ".join(segment["text"].strip() for segment in segments if "text" in segment)
    return result

if __name__ == "__main__":
    result = audio_diarize()
    print(result)