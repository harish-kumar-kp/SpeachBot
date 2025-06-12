import streamlit as st
from streamlit_player import st_player
#from PIL import Image
import json
from transformers import AutoTokenizer, AutoModelForQuestionAnswering , pipeline
import torch

import pyttsx3
def text2Speach(text,x,y):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[x].id)   #changing index, changes voices. 1 for female
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (rate)                        #printing current voice rate
    engine.setProperty('rate', y)     # setting up new voice rate
    engine.say(text)
    engine.runAndWait()
    



import speech_recognition as sr
def speach2Txt(stopword):
    questArray=[]
    # Initialize the recognizer 
    r = sr.Recognizer()
    x=1
    while(x):    
        try: 
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()      
        except sr.RequestError as e:
            MyText="Could not request results",{0}.format(e)
        except sr.UnknownValueError:
            MyText="unknown error occurred"
        if MyText == "unknown error occurred":
            finalTxt=""
        else:
            if stopword in MyText:
                finalTxt = MyText.replace(stopword,"?")
                questArray.append(finalTxt)
                break
            else:
                finalTxt = MyText
                questArray.append(finalTxt)
    return ("".join(questArray))



# Path to your custom-trained model
model_name ='model/customTrained_Distilbert_Squad'
# Load pre-trained DistilBERT model and tokenizer
#model_name = "model/customTrained_Distilbert_Squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Streamlit App
st.set_page_config(
    page_title="AI Bot Q & A",
    page_icon="image/ai.png",
    layout="wide",
    initial_sidebar_state='expanded'
)

#try:
col1 , col2 , col3 = st.columns([2, 5, 3])
with col1:
    st.image('image/AI-Human.png')
with col2:
    st.markdown("#### :orange[Question Answering System with Hugging Face Transformer Model- Distil Bert]")
    st.markdown("##### :green[Speach Bot Q & A for Topics on Selected Domain] ")
    st.markdown("###### :red[Project by] :violet[Harish Kumar K P] :orange[email] :blue[harishk_kotte@rediffmail.com]")
with col3:
    
    jFile = ''
    topic = ""
    File = open("appConfig/subjectChoice.txt", "r")
    jFile = File.read()
    st.write(":blue[Choose the Subject by Clicking the Buttons Below]")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        tech = st.button("Technology")
        if tech:
            file = 'appConfig/tech_trend.json'
            topic = "Technology"
            choice = open("appConfig/subjectChoice.txt", "w")
            choice.write(file)
            choice.close()
            st.rerun()

    with col2:            
        food = st.button("Recipies")
        if food:
            file = 'appConfig/food_recipies.json'
            topic = "Recipies"
            choice = open("appConfig/subjectChoice.txt", "w")
            choice.write(file)
            choice.close()
            st.rerun()

    with col3:
        med = st.button("Medical")
        if med:
            file = 'appConfig/medical_subject.json'
            topic = "Medical"
            choice = open("appConfig/subjectChoice.txt", "w")
            choice.write(file)
            choice.close()
            st.rerun()

    # Opening JSON file
    f = open(jFile)
    # returns JSON object as a dictionary
    data = json.load(f)
    # creating list
    topicTitleLst=[]
    contextLst=[]
    vidLnkLst=[]
    imgLnkLst=[]
    refLnkLst=[]
    kewwordLst=[]
    # Iterating through the json list
    for i in data['topicDetails']:
        topicTitleLst.append(i['topicTitle'])
        contextLst.append(i['contextText'])
        vidLnkLst.append(i['videoLink'])
        imgLnkLst.append(i['imageLink'])
        refLnkLst.append(i['referenceLink'])
        kewwordLst.append(i['keywords'])
col1 , col2 , col3 = st.columns([2, 5, 2])
with col1:
    st.write(":red["+ topicTitleLst[0][0] +"] : :blue["+topicTitleLst[0][2] +"]")
    st.write(":red["+ topicTitleLst[1][0] +"] : :blue["+topicTitleLst[1][2] +"]")
    st.write(":red["+ topicTitleLst[2][0] +"] : :blue["+topicTitleLst[2][2] +"]")
    st.write(":red["+ topicTitleLst[3][0] +"] : :blue["+topicTitleLst[3][2] +"]")
    st.write(":red["+ topicTitleLst[4][0] +"] : :blue["+topicTitleLst[4][2] +"]")
    st.write(":red["+ topicTitleLst[5][0] +"] : :blue["+topicTitleLst[5][2] +"]")
    st.write(":red["+ topicTitleLst[6][0] +"] : :blue["+topicTitleLst[6][2] +"]")
    st.write(":red["+ topicTitleLst[7][0] +"] : :blue["+topicTitleLst[7][2] +"]")
    st.write(":red["+ topicTitleLst[8][0] +"] : :blue["+topicTitleLst[8][2] +"]")
    st.write(":red["+ topicTitleLst[9][0] +"] : :blue["+topicTitleLst[9][2] +"]")

    st.write(" :green[Note: Choose topic by Speaking 'Topic # ' or 'Topic Name' end with 'alita' for all commands]")
    st.write(" :green[Note: use command 'start reading alita'' or 'skip reading alita'' for passage text]")
    st.write(" :green[Note: while question session 'go to topics alita'' to change topic]")
    st.write(" :green[Note:'stop alita'' or 'thank you alita'' to stop]")

with col2:
    
    idx = 0
    gender = 1
    speed = 135
    
    context = ""
    text2Speach("Hi Welcome , I am your Answering Bot Alita , Choose a topic with voice command and end always with alita",gender,speed)
    
    passage = ""
    # Text input for the passage
    #height = st.slider("Set the height of the text area", 1, 1000, 95)
    spechQuest =""
    topicChoose=""
    
    topicChoose = (speach2Txt("alita")).strip()
    # iterate through the list of elements
    for i in kewwordLst:
        subString = (i.lower()).split(",")
        for j in subString:
            if j in topicChoose:
                idx = kewwordLst.index(i)
                sbStr = subString
                break
                
    context = contextLst[idx]
    vidLink = vidLnkLst[idx]
    imageLink = imgLnkLst[idx]
    wikiLink = refLnkLst[idx]     
                
    if passage == None:
        text2Speach("Please , Choose a topic",gender,speed )
       
        
    else:
        passage = st.text_area("Topic Context for Questions, Reading voice with voice command 'start reading alita' or skip reading by 'skip reading alita' ",value = context ,height=180)

        col1 , col2 = st.columns(2)
        with col1:
            st.image(imageLink)
                        
        with col2:
            st_player(vidLink , height = 230 , controls=True)        
        st.write(wikiLink)
    
        text2Speach("speak out voice command start reading alita or skip reading alita",gender,speed)
        #st.write(len(passage))
        #st.write(idx)
        #st.write(topicChoose )
        
        #if st.button("Read Passage"):
        if passage == "":
            text2Speach("Hi ,Please choose the topic of context ",gender,speed)
            
            
            
        else:
            
            command = (speach2Txt("alita")).strip()
            if "start reading" in command or "read context" in command or "read it" in command :
                text2Speach(passage ,gender,speed )
                
                
            elif "change the" in command or "back to" in command or "choose another" in command or "go to" in command or "skip this" in command or "wrong" in command:   
                st.rerun()
            elif "skip" in command or "skip reading" in command or "questions" in command or "pass" in command:
                pass
            #if st.button("Listen to Question"):
            #st.write()
    x=1
with col3:
    while(x):
        if passage != "" or passage !="?":
            text2Speach("Your question Please" ,gender,speed)
            
            
            spechQuest = (speach2Txt("alita")).strip()
        # Text input for the question
        if "change" in spechQuest or "back to" in spechQuest or "choose another" in spechQuest or "go to" in spechQuest or "skip this" in spechQuest:
            context = ""
            st.rerun()
        elif "bye" in spechQuest or "see you" in spechQuest or "later" in spechQuest or "stop" in spechQuest or "thank you" in spechQuest:
            st.stop()
        else:
            st.write(":red[Question:]"+ str(spechQuest))
            question = str(spechQuest)
            inputs = tokenizer.encode_plus(question, passage, return_tensors="pt")
            input_ids = inputs["input_ids"].tolist()[0]

            # Get the model's outputs (start and end logits)
            outputs = model(**inputs)
            start_scores = outputs.start_logits
            end_scores = outputs.end_logits

            # Get the most likely start and end tokens
            start_index = torch.argmax(start_scores)
            end_index = torch.argmax(end_scores) + 1

            # Decode the tokens into the answer string
            answer = tokenizer.convert_tokens_to_string(
                tokenizer.convert_ids_to_tokens(input_ids[start_index:end_index])
            )
            # Display the answer
            st.write(":green[Answer:]", answer)
            text2Speach("Answer.......   "+answer,gender,speed)
            
            
            question = ""



#except:
st.write("")
st.write("")
st.write("")
st.write(" :red[Note: Choose topic by Speaking 'Topic # ' or 'Topic Name' end with 'alita' for all commands]")
st.write(" :red[Note: use command 'start reading alita'' or 'skip reading alita'' for passage text]")
st.write(" :red[Note: while question session 'go to topics alita'' to change topic]")
st.write(" :red[Note:'stop alita'' or 'thank you alita'' to stop]")
st.write("")
st.write("")
st.write("")
st.write(" :green[Note: To start,Choose any of the subject 'Technology' or 'Recipies' or 'Medical']")


