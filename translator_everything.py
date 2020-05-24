from tkinter import *
from tkinter import ttk
from googletrans import Translator
import pyttsx3
import speech_recognition as sr
from tkinter import filedialog
import pytesseract
from PIL import Image

LARGE_FONT = ("Verdana", 12)


class ZahidTranslator(Tk):
    global des_lang,lang
    lang =(
        "English",
        'Hindi',
        'French',
        'Spanish',
        'Japanese',
        'Russian',
        'Italian'
    )
    des_lang = {
        "English": 'en',
        'Hindi': 'hi',
        'French': 'fr',
        'Spanish': 'es',
        'Japanese': 'ja',
        'Russian': 'ru',
        'Italian': 'it'
    }

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        label = Label( bg='gray18')
        label.pack()
        container = Frame(label, relief=SUNKEN, bg="gray18", bd=1)
        container.pack(fill=BOTH, expand=True)

        self.frames = {}

        for F in (HomePage, TextTranslator, VoiceTranslator,Pictranslator):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def Speak(self,content):
        engine = pyttsx3.init()
        David = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.setProperty('voice', David)
        print("Jarvis: " + str(content))
        engine.say(str(content))
        engine.runAndWait()

#================================x===============================================x========================================
class HomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent,bg='gray14')
        label = Label(self, text="ZAHID TRANSLATOR",fg='green2',bg='gray14', font=('arial',35,'bold')).grid(row=1,column=1,columnspan=3)

        button = Button(self,label,text="Text",font=('arial',14,'bold'),bg='gray12',fg='cyan',command=lambda: controller.show_frame(TextTranslator)).grid(row=2,column=1,pady=10)


        button2 = Button(self, text="Voice",font=('arial',14,'bold'),bg='gray12',fg='cyan',command=lambda: controller.show_frame(VoiceTranslator)).grid(row=2,column=2)

        button3 = Button(self, text="Image",bg='gray12',fg='cyan',font=('arial',14,'bold'),command=lambda: controller.show_frame(Pictranslator)).grid(row=2,column=3)


#================================x===============================================x========================================

#Translation for Text
class TextTranslator(Frame):

    def translate(self):
        global translated_text,trans
        de = combobox_lang.get()
        translat_text = text_entry.get()

        translator = Translator()
        trans = translator.translate(translat_text, dest=des_lang[de]).text
        translated_text = Label(self, text='----------------------------------------------------------------', fg='cyan', font=('arial', 14), bg='gray14')
        translated_text.grid(row=5, column=0,pady=10, padx=10,columnspan=3)


        translated_text = Label(self, text=trans, fg='cyan', font=('arial', 14), bg='gray14',wraplength=500)
        translated_text.grid(row=6, column=0,pady=10, padx=10,columnspan=3)



    def Clr(self):
        translated_text['text']=''


# GUI programming for Text Translation
    def __init__(self, parent, controller):
        global combobox_lang,text_entry
        Frame.__init__(self, parent,bg='gray14')
        label = Label(self, text="TEXT TRANSLATOR", fg='green2',font=('arial',28,'bold'),bg='gray14').grid(row=1,pady=10, padx=10,columnspan=3)
        inputtext = Label(self, text="Input Text: ", fg='cyan',font=('arial',20,'bold'),bg='gray14').grid(row=2,column=0,pady=10, padx=10)

        text_entry=Entry(self,bg='black',fg='cyan',font=('arial',14))
        text_entry.grid(row=2,column=1,columnspan=2)

        languagetext = Label(self, text="Language ", fg='cyan',font=('arial',20,'bold'),bg='gray14').grid(row=3,column=0,pady=10, padx=10,sticky='W')
        combobox_lang=ttk.Combobox(self,values=lang,width=10,state='readonly')
        combobox_lang.grid(row=3,column=1)

        button1 = Button(self, text="Home",command=lambda: controller.show_frame(HomePage),bg='green2',fg='white').grid(row=4, column=0,sticky=W)

        button2 = Button(self, text="Translate",command=lambda: self.translate(),bg='gray14',fg='cyan').grid(row=4, column=1,sticky=E)
        button2 = Button(self, text="Voice",bg='gray14',fg='cyan',command=lambda: ZahidTranslator.Speak(self, trans)).grid(row=4, column=2, sticky=E)

        Clrbtn = Button(self, text="Clear", fg='cyan', bg='gray14', command=lambda: self.Clr()).grid(row=4, column=3, sticky=E)


#================================x===============================================x========================================

#translation for Voice
class VoiceTranslator(Frame):

    def My_command(self):

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            audio = r.record(source, duration=10)

            try:
                global query
                query = r.recognize_google(audio)
                print('user: ', query)
                return query

            except:
                not_recognize="sorry sir! \n I didn\'t get that!"
                ZahidTranslator.Speak(self,not_recognize)

    def translate_for_voice(self):
        global translated_text, Voice_trans
        de = combobox_lang2.get()
        translat_text = query

        translator = Translator()

        Voice_trans = translator.translate(translat_text, dest=des_lang[de]).text
        translated_text = Label(self, text='---------------------------------------------', fg='cyan', font=('arial', 14), bg='gray14').grid(row=5, column=0,pady=10,padx=10,columnspan=3)

        translated_text = Label(self, text=Voice_trans, fg='cyan', font=('arial', 14), bg='gray14',wraplength=500)
        translated_text.grid(row=6, column=0,pady=10,padx=10,columnspan=3)
        ZahidTranslator.Speak(self, Voice_trans)
    def Clr(self):
        translated_text['text'] = ''

    def __init__(self, parent, controller):
        global combobox_lang2
        Frame.__init__(self, parent,bg='gray14')
        label = Label(self, text="VOICE TRANSLATOR", bg='gray14',fg='green2',font=('arial',28,'bold')).grid(row=1,pady=10, padx=10,columnspan=3)

        RecordBtn = Button(self, text="Record",fg='cyan',command=lambda: self.My_command(),bg='gray14').grid(row=2, column=0)
        HomeBtn = Button(self, text="Home",fg='white',bg='green2',command=lambda: controller.show_frame(HomePage)).grid(row=4,column=0,sticky='W')

        languagetext = Label(self, text="Language ", fg='cyan', font=('arial', 20, 'bold'), bg='gray14').grid(row=3,column=0,pady=10,padx=10,sticky='W')

        combobox_lang2 = ttk.Combobox(self, values=lang, width=10, state='readonly')
        combobox_lang2.grid(row=3, column=1)

        TextBtn = Button(self, text="Translate", bg='gray14', fg='cyan',command=lambda: self.translate_for_voice()).grid(row=4,column=1,pady=10,padx=10,sticky='E')

        Clrbtn = Button(self, text="Clear", fg='cyan', bg='gray14',command=lambda: self.Clr()).grid(row=4, column=2, sticky=E)

#================================x===============================================x========================================
#translation for pictures

class Pictranslator(Frame):

    def atachements(self):
        global body_path
        body_path = filedialog.askopenfilename(initialdir='/', title='select the file',filetype=(('jpeg', '*.jpg'), ('All Files', '*.*')))
        body = (body_path.split('/'))[-1]
        body_lable = Label(self, text=body, font=('arial', 10), fg='cyan', bg='black').grid(row=2, column=2, sticky=E)



    def translate_for_image(self):
        global translated_image, img_trans,zahidtext,translated_text
        de = combobox_lang3.get()

        translator = Translator()
        img = Image.open(body_path)
        pytesseract.pytesseract.tesseract_cmd = 'C:/python/Scripts/tesseract.exe'
        result = pytesseract.image_to_string(img)

        print(result)
        img_trans = translator.translate(result, dest=des_lang[de]).text
        print(img_trans)
        translated_text = Label(self, text='-------------------------------------------------------------', fg='cyan', font=('arial', 14), bg='gray14').grid(row=5, column=0, pady=10, padx=10,columnspan=3)

        translated_text = Label(self, text=img_trans, fg='cyan', font=('arial', 14), bg='gray14')
        translated_text.grid(row=6, column=0,pady=10,padx=10,columnspan=3)
    def Clr(self):
        translated_text['text'] = ''

    def __init__(self, parent, controller):
        global combobox_lang3
        Frame.__init__(self, parent, bg='gray14')
        label = Label(self, text="TEXT IMAGE TRANSLATOR", bg='gray14', fg='green2', font=('arial', 25, 'bold')).grid(row=1,pady=10, padx=10,columnspan=3)

        label = Label(self, text="Browse Image", bg='gray14', fg='cyan', font=('arial', 20, 'bold')).grid(row=2,pady=10,padx=10,sticky='W')
        Btn = Button(self, text="Browse", fg='cyan',command=lambda: self.atachements(), bg='gray14').grid(row=2, column=1)
        HomeBtn = Button(self, text="Home", fg='white', bg='green2',command=lambda: controller.show_frame(HomePage)).grid(row=4, column=0,sticky='W')

        languagetext = Label(self, text="Language ", fg='cyan', font=('arial', 20, 'bold'), bg='gray14').grid(row=3,column=0,pady=10,padx=10,sticky='W')


        combobox_lang3 = ttk.Combobox(self, values=lang, width=10, state='readonly')
        combobox_lang3.grid(row=3, column=1)

        HomeBtn = Button(self, text="Translate", fg='cyan', bg='gray14',command=lambda: self.translate_for_image()).grid(row=4, column=1, sticky='E')

        HomeBtn = Button(self, text="Voice", fg='cyan', bg='gray14',command=lambda: ZahidTranslator.Speak(self, img_trans)).grid(row=4, column=2, sticky='W')

        Clrbtn = Button(self, text="Clear", fg='cyan', bg='gray14',command=lambda: self.Clr()).grid(row=4, column=3, sticky=E)

app = ZahidTranslator()
app.mainloop()