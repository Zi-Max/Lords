import pygame
from UiFunctions import *

######################## Main Element ##############################
####################################################################
class PyRect(UiDesgin):
    def __init__(self, group, name, size, pos, grab="", uiPrefix="", frame=""):
        self.name = f"{uiPrefix}{name}"
        self.group = group

        self.checkGroup()
        self.checkInc()

        self.attObj = None
        self.setFrame(frame)

        self.rect = super().setGeo(size, pos, grab)
        self.border_rect = super().setGeo(size, pos, grab)

        self.ren_text, self.rect_text = super().setText(self.rect)
        self.text_align = "center"

        self.active_color = "#FFFFFF"

        self.border_width = 0
        self.border_color = "#000000"
        super().setBorder(self.border_width, self.border_color)

        self.text_margin_x = 0
        self.text_margin_y = 0

        self.layer = 1

        draw_dict[group].update({self.name : self})

    def checkInc(self):
        if self.group[0:3] == "INC":
            try:
                inc_dict[self.group]
            except KeyError:
                inc_dict.update({self.group : 0})
            self.name = f"{inc_dict[self.group]}{self.name}"
            inc_dict[self.group] += 1

    def checkGroup(self):
        try:
            draw_dict[self.group]
        except KeyError:
            draw_dict.update({self.group : {}})

    def setFrame(self, frame):
        if frame == "":
            self.frame = None
        else:
            self.frame = draw_dict[self.group][frame]
            draw_dict[self.group][frame].children.append(self)

######################## Derived Elements ##############################
########################################################################
######################## Pygame Shapes #################################
class PyCircle(PyRect):
    def __init__(self, group, name, radius, pos, grab="", frame=""):
        super().__init__(group, name, (0, 0), pos, grab, "CI", frame)
        self.radius = radius

######################## My Ui Elements ##############################
class PyButton(PyRect):
    def __init__(self, group, name, size, pos, grab="", frame=""):
        super().__init__(group, name, size, pos, grab, "BT", frame)

        self.base_color = "#FFFFFF"
        self.active_color = self.base_color
        self.hover_color = "#999999"
        self.select_color = "#666666"
        self.disabled_color = "#333333"

        self.disabled = False

class PyProgressBar(PyRect):
    def __init__(self, group, name, width, pos, grab="", uiPrefix="", frame=""):
        super().__init__(group, name, (0, 0), pos, grab, uiPrefix, frame)

        bar_pos = super().setGeo((0, 0), pos, grab, False)
        bar_fill_pos = super().setGeo((0, 0), pos, grab, False)
        self.rect = super().setVector((width * 30, 15), bar_pos[0], grab)
        self.bar_fill_rect = super().setVector((width * 30, 15), bar_fill_pos[0], grab)

        self.start_pos = self.rect.centerx - self.rect.width / 2
        self.end_pos = self.rect.centerx + self.rect.width / 2
        self.precent = 0

        self.bar_color = "#FFF000"
        self.bar_fill_color = "#333333"

        self.disabled = False

    def setSlider(self, new_precent):
        self.precent = new_precent
        self.bar_fill_rect.width = self.handle_rect.x - self.start_pos

class PySlider(PyProgressBar):
    def __init__(self, group, name, width, pos, grab="", frame=""):
        super().__init__(group, name, width, pos, grab, "SL", frame)
        handle_pos = super().setGeo((0, 0), pos, grab, False)

        self.handle_rect = super().setVector((15, 20), handle_pos[0], grab)

        self.handle_color = "#FFFFFF"

    def setSlider(self, new_precent):
        self.precent = new_precent
        self.handle_rect.x = self.start_pos + (self.rect.width * self.precent)
        self.bar_fill_rect.width = self.handle_rect.x - self.start_pos

class PyFrame(PyRect):
    def __init__(self, group, name, size, pos, grab):
        super().__init__(group, name, size, pos, grab, "FR")

        self.children = []

    def moveChildren(self, x, y):
        for child in self.children:
            child.addMargin(x, y)
