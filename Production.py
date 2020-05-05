#!/usr/bin/env python
# coding: utf-8

# In[2]:


class Production:
    def __init__(self, left_side, right_side):
        self.left_side = left_side #Non terminal of the form <str>
        self.right_side = right_side #Array of terminals and non terminals, empty sequence 
    
    def get_left_side(self):
        return self.left_side
    
    def get_right_side(self):
        return self.right_side
    


# In[ ]:




