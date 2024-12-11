import gradio as gr
import assemblyai as aai
from translate import Translator
import uuid
from pathlib import Path
from gtts import gTTS

def voice_to_voice(audio_file):
    
    #transcribe audio
    transcription_response = audio_transcription(audio_file)

    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text

    en_translation, es_translation, tr_translation, ja_translation = text_translation(text)

    en_audi_path = text_to_speech(en_translation)
    es_audi_path = text_to_speech(es_translation)
    tr_audi_path = text_to_speech(tr_translation)
    ja_audi_path = text_to_speech(ja_translation)

    en_path = Path(en_audi_path)
    es_path = Path(es_audi_path)
    tr_path = Path(tr_audi_path)
    ja_path = Path(ja_audi_path)

    return en_path, es_path, tr_path, ja_path


def audio_transcription(audio_file):

    aai.settings.api_key = "7abb36d97d7a4ceb987518beb11cc4f0"

    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)

    return transcription

def text_translation(text):
    
    translator_en = Translator(from_lang="fr", to_lang="en")
    en_text = translator_en.translate(text)
    
    translator_es = Translator(from_lang="fr", to_lang="es")
    es_text = translator_es.translate(text)

    translator_tr = Translator(from_lang="fr", to_lang="tr")
    tr_text = translator_tr.translate(text)

    translator_ja = Translator(from_lang="fr", to_lang="ja")
    ja_text = translator_ja.translate(text)

    return en_text, es_text, tr_text, ja_text

# def text_to_speech(text):

#     client = ElevenLabs(
#         api_key= "<your-elevenlabs-api-key>",
#     )

#     # Calling the text_to_speech conversion API with detailed parameters
#     response = client.text_to_speech.convert(
#         voice_id="<your-voice-id>", #clone your voice on elevenlabs dashboard and copy the id
#         optimize_streaming_latency="0",
#         output_format="mp3_22050_32",
#         text=text,
#         model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
#         voice_settings=VoiceSettings(
#             stability=0.5,
#             similarity_boost=0.8,
#             style=0.5,
#             use_speaker_boost=True,
#         ),
#     )

#     # Generating a unique file name for the output MP3 file
#     save_file_path = f"{uuid.uuid4()}.mp3"

#     # Writing the audio to a file
#     with open(save_file_path, "wb") as f:
#         for chunk in response:
#             if chunk:
#                 f.write(chunk)

#     print(f"{save_file_path}: A new audio file was saved successfully!")

#     # Return the path of the saved audio file
#     return save_file_path


def text_to_speech(text, lang="en"):
    # On utilise gTTS pour générer de l'audio
    tts = gTTS(text=text, lang=lang)
    save_file_path = f"{uuid.uuid4()}.mp3"
    tts.save(save_file_path)
    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path



audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)

demo = gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[gr.Audio(label="English"), gr.Audio(label="Spanish"), gr.Audio(label="Turkish"), gr.Audio(label="Japanese")]
)

if __name__ == "__main__":
    demo.launch()