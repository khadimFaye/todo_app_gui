from kivymd.app import MDApp
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.lang.builder import Builder
# locale.setlocale(locale.LC_TIME,'it_IT.UTF-8')
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList,ThreeLineAvatarIconListItem,ILeftBody 
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from datetime import datetime
from sqlite3 import SQLITE_EMPTY,SQLITE_ERROR,OperationalError
from plyer import notification
import locale
from database import Database
db = Database()

class CARD(MDCard):
    ''' inizializza il card class '''
    def __init__(self,**kwargs):
        super().__init__() 

        self.size_hint=(1,None)                         
        self.height = (80)
        self.radius = [17,17,17,17]

class RELATIVE_LY(MDRelativeLayout):
    ''' inizializza il relativelayout class '''
    def __init__(self,**kwargs):
        super().__init__()
        self.size_hint_y = None
        self.height = 80
        self.pos_hint = {'center_x':.5,'center_y':.5}

class Dialog_content(MDBoxLayout):
    

    def __init__(self,**kwargs):
        super(Dialog_content,self).__init__(**kwargs)
        now = datetime.now()
        self.ids.date_text_label.text = str(now.strftime('%A %d %B %Y'))
        self.ids.inputs_gridlayout.bind(minimum_height = self.ids.inputs_gridlayout.setter('height'))
        self.update_height()
    def update_height(self):
        self.ids.inputs_gridlayout.height+=self.ids.task.height
        # self.ids.scrollview.height=self.ids.inputs_gridlayout.height
      

        
    def init_dat_time(self):
        data_picker = MDDatePicker(size_hint = (None,None),size =( 100,50))
        data_picker.bind(on_save =self.save)
        data_picker.open()

    def save(self,instance,value,data_range):
        data = value.strftime('%A %d %B %Y')
        self.ids.date_text_label.text = str(data)
        print(str(self.ids.date_text_label.text))

    
    
class ListItemWith_Checkbox(ThreeLineAvatarIconListItem):
    def __init__(self,pk=None,**kwargs):
        super().__init__(**kwargs)
        self.text_propery()
        self.pk = pk
        
    def text_propery(self):
        self._no_ripple_effect = True
        self.text = self.text.title()
        self.bold = True
        self.font_size = 12
        self.secondary_font_style = 'Body2'
        self.secondary_font_size = 9
        self.tertiary_font_style = 'Caption'
        self.tertiary_font_size = 8
    
    def mark(self,check,itemlist):
        try:
            ''' SEGNA I COMPITI GIA FATTI '''
            if check.active == True:
                itemlist.text = '[s]' + itemlist.text + '[s]'
                itemlist.secondary_text =  '[s]'+ itemlist.secondary_text + '[/s]'
                db.mark_task_completi(itemlist.pk)
            else:
                # print(itemlist.text.removeprefix('[s]'.upper()))  # = ''.join(itemlist.text).split('[s],[/s]').strip()
                db.mark_task_incompleti(itemlist.pk)
        # except SQLITE_ERROR as e:
        #     print(str(e))
        except Exception as e:
            print(str(e))


    def delet_item(self,trash,itemlist):
        md_list = itemlist.parent.parent.parent
    
        md_list.remove_widget(itemlist.parent.parent)
        md_list.remove_widget(itemlist.parent)
        md_list.remove_widget(itemlist)
        
        # card.remove_widget(relativ_layout)

        self.parent.remove_widget(itemlist)
        db.delet_task(itemlist.pk)
        
class MainApp(MDApp):
    
    def build(self):
        self.theme_cls.theme_style='Dark'
        self.theme_cls.primary_palette = 'DeepPurple'
        locale.setlocale(locale.LC_TIME,'it_IT.UTF-8')
        print(dir(locale))
        self.LISTA_TASK_TO_MODIFY = []
    
        return Builder.load_file('todo.kv')
    
    def Open_dialog(self):
        try:

            self.dialog = MDDialog(title = 'aggiugni un nuovo campito'.capitalize(),type ='custom',
            content_cls = Dialog_content())
            self.dialog.open()

            
        except Exception as e:
            print(str(e))
    

    def add_task(self,task_title,task,date_text):
        try:

            ''' add task passando i valori al data base '''
            TASK =  db.add_task(task_title.text.title(), task.text, date_text.text)

            ''' crea un istanza di CARD che conterra RELATIVE_LY '''
            

            ''' crea una relativa layout per inserire il  ListItemWith_Checkbox e le label'''
            relative_ly =RELATIVE_LY()
            relative_ly.add_widget(ListItemWith_Checkbox(pk=str(TASK[0]), text = str(TASK[1]),
                        secondary_text= str(TASK[2]), tertiary_text =str(TASK[3])))
            Card = CARD()
            Card.add_widget(relative_ly)
            

            print(TASK)
            self.root.ids['container'].add_widget(Card)
            
            print(task_title.text,task.text,date_text.text)
            task.text = ''
            task_title.text = ''
            self.close_dialog()
            self.send_notify()
        except SQLITE_ERROR as e:
            print(str(e))
        except Exception as e:
            print(str(e))

    # def modify_task(self,itemlist):
        
    #     self.LISTA_TASK_TO_MODIFY.append((itemlist.text,itemlist.secondary_text))
    #     print(self.LISTA_TASK_TO_MODIFY)
        
    #     self.dialog.open()
    def Open_dialog_to_modify_task(self,itemlist):
        self.LISTA_TASK_TO_MODIFY.append((itemlist.text,itemlist.secondary_text))
        print(self.LISTA_TASK_TO_MODIFY)

        self.dialog = MDDialog(title = 'modifica compito'.capitalize(),type ='custom',
        content_cls = Dialog_content())

        ''' crea un istanza di dialog per accedere ai widget del contenuto '''
        content = self.dialog.content_cls
        content.ids.task_title.text =itemlist.text
        content.ids.task.text =itemlist.secondary_text

        ''' init the save button e disabilita il b[salva]'''
        content.ids.save_mod_button.disabled=False
        content.ids.save_mod_button.bind(on_press = self.save_modified_task)
        content.ids.salva.disabled = True

        ''' apri il widget [DIALOGO]'''
        self.dialog.open()
    
    def close_dialog(self):
        self.dialog.dismiss()


    def save_modified_task(self,instance):
        try:
            if instance.text == 'salva modifiche':
                content = self.dialog.content_cls
                list_element = self.root.ids['container']
                list_task =[item for card in list_element.children if isinstance(card,MDCard) for rl in card.children if isinstance(rl,MDRelativeLayout) for item in rl.children if isinstance(item,ThreeLineAvatarIconListItem)] 

                for child in list_task:
                    # if isinstance(child,ThreeLineAvatarIconListItem):
                    chil_instance =( child.text,child.secondary_text)
                    if chil_instance in  self.LISTA_TASK_TO_MODIFY:

                        task_modifyed = db.modifiy(content.ids.task_title.text, content.ids.task.text,child.pk)
                        print(task_modifyed)
                        child.text = str(task_modifyed[0][0])
                        child.secondary_text =str(task_modifyed[0][1])
                        self.LISTA_TASK_TO_MODIFY.clear()
                        print(self.LISTA_TASK_TO_MODIFY)

                        self.close_dialog()
                        content.ids.task.text =''
                        content.ids.task_title.text =''
            else:
                self.close_dialog()
        except Exception as e:
            print(str(e))




    

    def send_notify(self):

        title = 'task aggiunto!'
        message = 'dacci dentro'.capitalize()
        notification.notify(
            title = title,
            message = message,
            app_name = 'task manager'.title(),
            ticker = 'basta procrastinare!!',
            timeout = 4
    
        )
    def on_start(self):
        try:

            incompleti, completi  = db.get_tasks()
            print(completi,incompleti)
            if incompleti is not None:
                for task in incompleti:
                    task_incompleti = ListItemWith_Checkbox(pk = task[0],text =str(task[1]), secondary_text=str(task[2]), tertiary_text = str(task[3]))
                    relative_ly = RELATIVE_LY()
                    relative_ly.add_widget(task_incompleti)

                    Card = CARD()
                    Card.add_widget(relative_ly)
                    self.root.ids['container'].add_widget(Card)
            if completi is not None:
                for task in completi:
                    task_completi = ListItemWith_Checkbox(pk = task[0],text ='[s]'+str(task[1])+'[/s]',secondary_text='[s]'+str(task[2])+'[/s]',tertiary_text = str(task[3]))
                    task_completi.ids.check.active = True

                    '''CREA UN ISTANZA DI RELATIVE_LY '''
                    relative_ly = RELATIVE_LY()
                    relative_ly.add_widget(task_completi)
                    ''' CREA UN ISTANZA DI CARD '''
                    Card = CARD()
                    Card.add_widget(relative_ly) 
                    self.root.ids['container'].add_widget(Card)
        except Exception as e:
            print(str(e))
                
    def on_stop(self):
        ''' elimina tutti i widget dal parent'''
        for i in self.root.ids['container'].children:
            self.root.ids['container'].remove_widget(i)
            print('leavinggg')


        
if __name__=='__main__':
    MainApp().run()


