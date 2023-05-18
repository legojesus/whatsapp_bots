from flask import Flask, request
from twilio.rest import Client
import requests
import os
from google.cloud import speech


# TWILIO setup and function (https://console.twilio.com/)

account_sid = 'xxxxxx'  # Replace with your Twilio account SID
auth_token = 'xxxxxx'   # Replace with your Twilio Auth Token
client = Client(account_sid, auth_token)

def sendMessage(body_mess, phone_number):
    print("BODY MESSAGE " + body_mess)
    message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=body_mess,
                                to="whatsapp:+" + phone_number
                            )



# Google Speech Recognition API

def speech_to_text(config: speech.RecognitionConfig, audio: speech.RecognitionAudio) -> speech.RecognizeResponse:

    client = speech.SpeechClient().from_service_account_json(filename="/home/xxxx/whatsapp_bots/creds.json") # Replace with the path to your GCP service account credentials file

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)
    return response


def print_response(response: speech.RecognizeResponse):
    results = []
    for result in response.results:
        results.append(print_result(result))
    return results[0]



def print_result(result: speech.SpeechRecognitionResult):
    alternative = result.alternatives[0]
    print("-" * 20)
    print(f"First alternative of result: {alternative}")
    print(f"Transcript: {alternative.transcript}")
    return alternative.transcript


config = speech.RecognitionConfig(
    language_code="en",                 # Main language to transcribe to.
    alternative_language_codes=["he"],  # List of other languages to try and transcribe. Up to 4 supported, but more languages = less accurate transcription.
    enable_automatic_punctuation = True
)

# FLASK app setup and init

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():

    phone_number = request.values['WaId']       # Values found from Twilio error logs of messages
    voice_message = request.values['MediaUrl0']

    if voice_message:
        # Get the voice message file
        file = requests.get(voice_message, allow_redirects=True)
        open("message.opus", "wb").write(file.content)

        # Convert the file to .wav for Google speech recognition. Requires ffmpeg installed on the operating system.
        os.system(f'ffmpeg -i "./message.opus" -vn "./message.wav"')

        with open("message.wav", "rb") as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)

        response = speech_to_text(config, audio)
        text = str(print_response(response))

        # Delete the files as they are no longer necessary
        os.remove("./message.opus")
        os.remove("./message.wav")

        # Send a Whatsapp message back with the text of the voice message
        sendMessage(text, phone_number)

        return "Done"


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)