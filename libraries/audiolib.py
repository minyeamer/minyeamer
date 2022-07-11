import speech_recognition as sr
from typing import Optional


def speech_recognition(language: Optional[str]='ko-KR', ret: Optional[bool]=False):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say Something')
        speech = r.listen(source)

    try:
        text = r.recognize_google(speech, language=language)
        print('Your speech thinks like\n ' + text)
    except sr.UnknownValueError:
        print('Your speech can not understand')
    except sr.RequestError as e:
        print('Request Error!; {0}'.format(e))

    if ret:
        return text


def audio_recognition(filename: str, language: Optional[str]='ko-KR', ret: Optional[bool]=False):
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data, language=language)
        print('Your audio thinks like\n ' + text)
    except:
        print('Your audio can not understand')

    if ret:
        return text


def playsound(filename: str):
    from playsound import playsound
    playsound(filename)
