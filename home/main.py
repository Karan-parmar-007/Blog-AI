import pyttsx3

def read_text(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties before adding the text
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    # Add the text to be spoken
    engine.say(text)

    # Block until the text is spoken
    engine.runAndWait()

# Example text to be read aloud
text_to_read = "Hello, this is an example text to be read aloud."

# Call the function to read the text
read_text(text_to_read)
