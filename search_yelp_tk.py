import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox


class Getopt(tk.Frame):
    ''' Popup dialog for seach option.'''
    def __init__(self, parent):
        # Define properties for input data.
        self.parent = parent
        self.yelp_area = tk.StringVar()
        self.yelp_keyword = tk.StringVar()
        self.yelp_dist = tk.IntVar()

        # Set default values to properties.
        self.set_init_val()

        frame = tk.Frame(parent, bd=10)
        ft = font.Font(weight='bold', size=10)
        lab = tk.Label(frame, text="Listing Businesses from Yelp",
                        fg="#555555", font=ft)
        lab.grid(row=0, columnspan=3, ipadx=3, ipady=20)

        l_area = tk.Label(frame, text="Area, suburb")
        l_area.grid(row=1, column=0, columnspan=2, sticky='E', ipady=3, ipadx=2)
        area = tk.Entry(frame, textvariable=self.yelp_area, width=40)
        area.grid(row=1, column=2, columnspan=3, ipady=3, ipadx=2)

        l_keyword = tk.Label(frame, text="Keyword, category")
        l_keyword.grid(row=2, column=0, columnspan=2, sticky='E', ipady=3, ipadx=2)
        keyword = tk.Entry(frame, textvariable=self.yelp_keyword, width=40)
        keyword.grid(row=2, column=2, columnspan=3, ipady=3, ipadx=2)

        l_distance = tk.Label(frame, text="Distance")
        l_distance.grid(row=3, column=0, sticky='E', pady=3)
        within4km = tk.Radiobutton(frame, text="Within 4 km",
                                    variable=self.yelp_dist, value=2)
        within4km.grid(row=3, column=2, pady=3)
        within2km = tk.Radiobutton(frame, text="Within 2 km",
                                    variable=self.yelp_dist, value=3)
        within2km.grid(row=3, column=3, pady=3)
        within500m = tk.Radiobutton(frame, text="Within 500 m",
                                    variable=self.yelp_dist, value=4)
        within500m.grid(row=3, column=4, pady=3)

        self.yelp_filename = tk.StringVar()
        l_filename = tk.Label(frame, text="Output file")
        l_filename.grid(row=4, column=0, sticky='E', pady=3)
        filename = tk.Entry(frame, textvariable=self.yelp_filename, width=40)
        filename.grid(row=4, column=2, columnspan=3, pady=10)
        filebutton = tk.Button(frame, text="Find",
                                command=self.savefile_search, width=8)
        filebutton.grid(row=4, column=5, pady=10, padx=3)

        button = tk.Button(frame, text="Execute", width=8, font=ft,
                            command=self.get_options)
        button.grid(row=5, column=2, pady=40)
        button2 = tk.Button(frame, text="Quit", width=8, command=self.quit_search)
        button2.grid(row=5, column=4, pady=40)

        frame.pack()

    def set_init_val(self):
        ''' Set initial value for options.'''
        self.yelp_area.set('Perth')
        self.yelp_dist.set(3)

    def savefile_search(self):
        ''' Set filename specified by filedialog to yelp_filename(StringVar())'''
        self.yelp_filename.set(filedialog.asksaveasfilename())

    def get_options(self):
        ''' Get options specified by Popup dialog and return as Dict.
            If output filename is not set, show message window.
        '''

        if not self.yelp_filename.get():
            messagebox.showwarning(message='Specify an output file to save the list.',
                                    title='Notification'
                                    )
            return

        print("Area = {}, Keyword = {}, distance = {}, savefile = {}".format(
                                                        self.yelp_area.get(),
                                                        self.yelp_keyword.get(),
                                                        self.yelp_dist.get(),
                                                        self.yelp_filename.get()),
                                                        flush=True)
        self.parent.destroy()
        self.exe_flag = True # Options are set properly.

    def quit_search(self):
        ''' Close the window.'''

        self.parent.destroy()
        self.exe_flag = False # Option setting failed.


def select_option():
    ''' Main function for Popup window for setting search options.'''

    window = tk.Tk()
    frame = Getopt(window)
    window.mainloop()

    if frame.exe_flag:  # Options are got properly.
        # print('area:{}, key:{}, dist:{}, filename:{}'.format(frame.yelp_area.get(),
        #                                             frame.yelp_keyword.get(),
        #                                             frame.yelp_dist.get(),
        #                                             frame.yelp_filename.get()),
        #                                             flush=True)
        return {'area' : frame.yelp_area.get(),
            'keyword' : frame.yelp_keyword.get(),
            'distance' : frame.yelp_dist.get(),
            'savefile' : frame.yelp_filename.get()}
    else:
        return {}


class ProgIndicator(tk.Tk):
    ''' Progress Indicator shown during search.'''
    def __init__(self, parent):
        self.parent = parent

        parent.geometry(self.center_window(parent, 300, 100))
        f = tk.Frame(parent, cursor='watch')

        #self.prog = Progressbar(parent, orient='horizontal', mode='indeterminate',
        #                        length=100)
        #self.prog.pack()

        msg_head = tk.Label(f, text='Collecting information from yelp.')
        msg_head.grid(row=0, pady=10)

        self.msg_text= tk.StringVar()
        self_msg_text=''
        msg = tk.Label(f, textvariable = self.msg_text)
        msg.grid(row=1, pady=10)

        f.pack()

    def center_window(self, parent, w, h):
        ''' Caliculate the position to center the window.'''
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        return '{}x{}+{}+{}'.format(w, h, x, y)

    def set_num_to_msg(self, num):
        ''' Show message how many businesses have found.'''
        self.msg_text.set('{} businesses found!'.format(num))
        self.parent.update()

    def set_msg(self, msg):
        ''' Show any text message on the indicator.'''
        self.msg_text.set(msg)
        self.parent.update()

def create_indicator():
    root = tk.Tk()
    return ProgIndicator(root)
