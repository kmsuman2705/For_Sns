import boto3
import speech_recognition as sr

# Initialize the SNS client
sns_client = boto3.client('sns', region_name='ap-south-1')

# ARNs
arn_police = 'arn:aws:sns:ap-10:ibm'
arn_neighbors = 'arn:aws:sns:'

# Initialize recognizer
recognizer = sr.Recognizer()

def send_sns_alert(arn, message):
    try:
        sns_client.publish(
            TopicArn=arn,
            Message=message,
            Subject='Emergency Alert'
        )
        print(f"Alert sent to ARN: {arn}")
    except Exception as e:
        print(f"Error sending SNS alert: {e}")

def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for voice commands...")
        while True:
            try:
                # Adjust for ambient noise and listen
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                # Recognize speech
                command = recognizer.recognize_google(audio).lower()

                # Check for specific keywords to trigger SNS alerts
                if 'police' in command:
                    send_sns_alert(arn_police, 'Alert: Assistance required from the police.')
                elif 'help' in command or 'neighbor' in command:
                    send_sns_alert(arn_neighbors, 'Alert: Assistance required from neighbors.')
                else:
                    print(f"Unrecognized command: {command}")

            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")

# Run the voice command listener in a separate thread
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()
