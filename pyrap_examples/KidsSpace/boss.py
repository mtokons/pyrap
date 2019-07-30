
import pyrap
from pyrap.layout import RowLayout, ColumnLayout, CellLayout
from pyrap.ptypes import Color
from pyrap.widgets import Shell, Label, Button, Composite, Canvas, Group


class HelloWorld:
    '''My pyRAP application'''

    def main(self, **kwargs):
        shell = Shell(title='Welcome to pyRAP', minwidth=500, minheight=400)
        shell.content.layout = CellLayout(halign='fill', valign='fill')
        canvas = Canvas(shell, halign='fill', valign='fill')
        context = canvas.gc
        canvas << context.draw_grid(10, 10, 'lightgrey')

        canvas << context.begin_path()
        canvas << context.rect(50, 50, 300, 100)
        canvas << context.fill_style(Color('white'))
        canvas << context.fill()
        canvas << context.linewidth(1)
        canvas << context.stroke_style(Color('black'))
        canvas << context.stroke()

        canvas << context.fill_style(Color('red'))
        canvas << context.font('Arial', 30)
        canvas << context.stroke_text("Hello World!\nThis is Awesome!", 200, 100, aligncenterx=True, aligncentery=True)

        canvas << context.begin_path()
        canvas << context.rect(50, 150, 300, 100)
        canvas << context.fill_style(Color('light grey'))
        canvas << context.fill()
        canvas << context.linewidth(1)
        canvas << context.stroke_style(Color('black'))
        canvas << context.stroke()

        canvas << context.fill_style(Color('green'))
        canvas << context.font('Arial', 30)
        canvas << context.fill_text("Hello World!\nThis is Awesome!", 60, 200, aligncenterx=False, aligncentery=True)
        canvas.draw()
        # # multiple content
        # shell.content.layout = RowLayout(halign='fill', valign='fill', flexrows=0)
        # Label(shell.content, 'Hello, world!')
        # #shell.bg = Color('blue')
        # comp = Composite(shell.content)
        # comp.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)# equalwidths=True
        # comp.bg = Color('blue')


        shell.on_resize += shell.dolayout
        # Button make
        # btn = Button(comp, 'Click Me', halign='fill', valign='fill')
        # btn1 = Button(comp, 'Click Me2', halign='fill', valign='fill')
        shell.show(True)


def main():
    pyrap.register(clazz=HelloWorld,
                   entrypoints={'start': HelloWorld.main},
                   path='helloworld',
                   name='Button')
    pyrap.run()


if __name__ == '__main__':
    main()
