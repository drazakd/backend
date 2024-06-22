import whisper
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator
from gtts import gTTS
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


@csrf_exempt
def translate_video(request):
    if request.method == 'POST':
        file = request.FILES['video']
        source_lang = request.POST.get('source_lang', 'fr')
        dest_lang = request.POST.get('dest_lang', 'en')
        video_path = 'video.mp4'

        with open(video_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Extraction de l'audio
        video = VideoFileClip(video_path)
        audio_path = 'audio.wav'
        video.audio.write_audiofile(audio_path)
        progress = 20
        time.sleep(1)  # Simulating a delay for demonstration purposes

        # Transcription
        text = transcribe_audio(audio_path)
        progress = 50
        time.sleep(1)  # Simulating a delay for demonstration purposes

        # Traduction
        translator = Translator()
        translated_text = translator.translate(text, src=source_lang, dest=dest_lang).text
        progress = 70
        time.sleep(1)  # Simulating a delay for demonstration purposes

        # Synthèse vocale
        tts = gTTS(translated_text, lang=dest_lang)
        translated_audio_path = 'translated_audio.mp3'
        tts.save(translated_audio_path)
        progress = 90
        time.sleep(1)  # Simulating a delay for demonstration purposes

        # Synchronisation et montage
        translated_audio = AudioFileClip(translated_audio_path)
        final_video = video.set_audio(translated_audio)
        final_video_path = 'translated_video.mp4'
        final_video.write_videofile(final_video_path)
        progress = 100
        time.sleep(1)  # Simulating a delay for demonstration purposes

        # Suppression des fichiers temporaires
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(translated_audio_path)

        # Retourner la vidéo traduite
        with open(final_video_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="video/mp4")
            response['Content-Disposition'] = 'attachment; filename=translated_video.mp4'

        os.remove(final_video_path)

        return response

    return JsonResponse({'error': 'Invalid request method.'})




## le code passe mais trop simple donc je vais ajouter d'autres options
# import whisper
# from moviepy.editor import VideoFileClip, AudioFileClip
# from googletrans import Translator
# from gtts import gTTS
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import os
#
# # Create your views here.
# def transcribe_audio(audio_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path)
#     return result["text"]
#
#
# @csrf_exempt
# def translate_video(request):
#     if request.method == 'POST':
#         file = request.FILES['video']
#         video_path = 'video.mp4'
#
#         with open(video_path, 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
#
#         # Extraction de l'audio
#         video = VideoFileClip(video_path)
#         audio_path = 'audio.wav'
#         video.audio.write_audiofile(audio_path)
#
#         # Transcription
#         text = transcribe_audio(audio_path)
#
#         # Traduction
#         translator = Translator()
#         translated_text = translator.translate(text, src='en', dest='fr').text
#
#         # Synthèse vocale
#         tts = gTTS(translated_text, lang='fr')
#         translated_audio_path = 'translated_audio.mp3'
#         tts.save(translated_audio_path)
#
#         # Synchronisation et montage
#         translated_audio = AudioFileClip(translated_audio_path)
#         final_video = video.set_audio(translated_audio)
#         final_video_path = 'translated_video.mp4'
#         final_video.write_videofile(final_video_path)
#
#         # Suppression des fichiers temporaires
#         os.remove(video_path)
#         os.remove(audio_path)
#         os.remove(translated_audio_path)
#
#         # Retourner la vidéo traduite
#         with open(final_video_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type="video/mp4")
#             response['Content-Disposition'] = 'attachment; filename=translated_video.mp4'
#
#         os.remove(final_video_path)
#
#         return response
#
#     return JsonResponse({'error': 'Invalid request method.'})




# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from moviepy.editor import VideoFileClip
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import os
#
# # Create your views here.
# @csrf_exempt
# def translate_video(request):
#     if request.method == 'POST':
#         file = request.FILES['video']
#         video_path = 'video.mp4'
#
#         with open(video_path, 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)
#
#         # Extraction de l'audio
#         video = VideoFileClip(video_path)
#         audio_path = 'audio.wav'
#         video.audio.write_audiofile(audio_path)
#
#         # Transcription
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_path) as source:
#             audio = recognizer.record(source)
#             text = recognizer.recognize_google(audio, language="fr-FR")
#
#         # Traduction
#         translator = Translator()
#         translated_text = translator.translate(text, src='fr', dest='en').text
#
#         # Synthèse vocale
#         tts = gTTS(translated_text, lang='en')
#         translated_audio_path = 'translated_audio.mp3'
#         tts.save(translated_audio_path)
#
#         # Synchronisation et montage
#         translated_audio = VideoFileClip(translated_audio_path)
#         final_video = video.set_audio(translated_audio)
#         final_video_path = 'translated_video.mp4'
#         final_video.write_videofile(final_video_path)
#
#         # Suppression des fichiers temporaires
#         os.remove(video_path)
#         os.remove(audio_path)
#         os.remove(translated_audio_path)
#
#         # Retourner la vidéo traduite
#         with open(final_video_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type="video/mp4")
#             response['Content-Disposition'] = 'attachment; filename=translated_video.mp4'
#
#         os.remove(final_video_path)
#
#         return response
#
#     return JsonResponse({'error': 'Invalid request method.'})
#
#
