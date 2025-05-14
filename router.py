from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
pathway1 = "+12494965822"
pathway2 = ""  # Will add later
pathway3 = ""  # Will add later


@app.route("/ivr", methods=['GET', 'POST'])
def ivr():
    response = VoiceResponse()

    # Initial greeting
    response.say("Press 1 to sell your vehicle, Press 2 for unwanted vehicle removal, Press 3 for used auto parts.")

    # Gather user input
    gather = response.gather(num_digits=1, action="/handle_input", method="POST")
    gather.say("Please enter your choice.")

    return str(response)


@app.route("/handle_input", methods=['GET', 'POST'])
def handle_input():
    response = VoiceResponse()
    digit_pressed = request.values.get('Digits', None)

    if digit_pressed == '1':
        response.say("Connecting you to the vehicle sales department.")
        response.dial(pathway1)
    elif digit_pressed == '2':
        response.say("Connecting you to the unwanted vehicle removal department.")
        response.dial(pathway2)
    elif digit_pressed == '3':
        response.say("Connecting you to the used auto parts department.")
        response.dial(pathway3)
    else:
        response.say("Invalid choice. I will repeat the message.")
        response.redirect("/ivr")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)

# COME BACK TO EDIT: INSTRUCTIONS HERE https://chatgpt.com/share/68211c10-70a0-8000-b8e4-e62c0dfce283

