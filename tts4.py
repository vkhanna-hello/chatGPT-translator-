import streamlit as st
import openai
import openpyxl
from pypdf import PdfReader
from gtts import gTTS
import csv
import os
from io import StringIO
import pandas as pd

def SendText(my_input, languageSelected):
    try:
        messages = [
        {"role": "system", "content": "You are a natural language translator which will translate the given text to: " + languageSelected}, ] 
        if my_input:
            messages.append(
                {"role": "user", "content": "translatethe following to:"+languageSelected + "text:"+ my_input},
                )
            chat = openai.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages
            )
            
        reply = chat.choices[0].message.content
        tts = gTTS(reply)
        tts.save('translation.mp3')
        st.markdown(reply)
    except UnboundLocalError:
        print("")


def file_upload(file_uploaded):
    try:
        text = ""             
        if file_uploaded.name[-5:] == ".xlsx":
            wrkbk = openpyxl.load_workbook(file_uploaded) 
            sh = wrkbk.active 
            for row in sh.iter_rows():
                for cell in row:
                    text += str(cell.value)
                    inputText = text


        if file_uploaded.name[-4:] == ".pdf":
            pdf_reader = PdfReader(file_uploaded)
            for page in pdf_reader.pages:
                text += page.extract_text()
                inputText = text
                


        if file_uploaded.name[-4:] == ".txt":
            stringio = StringIO(file_uploaded.getvalue().decode("utf-8"))
            for ch in stringio:
                text += ch
                inputText = text
                
        if file_uploaded.name[-4:] == ".csv": 
            csvFile = open(file_uploaded.name, newline='')       
            reader = csv.reader(csvFile)
            for line in reader:
                for i in line:
                    print(i)
                    text += i
            inputText = text

        return inputText
        
    except AttributeError:
        print("")

# Key as environment variable - required when hosting online.      
openai.api_key = os.getenv("OPENAI_API_KEY")


        

st.header("Language Translator")
languages = ["Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"]
languageSelected = st.selectbox("Choose translated language", languages, key="languageselector")

inputText = st.text_input(label = "Input text", value=" Provide text here")
st.button(label = "input text1", on_click = SendText(inputText,languageSelected ))


file_uploaded = st.file_uploader(label="Upload your .xlsx, .xlsm, .pdf, .txt, .csv file for translation ", type=[".xlsx", ".xlsm", ".pdf", ".txt", ".csv"])

st.button(label = "input text2", on_click = SendText(file_upload(file_uploaded), languageSelected))