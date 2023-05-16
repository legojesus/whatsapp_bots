# Whatsapp bots in Python with Twilio

This repo is a WIP and currently contains the following Whatsapp bots: 
- voice_to_text.py - A whatsapp bot that accepts voice messages and sends the user back a text message with the contents of the voice message.
- chatgpt.py - A ChatGPT Whatsapp bot that allows you to text directly to ChatGPT and get replies in Whatsapp. 

Integration with Twilio (https://console.twilio.com/) is required in order for this setup to work. Tested with Twilio's trial account using a Whatsapp sandbox, and a Google Cloud compute engine virtual machine that runs the python app. 


Setup is a bit complex as it requires installing additional components on the vm, enabling APIs in OpenAI and/or in GCP (using a service account with a credentials.json file), so a thorough walkthrough will be added in the future. 

The overall flow is: 
User's Whatsapp -> Twilio phone number (provided with trial account) -> Virtual machine's IP with Flask's URL (e.g. http://123.123.123.123/bot) -> User's text/voice into Python code -> Google Speech or OpenAI API -> answer from API into Python code -> Twilio reply text message -> User's Whatsapp. 



### TODO:
- Add error handling
- Add WSGI server
- Better documentation
