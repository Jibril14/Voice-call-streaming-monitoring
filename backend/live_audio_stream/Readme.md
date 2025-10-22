# A mini server and client to test live audio stream

## Convert MP3 file to .wav
- ffmpeg -i yourfile.mp3 -ar 16000 -ac 1 -sample_fmt s16 sample.wav

# run
- python live_audio_stream_client.py
- python live_audio_stream_server.py

python audio_stream_realtime_classify.py