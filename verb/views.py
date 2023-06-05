import hashlib
import os
import re

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.text import slugify
from gtts import gTTS

from excelUploader import settings
from verb.models import Verb, VerbAudio


def clean_sentence(sentence):
    # Remove commas and numbers
    cleaned_sentence = re.sub(r'[,0-9]', '', sentence)
    # Remove leading/trailing whitespace and dots
    cleaned_sentence = cleaned_sentence.strip().rstrip('.')
    return cleaned_sentence


def search_sentences(request):
    if request.method == 'POST':
        words = request.POST.getlist('words[]')
        verb_id = request.POST.get('verb_id')
        verb_ins = Verb.objects.get(id=verb_id)  # Retrieve the Verb instance

        file_path = 'sentences.xlsx'
        matching_sentences, _ = search_sentences_helper(words, file_path)

        if matching_sentences:
            create_audio_from_sentences(matching_sentences, verb_id)

        sentences_with_audio = []

        for index, sentence in enumerate(matching_sentences, start=1):
            audio_files = verb_ins.audio_files.filter(audio__isnull=False)

            if audio_files.exists() and audio_files.count() >= index:
                audio_file = audio_files[index - 1]
                audio_url = audio_file.audio.url
                audio_id = audio_file.id
            else:
                audio_url = None
                audio_id = None

            sentence_data = {
                'index': index,
                'sentence': sentence,
                'audio_file': audio_url,
                'audio_id': audio_id,
            }
            sentences_with_audio.append(sentence_data)

        response = {
            'sentences': sentences_with_audio,
        }

        return JsonResponse(response)
    else:
        return HttpResponseBadRequest("Invalid request method")


def search_sentences_helper(words, file_path):
    sentences = []
    related_sentences = []

    file_extension = os.path.splitext(file_path)[1]  # Get the file extension

    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                sentence = line.split(',')[0]  # Extract the sentence before the comma
                cleaned_sentence = clean_sentence(sentence)
                for word in words:
                    if re.search(rf"\b{re.escape(word)}\b", cleaned_sentence):
                        sentences.append(cleaned_sentence)
                    elif re.search(rf"\b{re.escape(word)}\b", cleaned_sentence, re.IGNORECASE):
                        related_sentences.append(cleaned_sentence)

    elif file_extension == '.xlsx':
        df = pd.read_excel(file_path)
        sentences_column = df['Sentences']
        for sentence in sentences_column:
            sentence = str(sentence)
            cleaned_sentence = clean_sentence(sentence)
            for word in words:
                if re.search(rf"\b{re.escape(word)}\b", cleaned_sentence):
                    sentences.append(cleaned_sentence)
                elif re.search(rf"\b{re.escape(word)}\b", cleaned_sentence, re.IGNORECASE):
                    related_sentences.append(cleaned_sentence)
    else:
        raise ValueError("Invalid file format. Only text (.txt) and Excel (.xlsx) files are supported.")

    if len(sentences) == 0 and len(related_sentences) > 0:
        # If no exact matches found, return related sentences as the final result
        sentences = related_sentences
        related_sentences = []

    return sentences, related_sentences


def create_audio_from_sentences_backup(sentences, verb_id):
    output_dir = 'audio'  # Define the output directory relative to the media folder
    media_dir = settings.MEDIA_ROOT  # Get the media directory from Django settings
    output_path = os.path.join(media_dir, output_dir)  # Output directory path in the media folder

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    verb_ins = Verb.objects.get(id=verb_id)  # Retrieve the Verb instance outside the loop
    print(f'Verb infinitive: {verb_ins.infinitive}')

    verb_audios = []  # List to hold the VerbAudio instances

    if sentences:
        for i, sentence in enumerate(sentences):
            # Generate a unique identifier for the sentence
            identifier = hashlib.md5(sentence.encode('utf-8')).hexdigest()

            # Generate the filename based on the sentence name and the identifier
            filename = f'{slugify(sentence)}_{identifier}_{i + 1}.mp3'
            audio_file = os.path.join(output_path, filename)

            # Check if an audio file with the same identifier already exists
            existing_audio = VerbAudio.objects.filter(verb=verb_ins, audio__contains=identifier).first()
            if existing_audio:
                verb_audios.append(existing_audio)
                print(f'Audio for sentence "{sentence}" already exists')
                continue

            # Generate the audio file
            tts = gTTS(text=sentence, lang='pt-br')
            tts.save(audio_file)

            # Validate the saved audio file
            if os.path.getsize(audio_file) == 0:
                # Error during audio generation, delete the file
                os.remove(audio_file)
                print(f'Error generating audio for sentence {i + 1}')
            else:
                print(f'Saved audio for sentence {i + 1}')

            # Create the VerbAudio instance and associate it with the Verb instance
            verb_audio = VerbAudio(verb=verb_ins)

            with open(audio_file, 'rb') as file:
                verb_audio.audio.save(filename, File(file), save=True)

            verb_audio.save()  # Save the individual VerbAudio instance

            verb_audios.append(verb_audio)

            # Delete the temporary audio file
            os.remove(audio_file)

    else:
        print("No sentences provided")

    print(sentences)  # Print the sentences list for debugging purposes


def create_audio_from_sentences(sentences, verb_id):
    output_dir = 'audio'  # Define the output directory relative to the media folder
    media_dir = settings.MEDIA_ROOT  # Get the media directory from Django settings
    output_path = os.path.join(media_dir, output_dir)  # Output directory path in the media folder

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    verb_ins = Verb.objects.get(id=verb_id)  # Retrieve the Verb instance outside the loop
    print(f'Verb infinitive: {verb_ins.infinitive}')

    verb_audios = []  # List to hold the VerbAudio instances
    existing_audio_files = set(VerbAudio.objects.filter(verb=verb_ins).values_list('audio', flat=True))

    if sentences:
        for i, sentence in enumerate(sentences):
            # Generate a unique identifier for the sentence
            identifier = hashlib.md5(sentence.encode('utf-8')).hexdigest()

            # Generate the filename based on the sentence name and the identifier
            filename = f'{slugify(sentence)}_{identifier}_{i + 1}.mp3'

            if filename in existing_audio_files:
                print(f'Audio for sentence "{sentence}" already exists')
                # Retrieve the existing VerbAudio instance based on the filename
                existing_verb_audio = VerbAudio.objects.get(verb=verb_ins, audio=filename)
                verb_audios.append(existing_verb_audio)
            else:
                existing_audio_files.add(filename)

                audio_file = os.path.join(output_path, filename)
                tts = gTTS(text=sentence, lang='pt-br')
                tts.save(audio_file)

                if os.path.getsize(audio_file) == 0:
                    os.remove(audio_file)
                    print(f'Error generating audio for sentence {i + 1}')
                else:
                    print(f'Saved audio for sentence {i + 1}')

                # Create the VerbAudio instance and associate it with the Verb instance
                verb_audio = VerbAudio(verb=verb_ins, audio=filename)

                with open(audio_file, 'rb') as file:
                    verb_audio.audio.save(filename, File(file), save=False)

                verb_audios.append(verb_audio)

                # Delete the temporary audio file
                os.remove(audio_file)

        if verb_audios:
            VerbAudio.objects.bulk_create(verb_audios)  # Bulk create the VerbAudio instances

    else:
        print("No sentences provided")

    print(sentences)  # Print the sentences list for debugging purposes


def index(request):
    verbs = Verb.objects.select_related('category').prefetch_related('audio_files')

    present_count = 0
    verb_list = []

    for verb in verbs:
        if verb.category.name == 'Presente':
            present_count += 1

        verb_data = {
            'verb_id': verb.id,
            'infinitive': verb.infinitive,
            'english_translation': verb.english_translation,
            'danish_translation': verb.danish_translation,
            'eu': verb.eu,
            'voce_ele_ela': verb.voce_ele_ela,
            'nos': verb.nos,
            'voces_eles_elas': verb.voces_eles_elas,
            'category': verb.category.name,
            'audio_files': verb.audio_files.all()  # Retrieve all audio files for the verb
        }

        verb_list.append(verb_data)

    total_count = len(verb_list)

    context = {
        'verbs': verb_list,
        'present_count': present_count,
        'total_count': total_count,
    }

    return render(request, 'index.html', context)
