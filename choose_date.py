import datetime
from tkinter import Frame, StringVar, Button, Label, Entry, OptionMenu, Tk
from tkinter import simpledialog
from tkcalendar import Calendar


class DateDialog(simpledialog.Dialog):
    def __init__(self, parent, title, selected: datetime.date = datetime.date.today()):
        self.calendar = None
        self.selected_date = selected
        self.parent = parent
        self.type = title
        self.selected_date = selected
        super().__init__(parent, title)

    def body(self, frame):
        horizontal_frame = Frame(self)
        self.calendar = Calendar(frame, selectmode='day',
                                 year=self.selected_date.year, month=self.selected_date.month,
                                 day=self.selected_date.day)
        cancel_button = Button(horizontal_frame, text='Cancel', width=5, command=self.cancel_pressed)
        self.bind('<Escape>', lambda event: self.cancel_pressed())

        self.bind("<<CalendarSelected>>", self.option_changed)  # added this

        self.calendar.pack(side='left')
        cancel_button.pack(side='right')
        horizontal_frame.pack()
        frame.pack()
        return horizontal_frame

    # noinspection PyUnusedLocal
    def option_changed(self, *args):
        self.selected_date = self.calendar.selection_get()  # changed this
        #print(self.selected_date)
        self.destroy()

    def cancel_pressed(self):
        self.selected_date = None
        self.destroy()

    def buttonbox(self):
        pass


def main():
    root = Tk()
    test = DateDialog(root, 'testing', datetime.datetime(2024, 9, 1, 20)).selected_date
    root.mainloop()


if __name__ == '__main__':
    main()