from pydantic_core import Url
import requests
import os
from requests.exceptions import HTTPError,ConnectionError,Timeout
# from crypttography.fernet import Fernet
from kivymd.app import MDApp
from  kivymd.uix.label import MDLabel,MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatIconButton,MDRoundFlatIconButton,MDTextButton,MDIconButton,MDFlatButton
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition,FadeTransition,NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import OneLineAvatarListItem,ImageLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.core.window import Window
import bcrypt


class InitialScreen(MDScreen):
    def __init__(self,**kwargs):
        super(InitialScreen,self).__init__(**kwargs)
    def registrati(self):
        title = MDLabel(text = 'registrati'.title(),font_name = 'assets/Poppins/Poppins-MediumItalic.ttf',
            font_size = (17),theme_text_color = 'Custom',text_color = '#F8F5F7')
        '''
        [content : boxlayout , inputs]'''   
        content = MDFloatLayout(size_hint_y = None,height = 400,pos_hint = {'center_x':.5,'center_y':.5})
       

        user_input_box = MDBoxLayout(orientation = 'vertical',padding = 10,spacing = 18,size_hint_y = None,height = 190,pos_hint = {'center_x':.5,'center_y':.47}) 
        '''
        [NOME UTENTE  INPUT ]'''
        self.user_name = MDTextField(size_hint = (1,.10),hint_text = 'nome'.title(),hint_text_color_focus = (96/255, 27/255, 114/255),
        text_color_focus = (96/255, 27/255, 114/255),
        max_text_length = 12,line_color_focus = (96/255, 27/255, 114/255),
        mode = 'fill',fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})

        # '''
        # [COGNOME  INPUT ]'''
        # self.cognome = MDTextField(size_hint = (1,.10),hint_text = 'cognome'.title(),hint_text_color_focus = (96/255, 27/255, 114/255),
        # text_color_focus = (96/255, 27/255, 114/255),
        # max_text_length = 12,mode = 'fill',line_color_focus = (96/255, 27/255, 114/255),
        # fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})

        # '''
        # [EMAIL  INPUT ]'''
        # self.Email = MDTextField(size_hint = (1,.10),hint_text = 'email'.title(),hint_text_color_focus = (96/255, 27/255, 114/255),
        # text_color_focus = (96/255, 27/255, 114/255),validator = 'email',
        # helper_text_mode = 'on_focus',helper_text = 'user@gmail.com',mode = 'fill',line_color_focus = (96/255, 27/255, 114/255),
        # fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})

        '''
        [PASSWORD  INPUT ]'''
        self.password = MDTextField(size_hint = (1,.10),hint_text = 'password',hint_text_color_focus = (96/255, 27/255, 114/255),
        text_color_focus = (96/255, 27/255, 114/255),max_text_length = 15,line_color_focus = (96/255, 27/255, 114/255),
        password = True,icon_left = 'key-variant',mode = 'fill',fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})

        '''
        [REGISTRATION BUTTON ]'''
        reg_button = MDRectangleFlatIconButton(text = 'registrati'.title(),font_name = 'assets/Poppins/Poppins-MediumItalic.ttf',
            font_size = (17),theme_text_color = 'Custom',text_color = '#F8F5F7', line_color=(96/255, 27/255, 114/255), size_hint = (1,.07),pos_hint = {'center_x':.5,'center_y':.5},
            on_press = lambda x: self.Create_new_user(isinstance))

        '''
        [ACCEDI BUTTON IF ACCOUNT ALREDY EXISTS ]'''
        accedi_if_account_exists = MDTextButton(text =  'ti sei gia registrato? accedi'.title(),font_name = 'assets/Poppins/Poppins-MediumItalic.ttf',
            font_style = 'Body2',theme_text_color = 'Custom',text_color = '#F8F5F7',pos_hint = {'center_x':.5,'center_y':.20},on_press = lambda x:self.dialog.dismiss())

        widget_list = [self.user_name, self.password,reg_button]
        for widget in widget_list:
            user_input_box.add_widget(widget)

        #  content.add_widget(bg)
        content.add_widget(user_input_box)
        content.add_widget(accedi_if_account_exists)


        self.dialog = MDDialog(title = title.text,type = 'custom',content_cls=content,md_bg_color = (24/255, 24/255, 24/255))
        self.dialog.open()
    

    '''
        [LA FUNZIONE {CREATE_NEW_USER} INVIA I DATI INSERITI DALL'UTENTE PER POI INVIARLI AL {DATABASE} TRAMITE IL SERVER [FAST-API] ]
        '''
    def Create_new_user(self,*args):
        '''
        CRITTOGRAFIA DEI DATI DELL '/UTENTE 
        '''
        # KEY = Fernet.generate_key()
        # CIPHER_SUITE = Fernet(KEY)
        # DTE = self.password.text.encode()
        # Ecnrypted_password = CIPHER_SUITE.encrypt(DTE)

        # HASH IL PASSWORD PER LA SICUREZZA 
        randow_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password.text.encode('utf-8'),randow_salt)
        # print(user_json_data)
       
        try:
            url = 'http://127.0.0.2:1106/creat-user/'
            user_json_data = dict(list(zip(['nome_utente','password'],[self.user_name.text, str(hashed_password)])))
            if user_json_data['nome_utente'] and user_json_data['password'] != None:
                send_data = requests.post(url,json=user_json_data)
                if url == 200:
                    return send_data.json(),{'alert':'data sended successfully!'}
            else:
                print({'Error': 'compila tuto '})

            
        except requests.exceptions.ConnectionError as e:
            return {'Alert': 'impossisbile raggiungere il serevr '+str(e)}
        # except Exception as e:
        #     print('error',str(e))
        # except Exception as e:
        #     print(str(e))
        


    def eye_on(self,*args):
        '''
        PASSWORD REVEAL  '''
        self.ids.password_mask_.icon = 'eye'
        self.ids.password_input_.password = False

        self.ids.password_mask_.on_release = self.eye_off
    def eye_off(self,*args):
         '''
        PASSWORD MASK  '''
         self.ids.password_mask_.icon = 'eye-off'
         self.ids.password_input_.password = True
     

    
    

    def Forgot_pws_(self,*args):

        title = MDLabel(text = 'recupero password'.title(),font_name = 'assets/Poppins/Poppins-MediumItalic.ttf',
            font_size = (17),theme_text_color = 'Custom',text_color = '#F8F5F7')
        '''
        [content : boxlayout , inputs]'''   
        pass_req_content = MDFloatLayout(size_hint_y = None,height = 230,pos_hint = {'center_x':.5,'center_y':.5})
        user_req_box = MDBoxLayout(orientation = 'vertical',padding = 10,spacing = 18,size_hint_y = None,height = 190,pos_hint = {'center_x':.5,'center_y':.47}) 

        
        '''
        [user_name  INPUT ]'''
        self.nome_utente = MDTextField(size_hint = (1,.10),hint_text = 'nome utente'.title(),hint_text_color_focus = (96/255, 27/255, 114/255),
        text_color_focus = (96/255, 27/255, 114/255),
        max_text_length = 12,line_color_focus = (96/255, 27/255, 114/255),
        mode = 'fill',fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})
        
    
        '''
        [EMAIL  INPUT ]'''
        self.Email_ = MDTextField(size_hint = (1,.10),hint_text = 'email'.title(),hint_text_color_focus = (96/255, 27/255, 114/255),
        text_color_focus = (96/255, 27/255, 114/255),validator = 'email',
        helper_text_mode = 'on_focus',helper_text = 'user@gmail.com',mode = 'fill',line_color_focus = (96/255, 27/255, 114/255),
        fill_color_normal ='#2A2A2A',pos_hint = {'center_x':.5,'center_y':.5})
       
        '''[PASSWORD REQUEST BUTTON ]'''
        password_req_button = MDRectangleFlatIconButton(text = 'richeidi password'.title(),font_name = 'assets/Poppins/Poppins-MediumItalic.ttf',
            font_size = (17),line_color =(96/255, 27/255, 114/255), theme_text_color = 'Custom',text_color = '#F8F5F7',size_hint = (1,.07),pos_hint = {'center_x':.5,'center_y':.5},
            on_press = self.send_password_request)

        '''[EXPETIONS  ]'''
        self.exceptions = MDLabel(text = ''.title(),font_name = 'assets/Poppins/Poppins-Light.ttf',
            font_style = 'Caption',theme_text_color = 'Error',pos_hint = {'center_x':.5,'center_y':.02})

        widget_list = [self.nome_utente,self.Email_,password_req_button]
        for widget in widget_list:
            user_req_box.add_widget(widget)

   
        pass_req_content.add_widget(user_req_box)
        pass_req_content.add_widget(self.exceptions)
        self.dialog = MDDialog(title = title.text,buttons=[
            MDIconButton(
                icon = 'close',pos_hint= {'top':.9},on_press = lambda x : self.dialog.dismiss())
            ],type = 'custom',content_cls=pass_req_content,md_bg_color = (24/255, 24/255, 24/255)
            )
        self.dialog.open()
    def send_password_request(self,*args):
        try:
            
            '''
            SET THE FASTAPI REQUEST '''   
            URL = ' http://127.0.0.1:8001/recupero-password/'

            user_data = dict(list(zip(['nome_utent','Email'],[self.nome_utente.text,self.Email_.text])))
            send_request = requests.post(URL,json=user_data)
            if URL == 200:
                return send_request.json()
        except Exception as e :
            e = list(str(e).split(' '))
            self.exceptions.text = ''.join(e[:7])
            Clock.schedule_once(lambda dt : setattr(self.exceptions,'text',''),5)
    def Accedi(self):
        try:

            user_data = dict(list(zip(['nome_utente','password'],[self.ids.user_name.text, self.ids.password_input.text])))
            URL =  'http://127.0.0.2:1106/get-user/'
            user = requests.get(URL,json=user_data)
            print(user)
        except requests.exceptions.ConnectionError as e :
            print(str(e))

        # self.manager.current = 'main screen'


        

class MainApp(MDApp):
    def build(self):
        Window.size = 1082 ,640 

        '''get kv files path  '''
        # cwd : str = os.getcwd()
        # dir_Path = os.path.join(cwd,'kv-files')
        # kvfile = [i for i in os.listdir(dir_Path) if i == 'InitialScreen.kv']
       
        '''set permission to acces the folder '''
        # desired_permission : int = 0o644
        # os.chmod(dir_Path,desired_permission)
        # kvfile_path : str = os.path.join(dir_Path,''.join(kvfile))
        '''carica kv file '''
        Builder.load_file('InitialScreen.kv')

        sm = ScreenManager(transition = SlideTransition())
        sm.add_widget(InitialScreen(name = 'initial'))
        sm.add_widget(MainScreen(name='main screen'))
        Window.bind(on_resize=self.on_window_resize)
        return sm
        

        
    def on_window_resize(self,instance,width,height):
        print(width,height)
        # max_width,max_height = 360,800
        # if width > max_width or height>max_height:
        #     Window.size = (min(width,max_width),min(height,max_height))

if __name__ == '__main__':
    MainApp().run()