from src.voice.speech_to_text import SpeechToText
from src.voice.text_to_speech import TextToSpeech

class VoicePipeline:
    def __init__(self):
        self.stt=SpeechToText()
        self.tts=TextToSpeech()

    def audio_to_query(self,audio_path):
        return self.stt.transcribe(audio_path)
    
    def speak_response(self,response):
        self.tts.speak(response)