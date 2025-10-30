import requests

# Replace with your actual Deepgram API key
DEEPGRAM_API_KEY = "b8919e8cbe5181cfc4e899b9a8c64bae99cf39f3"

# Path to your local audio file
audio_file_path = "sample.wav"

# Deepgram API endpoint with diarization enabled
url = "https://api.deepgram.com/v1/listen?diarize=true"

# Open the audio file in binary mode
with open(audio_file_path, "rb") as audio_file:
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }

    print("Uploading audio to Deepgram...")
    response = requests.post(url, headers=headers, data=audio_file)

# Handle response
if response.status_code == 200:
    result = response.json()
    print("✅ Transcription & Diarization Result:")
    print("Res", result)
else:
    print(f"❌ Error {response.status_code}: {response.text}")
