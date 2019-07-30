import os

from pyrap import session

import pyrap
from pyrap.layout import ColumnLayout, RowLayout, StackLayout
from pyrap.ptypes import Color, Pixels, Image
from pyrap.pwt.audio.audio import Audio
from pyrap.pwt.video.video import Video
from pyrap.widgets import Shell, Label, Composite, Button


class MultiPage:
    '''My pyRAP application'''

    def __init__(self):
        self.visible = 0  # initialize variable that indicates which page is visible

    def main(self, **kwargs):
        self._shell = Shell(maximized=True, titlebar=False)
        self._shell.bg = Color('red')
        self._shell.on_resize += self._shell.dolayout

        comp_mainframe = Composite(self._shell.content)
        comp_mainframe.layout = RowLayout(halign='fill', valign='fill', flexrows=0, vspace=0)

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # HEADER - we may not need this.. or maybe we do. You decide.
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        comp_header = Composite(comp_mainframe)
        comp_header.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True, padding=Pixels(0))
        comp_header.bg = Color('black')

        btn_switch1 = Button(comp_header, text='Back', halign='fill', valign='fill')
        btn_switch = Button(comp_header, text='Next', halign='fill', valign='fill')
        lbl_header = Label(comp_header, text='<b>Click button to switch pages!</b>', markup=True, halign='fill', valign='fill')
        lbl_header.bg = 'transp'
        lbl_header.color = Color('white')

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # BODY - this is the 'main' composite that for the content. The visibility of the composites inside changes
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        self.comp_body = Composite(comp_mainframe, border=True)
        self.comp_body.layout = StackLayout(halign='fill', valign='fill')
        self.comp_body.bg = Color('white')

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # HOME PAGE #
        self.comp_home = Composite(self.comp_body)
        self.comp_home.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        #self.comp_home.bg = Color('blue')
        self.comp_home.bgimg = Image(os.path.join('images', 'al_2.jpg'))
        self.comp_home.bgsize = 'cover'
        self.comp_home.visible = True
        btn_showdialog = Button(self.comp_home, text='Show Dialog1')
        btn_showdialog = Button(self.comp_home, text='Show Dialog2')
        btn_showdialog = Button(self.comp_home, text='Show Dialog3')

        lbl_wnd = Label(self.comp_home, text='Page 1 Google Search, also referred to as \n Google Web Search or simply Google,\n'
                                            'web search engine developed by Google LLC. \n \n '
                                             'It is the most used search engine on the World Wide Web across all platforms, <br />'
                                             '\n \n with 92.74% market share as of October 2018,\n handling more than 3.5 billion searches each day.'
                                             , markup=False, multiline=True)
        lbl_wnd.font = lbl_wnd.font.modify(size=16)
        lbl_wnd.color = Color("#00ff00")

        btn_showdialog = Button(self.comp_home, text='Show Dialog4')
        btn_showdialog = Button(self.comp_home, text='Show Dialog5')

        #lbl_wnd = Label(cmp_dialog, text='Blafasel <b> This is really important</b>', markup=True, valign='fill', halign='fill')
        #lbl_wnd.bg = Color('red')


        comp_home_s1 = Composite(self.comp_home)
        comp_home_s1.layout = RowLayout(flexrows=0, halign='fill', valign='fill')

        comp_home_s1.bg = Color('blue')
        comp_home_s1.bgimg = Image(os.path.join('..', 'KidsSpace', 'images', 'al_m_1.jpg'))
        comp_home_s1.bgsize = 'cover'
        comp_home_s1.visible = True
        btn_showdialog11 = Button(comp_home_s1, text='Show Dialog6', halign='fill', valign='fill')



        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # 2nd PAGE #
        self.comp_second = Composite(self.comp_body)
        self.comp_second.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_second.bg = Color('green')
        self.comp_second.visible = True
        self.comp_second.bgimg = Image(os.path.join('images', 'al_8.jpg'))
        self.comp_second.bgsize = 'cover'
        xxx = Label(self.comp_second, text='<b>Page 2</b>', markup=True)

        btn_showdialog = Button(self.comp_second, text='Show Dialog1', halign='fill', maxwidth=100)
        btn_showdialog = Button(self.comp_second, text='Show Dialog')
        btn_showdialog1 = Button(self.comp_second, text='Show Dialog', halign='fill', valign='fill')

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # THIRD PAGE #
        self.comp_third = Composite(self.comp_body)
        self.comp_third.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_third.bg = Color('yellow')
        self.comp_third.bgimg = Image(os.path.join('images', 'al_3.jpg'))
        #self.comp_third.bgsize = 'cover'
        self.comp_third.visible = True
        #Label(self.comp_third, text='<b>Page 3</b>', markup=True)

        comp_third_field = Composite(self.comp_third)
        comp_third_field.layout = RowLayout(flexrows=1, halign='fill', valign='fill')
        #comp_third_field.bgimg = Image(os.path.join('images', 'al_3.jpg'))
        #comp_third_field.bgsize = 'cover'

        comp_btn = Composite(comp_third_field)
        comp_btn.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)
        btn_clear = Button(comp_btn, text='Clear', halign='fill', valign='fill')
        btn_reload = Button(comp_btn, text='Reload', halign='fill', valign='fill')
        btn_download = Button(comp_btn, text='Download', halign='fill', valign='fill')

        comp_third_field1 = Composite(comp_third_field)
        comp_third_field1.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        Label(comp_third_field1, img=Image(os.path.join('images', 'al_s_1.jpg')))
        Label(comp_third_field1, img=Image(os.path.join('images', 'al_m_1.jpg')))
        comp_third_field1.visible = True
        comp_third_field1.bgimg = Image(os.path.join('images', 'al_3.jpg'))
        #comp_third_field1.bgsize = 'cover'

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # 4th PAGE #

        self.comp_four = Composite(self.comp_body)
        self.comp_four.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_four.bg = Color('yellow')
        self.comp_four.bgimg = Image(os.path.join('images', 'al_1.jpg'))
        self.comp_four.bgsize = 'cover'
        self.comp_four.visible = True
        # Label(self.comp_third, text='<b>Page 3</b>', markup=True)

        comp_four_field = Composite(self.comp_four)
        comp_four_field.layout = ColumnLayout(flexcols=1, halign='fill', valign='fill')
        # comp_third_field.bgimg = Image(os.path.join('images', 'al_3.jpg'))
        # comp_third_field.bgsize = 'cover'

        #Audio

        comp_four_btn = Composite(comp_four_field)
        comp_four_btn.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)
        btn_play = Button(comp_four_btn, text='Play Audio', halign='fill', valign='fill')
        btn_pause = Button(comp_four_btn, text='Pause Audio', halign='fill', valign='fill')
        #btn_download = Button(comp_four_btn, text='Download', halign='fill', valign='fill')

        v = Audio(self.comp_four, halign='fill', valign='fill')
        v.addsrc({'source': 'Audio/test.mp3', 'type': 'audio/mpeg'})

        def play(*_):
            v.play()

        def pause(*_):
            v.pause()


        btn_play.on_select += play
        btn_pause.on_select += pause

        #Audio End

        comp_four_field1 = Composite(comp_four_field)
        comp_four_field1.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        #Label(comp_four_field1, img=Image(os.path.join('images', 'al_s_1.jpg')))
        #Label(comp_four_field1, img=Image(os.path.join('images', 'al_m_1.jpg')))
        comp_four_field1.visible = True
        comp_four_field1.bgimg = Image(os.path.join('images', 'al_1.jpg'))
        comp_four_field1.bgsize = 'cover'


        #Video

        comp_four_btn2 = Composite(comp_four_field)
        comp_four_btn2.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)

        comp_four_btn3 = Composite(comp_four_btn2)
        comp_four_btn3.layout = RowLayout (halign='fill', valign='fill', equalheights=True)

        btn_play1 = Button(comp_four_btn3, text='Play Video', halign='fill', valign='fill')
        btn_play2 = Button(comp_four_btn3, text='Play Video', halign='fill', valign='fill')
        #btn_pause1 = Button(comp_four_btn2, text='Pause', halign='fill', valign='fill')

        comp_body1 = Composite(comp_four_field)
        comp_body1.layout = RowLayout(halign='fill', valign='fill', flexrows=0)



<<<<<<< HEAD
=======
<<<<<<< HEAD

=======
>>>>>>> b241de47e7b3afc9aff29d66ef27dec5d133b5df
>>>>>>> origin/master

        def video_window(*_):

            wnd_dialog = Shell(parent=self._shell, titlebar=True, border=True, resize=False, modal=True,
                               halign='center', valign='center')
            wnd_dialog.create_content()
            wnd_dialog.content.bg = Color('white')

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            wnd_dialog.bounds = w / 2 - 200, h / 2 - 150, 400, 300

            cmp_dialog = Composite(wnd_dialog.content)
            cmp_dialog.layout = RowLayout(valign='fill', halign='fill', flexrows=1)

<<<<<<< HEAD
            lbl_wnd = Label(cmp_dialog, text='Blafasel <b> This is a video/b>', markup=True, valign='fill', halign='fill')
            lbl_wnd.bg = Color('red')
            v1 = Video (cmp_dialog, halign='fill', valign='fill')
=======
<<<<<<< HEAD
            v1 = Video(cmp_dialog, halign='fill', valign='fill')
=======
            lbl_wnd = Label(cmp_dialog, text='Blafasel <b> This is a video/b>', markup=True, valign='fill', halign='fill')
            lbl_wnd.bg = Color('red')
            v1 = Video (cmp_dialog, halign='fill', valign='fill')
>>>>>>> b241de47e7b3afc9aff29d66ef27dec5d133b5df
>>>>>>> origin/master
            v1.addsrc({'source': 'video/test.mp4', 'type': 'video/mp4'})

            def play1(*_):
                v1.play()

            def pause1(*_):
                v1.pause()
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> origin/master

            btn_play1 = Button(cmp_dialog, text='Play', halign='fill', valign='fill')
            btn_pause1 = Button(cmp_dialog, text='Pause', halign='fill', valign='fill')


            #def dosomething(*_):
                #lbl_wnd.text = '<b>I did something!</b>'

<<<<<<< HEAD
=======
>>>>>>> b241de47e7b3afc9aff29d66ef27dec5d133b5df
>>>>>>> origin/master


            #btn_dosomething = Button(cmp_dialog, text='Do something', valign='fill', halign='fill')

            #btn_dosomething.on_select += dosomething

            wnd_dialog.show()

<<<<<<< HEAD
=======

>>>>>>> origin/master
            btn_play1.on_select += play1
            btn_pause1.on_select += pause1

        btn_play1.on_select += video_window

    # video end




        def resize_bg (*_):

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            self.comp_home.bgimg = self.comp_home.bgimg.resize(width= Pixels(w), height=Pixels(h))
            self.comp_second.bgimg = self.comp_second.bgimg.resize(width=Pixels(w), height=Pixels(h))
            self.comp_third.bgimg = self.comp_third.bgimg.resize(width=Pixels(w), height=Pixels(h))
            self.comp_four.bgimg = self.comp_four.bgimg.resize(width=Pixels(w), height=Pixels(h))
            print(w,h)
            self._shell.dolayout()


        # LISTENER FUNCTION TO SWITCH PAGE VISIBILITY
        def open_menu(*_):
            self.visible = (self.visible + 1) % 4  # if you don't understand this, learn about the modulo operator (Euclidean division)

            # switch the Four pages all around
            self.comp_home.visible = self.visible == 0
            self.comp_home.layer = (0 - self.visible) % 4
            self.comp_second.visible = self.visible == 1
            self.comp_second.layer = (1 - self.visible) % 4
            self.comp_third.visible = self.visible == 2
            self.comp_third.layer = (2 - self.visible) % 4
            self.comp_four.visible = self.visible == 3
            self.comp_four.layer = (3 - self.visible) % 4

        # LISTENER FUNCTION TO SWITCH PAGE VISIBILITY
        def back_menu(*_):
            self.visible = (self.visible - 1) % 4  # if you don't understand this, learn about the modulo operator (Euclidean division)

            # switch the Four pages all around
            self.comp_home.visible = self.visible == 0
            self.comp_home.layer = (0 - self.visible) % 4
            self.comp_second.visible = self.visible == 1
            self.comp_second.layer = (1 - self.visible) % 4
            self.comp_third.visible = self.visible == 2
            self.comp_third.layer = (2 - self.visible) % 4
            self.comp_four.visible = self.visible == 3
            self.comp_four.layer = (3 - self.visible) % 4

        def showdialog(*_):
            # this will create a new dialog every time the button is clicked. You can also create it when setting
            # up the layout and set its visibility to false after calling wnd_dialog.show(), then set the visibility
            # to true in the listener function that is called when the button is clicked (will only work if the window
            # was hidden before. Closing the window will destroy the widget and an error will be thrown when trying
            # to make it visible again.
            wnd_dialog = Shell(parent=self._shell, titlebar=True, border=True, resize=False, modal=True,
                               halign='center', valign='center')
            wnd_dialog.create_content()
            wnd_dialog.content.bg = Color('white')

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            wnd_dialog.bounds = w / 2 - 200, h / 2 - 150, 400, 300

            cmp_dialog = Composite(wnd_dialog.content)
            cmp_dialog.layout = RowLayout(valign='fill', halign='fill', flexrows=0)

            lbl_wnd = Label(cmp_dialog, text='Blafasel <b> This is really important</b>', markup=True, valign='fill', halign='fill')
            lbl_wnd.bg = Color('red')

            def dosomething(*_):
                lbl_wnd.text = '<b>I did something!</b>'

            btn_dosomething = Button(cmp_dialog, text='Do something', valign='fill', halign='fill')
            btn_dosomething.on_select += dosomething

            wnd_dialog.show()

        def showdialog1(*_):

            # Start Window1

            wnd_dialog1 = Shell(parent=self._shell, titlebar=True, border=True, resize=False,
                               halign='center', valign='center')
            wnd_dialog1.create_content()
            wnd_dialog1.content.bg = Color('white')

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            wnd_dialog1.bounds = w / 2 - 100, h / 3 - 150, 250, 250

            cmp_dialog1 = Composite(wnd_dialog1.content)
            cmp_dialog1.layout = RowLayout(valign='fill', halign='fill', flexrows=0)

            lbl_wnd1 = Label(cmp_dialog1, text='Blafasel <b> This is really important</b>', markup=True,
                             valign='fill', halign='fill')
            lbl_wnd1.bg = Color('black')

            def dosomething1(*_):
                lbl_wnd1.text = '<b>I did something!</b>'

            btn_dosomething1 = Button(cmp_dialog1, text='Do something', valign='fill', halign='fill')
            btn_dosomething1.on_select += dosomething1

            wnd_dialog1.show()

            # End window1

            # Start Window2

            wnd_dialog2 = Shell(parent=self._shell, titlebar=True, border=True, resize=False,
                                halign='top', valign='top')
            wnd_dialog2.create_content()
            wnd_dialog2.content.bg = Color('blue')

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            wnd_dialog2.bounds = w / 2 - 200, h / 1 - 350, 250, 250

            cmp_dialog2 = Composite(wnd_dialog2.content)
            cmp_dialog2.layout = RowLayout(valign='fill', halign='fill', flexrows=0)

            lbl_wnd2 = Label(cmp_dialog2, text='Blafasel \n Its my life</b>', markup=False,
                            valign='fill', halign='fill')
            lbl_wnd2.bg = Color('blue')
            lbl_wnd2.bgimg = Image(os.path.join('images', 'al_2.jpg'))

            wnd_dialog2.show()

            # End window1

            def dosomething1(*_):
                lbl_wnd1.text = '<b>I did something!</b>'

            btn_dosomething1 = Button(cmp_dialog1, text='Do something', valign='fill', halign='fill')
            btn_dosomething1.on_select += dosomething1

            wnd_dialog1.show()





        # assign listener function to button click
        btn_switch.on_select += open_menu
        btn_switch1.on_select += back_menu
        btn_showdialog.on_select += showdialog
        btn_showdialog1.on_select += showdialog1
        btn_showdialog11.on_select += showdialog1
        xxx.on_mouseup += showdialog1


        self._shell.show()


def main():
    pyrap.register(clazz=MultiPage,
                   entrypoints={'start': MultiPage.main},
                   path='kidsApp',
                   name='Space Station for kids!')
    pyrap.run()


if __name__ == '__main__':
    main()
