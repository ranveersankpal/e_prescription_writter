import os
from faster_whisper import WhisperModel
import tempfile

model = WhisperModel("small", device="cpu", compute_type="int8")

async def extract_text_from_audio(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    segments, info = model.transcribe(temp_path)

    text = ""
    for seg in segments:
        text += seg.text + " "

    os.remove(temp_path)
    return text.strip()
