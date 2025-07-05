import cv2
from deepface import DeepFace
from PIL import Image
import numpy as nu
import streamlit as st
import tempfile
import os
st.markdown("""
<style>
.stApp{
    background-color: #1e1e2f;
    color: black;
    padding: 2rem;
}
body {
   background-color: #1e1e2f;
}
h1,h2,h3,h4,h5 {
    color: #4ea8de;
}
.stButton>button {
    background-color: #ff4b4b;
    color: White;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""",unsafe_allow_html=True)

#The following is the Layout Part of the System written in CSS  
st.markdown("""
    <style>
    .stApp{
        backgroud-color: #e6foff;
       color: blue
       }
       h1,h2,h3,h4{
           color:#0066cc; 
        }
        .stButton>button {
            backgroud-color: #ff6666;
            color:white;
            border-radius: 8px;
            font-weight:bold
       }
        </style>
    """,unsafe_allow_html=True)

mood_songs={
    "happy":["Happy - pharrell williams","Uptown Funk - Bruno Mars","Light Switch - NickeyYOUre,hey daisy","No Idea - Don Toliver","Streo Hearts(feat Adam) - Gym Glass Heros"],
    "sad":["let her go - passenger","someone like you - Adele","Someone You Loved - Lewis Capaldi","I cant Hate You - Kayou","Angels For each Other - martin Garrix"],
    "angry":["Numb - Linkin park","Break Stuff - Limp Bizkit","ULTIMATE - xneymar","Death is no more - BLESSED MANE","Bones - Imagine Dragon"],
    "relaxed":["Weightless - Markoni Union","Let it be - The Beatles","Dynasty - MIIA","In THis Shirt - The irrepressibles","Little Dark Age - MGMT"],
    "Stressed":["Fix You - Cold Play","Breath Me - Sia","Let Me Doen Slowly - Alec Benjamin","Arcade - Duncan Lawrence","No Lie - Sean Paul","Tous Le Memes - Stromae"]
}
def detect_mood(user_text):
    text = user_text.lower()
    for mood in mood_songs:
        if mood in text:
            return mood
    return "relaxed" #default mood for user

st.title("Modd Journal With Sound Track")
st.write("Describe how you are feeling , and we will recommend songs to match your mood")

user_input = st.text_area("Today how are You feeling")
if st.button("Get Songs"):
    if user_input.strip() == "":
        st.warning("Please Write Something On your Mood")
    else:
        mood = detect_mood(user_input)
        songs = mood_songs.get(mood, [])
        st.success(f"Detected Mood: **{mood.capitalize()}**")
        st.write("Recommended Songs:")
        for song in songs:
            st.markdown(f"- {song}")

st.markdown("---")
st.subheader("Or Detect Mood from Your Face")


if st.button("Capture Face And Detect Emotion"):
    st.markdown("""
            <p style='color:#00FF00;' 'font size:14px;'>
            <b>Privacy Notice:</b> Webcam is only accessed after your permission when you click the button below. <br>
                Images are Recorded and Stored locally not shared to any Third Party
                </p>
                """,  unsafe_allow_html=True)
    cap = cv2.VideoCapture(0)
    st.info("Capturing....Please Look at The Camera")
    ret, frame = cap.read()
    cap.release()

    if ret:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        st.image(img_rgb, caption="Captured Image" , use_container_width=True)
        img_path = os.path.join(tempfile.gettempdir(), "capture.jpg")
        cv2.imwrite(img_path, frame)

        try:
            result = DeepFace.analyze(img_path=img_path, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            st.success(f"Detected Emotion: {emotion.capitalize()}")

            mood_map = {
                'happy': 'happy',
                'sad': 'sad',
                'angry': 'angry',
                'fear': 'fear',
                'neutral': 'relaxed',
                'surprise': 'happy',
                'disgust': 'angry'
            }
            mood = mood_map.get(emotion.lower(),'relaxed')
            st.info(f"Mood Category: {mood}")
            
            st.markdown("### Recommended Songs:")
            for song in mood_songs[mood]:
                st.write(f"- {song}")

            #This will remove the image that has been captured recently    
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception as e:
            st.error("Emotion Detection Failed. Try Again with clear Lighting.")
            st.text(str(e))
