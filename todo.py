


from kivymd.app import MDApp
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.lang.builder import Builder
from kivy.core.window import Window
# locale.setlocale(locale.LC_TIME,'it_IT.UTF-8')
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList,ThreeLineAvatarIconListItem,ILeftBody ,OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.card import MDCard,MDCardSwipe,MDCardSwipeLayerBox,MDCardSwipeFrontBox

from kivymd.uix.chip import MDChip
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import Clock,StringProperty, NumericProperty
from kivy.metrics import dp
from kivymd.uix.bottomsheet import MDCustomBottomSheet,MDBottomSheet
from datetime import datetime
from sqlite3 import SQLITE_EMPTY,SQLITE_ERROR,OperationalError
# from plyer import notification
import locale  
import time
from initialScreen import InitialScreen
from database import Database
db = Database()

class task_content_screen(Screen):
    regular = StringProperty('AllertaStencil-Regular.ttf')
    num_obj = StringProperty('0')
    lista_obj = []

    task_id = []
    def __init__(self, **kwargs):
        super(task_content_screen,self).__init__(**kwargs)

        ''' REGOLA L ALTEZZ ADEI LAYOUT IN MODO DA AVERE SPAZIO PER  LO SCROLLING '''
        self.ids.widget_box.bind(minimum_height = self.ids.widget_box.setter('height'))
        self.grid = [grid for child in self.ids.widget_box.children if isinstance(child,MDList) for grid in child.children if isinstance(grid,MDGridLayout)]
        self.card = [card for card in self.ids.widget_box.children if isinstance(card,MDList) ]

    def update_num_obbiettivi(self):
        ''' aggiorna il numero degli obiettivi '''
        lista_obiettivi = [obj for obj in self.grid[0].children if isinstance(obj,MDCardSwipe)]
        num_obiettivi = len(lista_obiettivi)
        self.num_obj =str(num_obiettivi)
        return self.num_obj

    def update(self):

        for j in self.grid[0].children:
            j.parent.height+=j.height/7
            self.ids.widget_box.height +=j.parent.height/90
        print(self.ids.widget_box.height)
        # self.update_num_obbiettivi()

    def swith_to_home(self,instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'main screen'
        self.task_id.clear()
    
    def add_subtask(self,sottoObiettivo):
        # task_id = self.task_id[0]
        # print(task_id)
        if len(sottoObiettivo.text)>=80:

            print(f'{sottoObiettivo.text[:int(len(sottoObiettivo.text)/2)]}\n{sottoObiettivo.text[int(len(sottoObiettivo.text)/2):]}')
        subtask = db.add_subtask(sottoObiettivo.text,0,self.task_id[0])
        print(subtask) 
        ''' accedi alla list degli item tramite ID'''
        LISTA_ITEM = self.grid[0]

        ''' creare un oggetto di tipo OneLineAvatarIconListItem e [e task tag]'''
        task_tag = MDLabel(text= f'#{self.ids.top_bar.title}',
            font_style = 'Body2',font_size=dp(10),theme_text_color='Custom',text_color ='#316bd6')
        
        Sub_Task = OneLine_AvatarIcon_ListItem(pk=subtask[1],
            text=f'{subtask[0]}  {task_tag.text}',
           _no_ripple_effect = 1,divider=None, pos_hint={'center_x':.5,'center_y':.5})

        swipe_card = Swipecard(size_hint = (1,None),height =Sub_Task.height-10)

        ''' crea un istansa di MDRelativeLayout '''
        RL_Layout = MDRelativeLayout(size_hint_y = None,height=swipe_card.height,pos_hint={'center_x':.5,'center_y':.5})

        ''' aggiugni i widget '''
        RL_Layout.add_widget(Sub_Task)
        swipe_card.ids.frontbox.add_widget(RL_Layout)
        LISTA_ITEM.add_widget(swipe_card)
        self.lista_obj.append(swipe_card)
        self.num_obj = str(len(self.lista_obj))

      
       
        ''' pulisci input '''
        sottoObiettivo.text = ''
        self.update()
    def swith_to_contet(self,itemlist):
        pass
    
        

    ''' pulisci tutti i subtasks ogni volta che lasci lo schermo '''
    def on_leave(self):
        self.grid[0].clear_widgets()
        self.lista_obj.clear()
        self.num_obj='0'
    
       

class Swipecard(MDCardSwipe):
    def __init__(self,**kawrgs):
        super().__init__(**kawrgs)
        # self.task_content = task_content

    def check_state(self,swipecard):
        for swipe in swipecard.parent.children:
            if swipe!=swipecard :
             
                swipe.close_card()
                # print(swipe.state)
    def delet_sub_task(self,sub_task):
        confirmation = MDDialog(title = 'attenzione!',text ='vuoi veramente eliminare questo obiettivo?',
                buttons = [MDRaisedButton(text='si',on_press = lambda x: confirm()),
                           MDRaisedButton(text = 'no',on_press = lambda x:confirmation.dismiss() )])
        confirmation.open()
        print('helo')
        ''' crea un sub function per la conferma di concellazione'''
        def confirm():
            id_sub_task_to_delet = [task.pk for child in  sub_task.children if isinstance(child,MDCardSwipeFrontBox) for sub_child in child.children if isinstance(sub_child,MDRelativeLayout) for task in sub_child.children if isinstance(task,OneLineAvatarIconListItem)]
            sub_task.parent.remove_widget(sub_task)
            ''' crea un istanza di task content screen e ricava id del task principale '''
            task_content=MDApp.get_running_app().root.get_screen('task content')
            task_id = task_content.task_id[0]
            db.delet_subtask(task_id,id_sub_task_to_delet[0])
            
            confirmation.dismiss()

            ''' aggorna il contatore di obbietivi '''
            app = MDApp.get_running_app().root.get_screen('task content').update_num_obbiettivi()
            return app
            # MDApp.get_running_app()
            # screnn_manager = app.root
            # get_screen = screnn_manager.get_screen('task content')
            # get_screen.update_num_obbiettivi()

            # task_content.update_num_obbiettivi()
    


    
class OneLine_AvatarIcon_ListItem(OneLineAvatarIconListItem):
    def __init__(self,pk=None,**kwargs):
        self.pk = pk
        super().__init__(**kwargs)
        self.font_size = dp(10)
        self.font_style = 'Body2'
        self.text_color='white'


    def check_icon(self,instance):
        if instance.icon!='check-circle':
            self.ids.circle_icon.icon = 'check-circle'
        else:
            self.ids.circle_icon.icon = 'circle-outline'
    # def on_open_progress(self,instance,value:float):
    #     # print(instance)
    #     pass
      
            




class MainScreen(Screen):
    pass
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
        db.delet_all_subtask(itemlist.pk)
        
        
class MainApp(MDApp):
    
    def build(self):
        Window.size = (1082 ,640)
        self.theme_cls.theme_style='Dark'
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.material_style = 'M3'
        locale.setlocale(locale.LC_TIME,'it_IT.UTF-8')
        print(dir(locale))
        
        self.LISTA_TASK_TO_MODIFY = []
        self.sm = MDScreenManager()
        Builder.load_file('todo.kv')
        Builder.load_file('InitialScreen.kv')

        self.sm.add_widget(InitialScreen(name='initial'))
        self.sm.add_widget(MainScreen(name = 'main screen'))
        self.sm.add_widget(task_content_screen(name='task content'))
        return self.sm
    
    def Open_dialog(self):
        try:
            
            self.dialog = MDDialog(title = 'aggiugni un nuovo campito'.capitalize(),type ='custom',
            content_cls = Dialog_content())
            self.dialog.open()

        except Exception as e:
            print(str(e))
    
    def check_inputs(self,instance):
        content = Dialog_content()
        itemlist = ListItemWith_Checkbox()
        ''' controlla gli inputs se hanno un valore inserito'''
        content.ids.task.text = 'ciao'  
       
        if content.ids.task.text !='' or content.ids.task_title.text !='':
                content.ids.salva.disabled = False
        
        # if content.ids.task.text == itemlist.text  or content.task_title.text == itemlist.secondary_text:
        #         content.ids.save_mod_button.disabled = True
        # else:
        #     content.ids.save_mod_button.disabled = False

        
        


    def add_task(self,instance,task_title,task,date_text):
        try:
            if  (task_title.text != '') or (task.text != ''):

                if  instance.text == 'salva':

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
                    container = self.root.get_screen('main screen')
                    container.ids['container'].add_widget(Card)
                   
                    
                    print(task_title.text,task.text,date_text.text)
                    task.text = ''
                    task_title.text = ''
                    self.close_dialog()
                    # self.send_notify()
            else:
                empty_campo_popup = MDDialog(title = 'avviso', text = '** i campi sono vuoti per favore riempili ;) **',size_hint = (.5,.2),
                    buttons=[MDRaisedButton(text="OK", pos_hint = {'right':.7}, on_release=lambda x : empty_campo_popup.dismiss())])
                empty_campo_popup.open()
        # except SQLITE_ERROR as e:
        #     print(str(e))
        except Exception as e:
            print(str(e))

    def Open_content_task_screen(self,itemlist):
        content_task = self.sm.get_screen('task content')
        content_task.ids.top_bar.title = itemlist.text
        LISTA_ITEM = content_task.grid[0]
        all_subtask = db.get_subtasks(itemlist.pk)
        for subtask in all_subtask:
            if subtask !=[]:

                Sub_Task = OneLine_AvatarIcon_ListItem(pk=subtask[1],
                text=f'{subtask[0]}',
            _no_ripple_effect = 1,divider=None, pos_hint={'center_x':.5,'center_y':.5})

                swipe_card = Swipecard(size_hint = (1,None),height =Sub_Task.height-10)

                ''' crea un istansa di MDRelativeLayout '''
                RL_Layout = MDRelativeLayout(size_hint_y = None,height=swipe_card.height,pos_hint={'center_x':.5,'center_y':.5})

                RL_Layout.add_widget(Sub_Task)
                swipe_card.ids.frontbox.add_widget(RL_Layout)
                LISTA_ITEM.add_widget(swipe_card)
        #    

        # self.sm.add_widget(content_task)
       
        
        def transita_to_task_content_screen():
            x = task_content_screen()
            # x.swith_to_contet(itemlist)
            print(x.ids.top_bar.title)
            x.task_id.append(itemlist.pk)
            # print(x.task_id)
            # time.sleep(0.3)
            def cambia_screen():

                self.sm.transition.direction = 'right'
                time.sleep(0.3)
                self.sm.current='task content'
            time.sleep(0.3)
            cambia_screen()
        transita_to_task_content_screen()

    # def acces_to_delet_subtask(self,subtask):
    #     z = Swipecard()
    #     z.delet_sub_task(subtask)
    #     x = self.sm.get_screen('task content')
    #     x.update_num_obbiettivi()
    #     x.lista_obj.pop()
    #     x.num_obj='ciao'
        

        


    def Open_dialog_to_modify_task(self,itemlist):
        self.dialog = MDDialog(title = 'modifica compito'.capitalize(),type ='custom',
        content_cls = Dialog_content())

        ''' modifica la funzione e il comportamento dei bottoni '''
        content = self.dialog.content_cls
        content.ids.salva.text = 'salva modifiche'
        content.ids.cancel.text = 'annulla'

        content.ids.salva.bind(on_press = self.save_modified_task)
        self.LISTA_TASK_TO_MODIFY.append((itemlist.text,itemlist.secondary_text))
        print(self.LISTA_TASK_TO_MODIFY)


        ''' crea un istanza di dialog per accedere ai widget del contenuto '''
        content = self.dialog.content_cls
        content.ids.task_title.text =itemlist.text
        content.ids.task.text =itemlist.secondary_text

        # ''' init the save button e disabilita il b[salva]'''
        # content.ids.save_mod_button.disabled=False
        # content.ids.save_mod_button.bind(on_press = self.save_modified_task)
        # content.ids.salva.disabled = True

        ''' apri il widget [DIALOGO]'''
        self.dialog.open()
        # Clock.schedule_interval(self.check_inputs,0.1)
    
    def close_dialog(self):
        if self.dialog:

            self.dialog.dismiss()
            print('suiiiii')


    def save_modified_task(self,instance):
        try:
            if instance.text == 'salva modifiche':
                content = self.dialog.content_cls
                container = self.root.get_screen('main screen')
                list_element = container.ids['container']
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

                        content.ids.task.text =''
                        content.ids.task_title.text =''
                        # self.close_dialog()
            else:
                # self.close_dialog()
                print(instance.text)
        except Exception as e:
            print(str(e))




    

    # def send_notify(self):

    #     title = 'task aggiunto!'
    #     message = 'dacci dentro'.capitalize()
    #     notification.notify(
    #         title = title,
    #         message = message,
    #         app_name = 'task manager'.title(),
    #         ticker = 'basta procrastinare!!',
    #         timeout = 4
    
    #     )
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

                    container = self.root.get_screen('main screen')
                    container.ids['container'].add_widget(Card)
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

                    container = self.root.get_screen('main screen')
                    container.ids['container'].add_widget(Card)
        except Exception as e:
            print(str(e))
                
    def on_stop(self):
        ''' elimina tutti i widget dal parent'''
        container = self.root.get_screen('main screen')
        for i in container.ids['container'].children:
            container.ids['container'].remove_widget(i)
            print('leavinggg')


        
if __name__=='__main__':
    MainApp().run()


