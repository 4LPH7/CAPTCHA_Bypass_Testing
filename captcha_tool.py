import cv2
import pytesseract
import numpy as np
import speech_recognition as sr

def solve_text_captcha(image_path):
    """
    Solves a text-based CAPTCHA image using OCR.
    
    Parameters:
    image_path (str): Path to the CAPTCHA image file.
    
    Returns:
    str: Extracted text from the CAPTCHA.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur to reduce noise
    blurred = cv2.medianBlur(gray, 3)
    
    # Apply thresholding
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Apply dilation
    kernel = np.ones((2,2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(dilated, config='--psm 6')
    
    # Clean up the text
    clean_text = ''.join(e for e in text if e.isalnum())
    
    return clean_text

def solve_audio_captcha(audio_path):
    """
    Solves an audio-based CAPTCHA file using speech recognition.
    
    Parameters:
    audio_path (str): Path to the CAPTCHA audio file.
    
    Returns:
    str: Transcribed text from the audio CAPTCHA.
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Example usage
if __name__ == '__main__':
    # For text-based CAPTCHA
    text_captcha_path = 'captcha.png'
    captcha_text = solve_text_captcha(text_captcha_path)
    print(f'Solved Text CAPTCHA: {captcha_text}')
    
    # For audio-based CAPTCHA
    audio_captcha_path = 'captcha.wav'
    captcha_audio_text = solve_audio_captcha(audio_captcha_path)
    print(f'Solved Audio CAPTCHA: {captcha_audio_text}')
