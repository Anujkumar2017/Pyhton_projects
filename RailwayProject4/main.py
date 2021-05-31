import os
import pandas as pd
from pydub import AudioSegment
from gtts import gTTS


def generateSegment(start,finish,filename):
    audio =AudioSegment.from_mp3('railway.mp3')
    audioProcessed = audio[start:finish]
    audioProcessed.export(filename,format='mp3')
    return audioProcessed

def textToSpeech(text,filename):
    mytext = str(text)
    language ='hi'
    myobj = gTTS(text=mytext,lang=language,slow=True)
    myobj.save(filename)
    print(myobj)

def mergeAudios(audios):
    combined = AudioSegment.empty()
    for audio in audios:
        combined += AudioSegment.from_mp3(audio)
    return combined 

def generateSkleton():
    # 1. "kripya dyaan dijiye"    
    generateSegment(88000,90200,"1_hindi.mp3")
    # 3. "se chalkar"    
    generateSegment(91000,92200,"3_hindi.mp3")
    # 5. "ke raste"    
    generateSegment(94000,95000,"5_hindi.mp3")
    # 7. "ko jane wali gadi sankhya"    
    generateSegment(96000,98200,"7_hindi.mp3")
    # 9. "kuchh hi samaye me platform sankhya"    
    generateSegment(105000,108500,"9_hindi.mp3")
    # 11. "par aa rhi hai"    
    generateSegment(109000,112250,"11_hindi.mp3") 

def generateAnnouncement(filename):
    df = pd.read_excel(filename)
    # print(df)
    for index, item in df.iterrows():
        # 2. from city
        textToSpeech(item['from'],"2_hindi.mp3") 
        # 4. via-city
        textToSpeech(item['via'],"4_hindi.mp3") 
        # 6. to-city
        textToSpeech(item['to'],"6_hindi.mp3")
        # 8. train no and name
        textToSpeech(item['train_no']+" "+item['train_name'],"8_hindi.mp3") 
        # 10. platform no
        textToSpeech(item['platform'],"10_hindi.mp3")

        audios = [f"{i}_hindi.mp3" for i in range(1,12)]
        
        announcement = mergeAudios(audios)
        announcement.export(f"announcement_{index+1}.mp3",format='mp3')

if __name__ == "__main__":
    print('Generating Skeleton....')
    generateSkleton()
    print("Now generating a announcement..")
    generateAnnouncement('announce_hindi.xlsx')
