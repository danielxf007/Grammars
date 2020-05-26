#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# In[4]:


def create_main_window(title, dimensions, resizable):
    window = tk.Tk()
    window.title(title)
    window.geometry(dimensions)
    window.resizable(*resizable)
    return window
        
def create_button(window, name, b_width, b_command):
    return ttk.Button(window, text=name, width=b_width, command=b_command)

def create_text_box(window, t_height, t_width):
    return tk.Text(window, height=t_height, width=t_width)

def create_entry(window, txt_variable, e_width):
    return ttk.Entry(window, textvariable=txtVariable, width=eWidth)

def show_error_message(message_content):
    tk.messagebox.showerror("Error", message_content)

def show_info_message(message_content):
    tk.messagebox.showinfo("Information", message_content)

