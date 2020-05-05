#!/usr/bin/env python
# coding: utf-8

# In[1]:


def add_list_no_repeated_elements(list_1, list_2):
    return list_1 + list(filter(lambda x: not x in list_1, list_2))

