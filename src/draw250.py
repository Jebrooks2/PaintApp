# Code loosely based on the following open source projects:
# https://github.com/raspberrypilearning/shapes
# https://github.com/mozilla/stoneridge/blob/master/python/src/Demo/tkinter/matt/rubber-band-box-demo-1.py
# https://gist.github.com/nikhilkumarsingh/85501ee2c3d8c0cfa9d1a27be5781f06
import ast
import pickle
try:
    from tkinter import *
    from tkinter.colorchooser import askcolor
    #@todo - you likely need to import some filedialog methods
    from tkinter import filedialog

except ImportError:
    print("tkinter did not import successfully - check you are running Python 3 and that tkinter is available.")
    exit(1)

from circle import Circle
from ellipse import Ellipse
from square import Square
from rectangle import Rectangle
import PIL
from PIL import ImageGrab

class Draw:

    def __init__(self, width, height):

        self.shapes = list()
        self.file_name = None
        self.unsaved = False

        # Set up the root window
        self.root = Tk()
        self.root.title("Draw 250")

        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        submenu = Menu(menubar, tearoff=0)
        # new, open, save, save as
        menubar.add_cascade(label="file", menu=submenu)
        submenu.add_command(label='New', command=self.new_canvas)
        submenu.add_command(label='Open', command=self.open_file)
        submenu.add_command(label='Save', command = self.save)
        submenu.add_command(label='Save As', command=self.save_as)

        
        # Define our layout grid
        self.grid = Frame(self.root)
        self.grid.grid_columnconfigure(7, weight=1)
        self.grid.grid_rowconfigure(3, weight=1)

        # Top level menu buttons

        # @todo  We will eventually want a File menu that allows us to save and load shapes
        # @todo include option to clear canvas (or New canvas) and "save as" or save existing file.


        # @todo - add choice of different shapes
        available_shapes = ['Circle', 'Ellipse', 'Square', 'Rectangle']
        self.shape_choice = StringVar(self.root) # Initialize string to hold value
        self.shape_choice.set(available_shapes[0])  # default value

        self.shape_choice_menu = OptionMenu(self.grid, self.shape_choice, *available_shapes)
        self.shape_choice_menu.grid(row=0,column=2)

        self.fill_color = 'blue'
        self.prior_fill_color = 'blue'

        self.fill_check = BooleanVar(self.root,value=True)
        self.fill_check_box = Checkbutton(self.grid,text='fill', variable=self.fill_check, command=self.fill_toggle)
        self.fill_check_box.grid(row=0, column=3, sticky=E)
        self.fill_check_box.select() # Start checked by default

        self.fill_color_button = Button(self.grid, text='fill color', command=self.choose_fill_color)
        self.fill_color_button.grid(row=0, column=4,sticky=E)

        self.fill_color_button = Button(self.grid, text='edge color', command=self.choose_edge_color)
        self.fill_color_button.grid(row=0, column=5, sticky=E)

        self.fill_canvas = Canvas(self.grid, background=self.fill_color, width=15, height=15)
        self.fill_canvas.grid(row=0, column=5,sticky=W)

        self.edge_color = 'red'

        # @todo - allow to select the edge color as well

        # Row 1 Canvas
        self.canvas = Canvas(self.grid, background='white', width=width, height=height)
        self.canvas.grid(row=1,column=0, columnspan=7)

        self.canvas.bind("<Button-1>" ,       self.select)
        self.canvas.bind("<B1-Motion>",       self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        print("Default shape choice:",self.shape_choice.get())

        # Row 2 Status messages

        # Let's add a label that shows the mouse position
        self.grid.pack()
        print("button height=",self.fill_color_button.winfo_height())

        self.new_shape = self.shape_choice.get()


    def open_file(self):
        try:
            file2 = filedialog.askopenfilename(initialdir=".",
                                               filetypes=[("dwg", "*.dwg")])
            try:
                lmao = pickle.load(open(file2, "rb"))
                print("PICKLE", lmao)
                if lmao is None:
                    print("fuck you")
                self.shapes.clear()
                for shape in lmao:
                    self.shapes.append(shape)
                self.repaint()
            except Exception as e:
                print(e)
        except:
            Exception("This is invalid")


    def save_as(self):
        try:
            self.file_name = filedialog.asksaveasfilename(initialdir=".",
                                            defaultextension='*.dwg',
                                            filetypes=[(".dwg", "*.dwg")])

            if self.file_name is not None:
                self.save_shapes()
        except Exception as e:
            print(e)
            print("WTF???!!?")

    def save_shapes(self):

        try:
            pickle.dump(self.shapes, open(self.file_name, "wb"))
            self.unsaved = False

        except Exception as e:
            print(e)
            print("invalid")

    def save(self):
        if self.file_name is None:
            self.save_as()
        else:
            self.save_shapes()

    def new_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()

    def fill_toggle(self):
        print(" fill checkbox  ", self.fill_check.get())
        if self.fill_check.get():
            self.fill_color = self.prior_fill_color
        else:
            self.fill_color = ''

    def select(self, event):
        """
        On select (button press) we create a temporary shape used to
        draw the stretchy "rubber band" used to define the extents
        :param event:
        :return:
        """
        # used class string methods to create condition on chosen shape type
        lol = Circle(event.x, event.y, dx=0,dy=0,
                                        fill_color=self.fill_color,
                                        edge_color=self.edge_color)
        lmao = Ellipse(event.x, event.y, dx=0,dy=0,
                                        fill_color=self.fill_color,
                                        edge_color=self.edge_color)
        squ = Square(event.x, event.y, dx=0, dy=0,
                                        fill_color=self.fill_color,
                                        edge_color=self.edge_color)
        rect = Rectangle(event.x, event.y, dx=0, dy=0,
                                        fill_color=self.fill_color,
                                        edge_color=self.edge_color)
        print(lol.__str__()[:6])
        print(self.shape_choice)
        if self.shape_choice.get() == lol.__str__()[:6]:
            print(type(self.new_shape))
            print("awetSelect:", event.x, event.y)
            print("Creating ", self.shape_choice.get(), " at (", event.x, ", ", event.y, ") !")
            cls = Circle  # @todo - need to get selected shape definition

            print(" class : ", cls.__name__)
            print("  fill=", self.fill_color, ' edge=', self.edge_color)
            self.new_shape = cls(event.x, event.y, dx=0, dy=0,
                                 fill_color=self.fill_color,
                                 edge_color=self.edge_color)
        if self.shape_choice.get() == lmao.__str__()[:7]:
            print("qwerSelect:" , event.x, event.y)
            print("Creating ",self.shape_choice.get()," at (", event.x,", ",event.y,") !")
            cls = Ellipse # @todo - need to get selected shape definition

            print(" class : ",cls.__name__)
            print("  fill=", self.fill_color, ' edge=', self.edge_color)
            self.new_shape = cls(event.x, event.y, dx=0,dy=0,
                                        fill_color=self.fill_color,
                                        edge_color=self.edge_color)
        if self.shape_choice.get() == squ.__str__()[:6]:
            print(type(self.new_shape))
            print("awetSelect:", event.x, event.y)
            print("Creating ", self.shape_choice.get(), " at (", event.x, ", ", event.y, ") !")
            cls = Square  # @todo - need to get selected shape definition

            print(" class : ", cls.__name__)
            print("  fill=", self.fill_color, ' edge=', self.edge_color)
            self.new_shape = cls(event.x, event.y, dx=0, dy=0,
                                 fill_color=self.fill_color,
                                 edge_color=self.edge_color)
        if self.shape_choice.get() == rect.__str__()[:9]:
            print(type(self.new_shape))
            print("awetSelect:", event.x, event.y)
            print("Creating ", self.shape_choice.get(), " at (", event.x, ", ", event.y, ") !")
            cls = Rectangle  # @todo - need to get selected shape definition

            print(" class : ", cls.__name__)
            print("  fill=", self.fill_color, ' edge=', self.edge_color)
            self.new_shape = cls(event.x, event.y, dx=0, dy=0,
                                 fill_color=self.fill_color,
                                 edge_color=self.edge_color)

        # @todo - need to get selected shape definition

    def drag(self, event):
        """
        A "rubber band" that we stretch to define the shape extents
        :param event:
        :return:
        """
        print("Drag: ",event.x, event.y)
        print(self.new_shape)
        dx = abs(self.new_shape.x - event.x)
        dy = abs(self.new_shape.y - event.y)
        self.new_shape.update(self.canvas, dx, dy, dash_style=(5,5))


    def release(self, event):
        """
        On release, we create the shape and add to list of shapes
        :param event:
        :return:
        """
        # condition to choose which shape class to use on release
        lol = Circle(event.x, event.y, dx=0, dy=0,
                     fill_color=self.fill_color,
                     edge_color=self.edge_color)
        lmao = Ellipse(event.x, event.y, dx=0, dy=0,
                       fill_color=self.fill_color,
                       edge_color=self.edge_color)
        squ = Square(event.x, event.y, dx=0, dy=0,
                       fill_color=self.fill_color,
                       edge_color=self.edge_color)
        rect = Rectangle(event.x, event.y, dx=0, dy=0,
                       fill_color=self.fill_color,
                       edge_color=self.edge_color)
        cls = Circle
        if self.shape_choice.get() == lol.__str__()[:6]:
            cls = Circle
        if self.shape_choice.get() == lmao.__str__()[:7]:
            cls = Ellipse
        if self.shape_choice.get() == squ.__str__()[:6]:
            cls = Square
        if self.shape_choice.get() == rect.__str__()[:9]:
            cls = Rectangle
        #print("Release: ",event.x, event.y)
        dx = abs(self.new_shape.x - event.x)
        dy = abs(self.new_shape.y - event.y)

        self.canvas.delete(self.new_shape.tk_id)

        print("Completing ",self.shape_choice.get()," !")
         # @todo - handle creating the selected shape
        self.add_shape(cls(self.new_shape.x, self.new_shape.y,
                           dx=dx,dy=dy,fill_color=self.fill_color,
                           edge_color=self.edge_color))
        self.repaint()
        self.new_shape = None

    def choose_fill_color(self):
        get_color = askcolor(color=self.fill_color)
        print(" get_color=",get_color)
        self.fill_color = get_color[1]
        self.fill_canvas.configure(background=self.fill_color)
        self.prior_fill_color = self.fill_color
        self.fill_check_box.select() # Selecting color automatically selects fill

    def choose_edge_color(self):
        get_color = askcolor(color=self.edge_color)
        print(" get_color=",get_color)
        self.edge_color = get_color[1]
        # self.prior_fill_color = self.edge_color
        # self.fill_check_box.select() # Selecting color automatically selects fill

    def add_shape(self, shape):
        print("Adding ", shape)
        self.shapes.append(shape)

    def repaint(self):
        print("Repaint the canvas")
        self.canvas.delete("all")

        for shape in self.shapes:
            shape.draw(self.canvas)

        print("Done repainting!")

    def run(self):
        print("     inside Draw run loop ...")
        self.root.mainloop()
        print("     done run!")


if __name__=='__main__':

    # @TODO - YOU MIGHT WANT TO INITIALIZE AVAILABLE SHAPES HERE

    print("Create drawing program for CPSC 250")
    draw = Draw(800, 600)

    draw.repaint()
    draw.run()
    print("Done run loop - call save_shapes ...")

    # @TODO - If you added shapes you might want to give the user option to save to file

    print("Done drawing!")