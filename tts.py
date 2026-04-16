import threading
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


ELEVENLABS_API_KEY = "ADD API"
elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_stream(text: str) -> IO[bytes]:
    # Perform the text-to-speech conversion
    response = elevenlabs.text_to_speech.stream(
        voice_id="sIkyg34IaM6WNYMeZdty", 
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_flash_v2_5",
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream



from io import BytesIO

def play_audio_task(data):
    pygame.mixer.init()
    data.seek(0)
    pygame.mixer.music.load(data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


