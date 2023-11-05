

from kivymd.app import MDApp
from kivymd.uix.card import MDCard,MDCardSwipe,MDCardSwipeFrontBox,MDCardSwipeLayerBox
from kivy.lang.builder import Builder
from kivymd.uix.bottomsheet import MDBottomSheet

from kivy.properties import StringProperty
KV = '''
MDScreen:
    MDBoxLayout:
        id : box
    

<carswipe_item_delet>:
    size_hint_y: None
    height: 80
    type : 'hand'
    anchor : 'left'
    
    md_bg_color : 'yellow'
    swipe_distance : 50
    # max_opened_x : 10
    max_swipe_x : 0
    pos_hint : {'center_x':.5,'center_y':.5}
    

    MDCardSwipeLayerBox:
        padding : 10
        MDIcon:
            icon : root.icon
            pos_hint : {'center_x':.5,'center_y':.5}
    MDCardSwipeFrontBox:
        md_bg_color : 'black'
        MDRelativeLayout:
            MDList:
                id : content
                ThreeLineAvatarIconListItem:
                    text : 'Scorri per eleiminare'.capitalize()
                    theme_text_color : 'Custom'
                    text_color : 'white'
                    _no_ripple_effect : 1

                    # CheckboxLeftWidget:
                      
                    #     icon_color : 'blue'

                    
        
        






'''





class carswipe_item_delet(MDCardSwipe):
    icon = StringProperty('trash-can')


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)
    def on_start(self):
        self.root.ids['box'].add_widget(carswipe_item_delet())
    
if __name__ =='__main__':
    MainApp().run()
    


