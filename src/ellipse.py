from invalid_shape_parameter_error import InvalidShapeParameterError
from circle import Circle


class Ellipse(Circle):
    def __init__(self, x, y, radius=None, fill_color='',edge_color='red',dash_style=None,dx=1, dy=1):

        Circle.__init__(self, x, y, radius=0, fill_color='',edge_color='red',dash_style=None)

        self.edge_color = edge_color
        self.fill_color = fill_color
        self.x_axis = dx
        self.y_axis = dy

    def __str__(self):
        """
        Return special string for circle, not based on ellipse
        :return:
        """

        return Circle.__str__(self) + " (dx={}, dy={}]".format(self.x_axis, self.y_axis)

    def draw(self, canvas):

        print("wtf")
        x0 = self.x - self.x_axis
        y0 = self.y - self.y_axis
        x1 = self.x + self.x_axis + 1  # (x1,y1) is just outside the oval
        y1 = self.y + self.y_axis + 1

        if self.tk_id is not None:
            canvas.delete(self.tk_id)

        self.tk_id = canvas.create_oval(x0, y0, x1, y1, fill=self.fill_color, outline=self.edge_color,
                                        dash=self.dash_style)

    def update(self, canvas, dx, dy, dash_style=(5, 5)):
        self.x_axis = dx
        self.y_axis = dy
        self.dash_style = dash_style
        x0 = self.x - self.x_axis
        y0 = self.y - self.y_axis
        x1 = self.x + self.x_axis + 1  # (x1,y1) is just outside the oval
        y1 = self.y + self.y_axis + 1
        # print(" Updating ",self.__class__.__name__," with ",dx,dy)

        if self.tk_id is not None:
            canvas.delete(self.tk_id)

        self.tk_id = canvas.create_oval(x0, y0, x1, y1,
                                        fill='',
                                        outline=self.edge_color,
                                        dash=self.dash_style)
