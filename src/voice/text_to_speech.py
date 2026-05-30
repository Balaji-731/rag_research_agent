import edge_tts
import asyncio
import tempfile

class TextToSpeech:

    async def generate(self,text):
        tmp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural"
        )
        await communicate.save(
            tmp_file.name
        )
        return tmp_file.name