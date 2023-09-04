from django import template
import datetime
from django.utils import timezone
import math

register = template.Library()

def age(bday, d=None):
    if d is None:
        d = datetime.date.today()
    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
register.filter('age', age)

def multiply(num1,num2) ->int:
    return num1*num2
register.filter('multiply', multiply)

def get_list_item(arr,index):
    return arr[index-1]
register.filter('get_list_item',get_list_item)

def get_list_item_abs(arr,index):
    return arr[index]
register.filter('get_list_item_abs',get_list_item_abs)

def parent_path_name(path_info):
    ''' 
    returns a string of characters that appear after the first / but before the index of the second one.
    To avoid a ValueError when checking for the first occurence of / after index[1], we append / to the string
    '''
    return "".join([c if not c=="/" and list(path_info.lower()+str('/')).index('/',1)>=counter else '' for counter,c in enumerate(list(path_info.lower()+str('/')))])

register.filter('parent_path_name',parent_path_name)

def addclass(field, given_class):
    existing_classes = field.field.widget.attrs.get('class', None)
    if existing_classes:
        if existing_classes.find(given_class) == -1:
            # if the given class doesn't exist in the existing classes
            classes = existing_classes + ' ' + given_class
        else:
            classes = existing_classes
    else:
        classes = given_class
    return field.as_widget(attrs={"class": classes})
register.filter('addclass',addclass)

def as_words(text):
    return "".join([c if not c=="_" else ' ' for counter,c in enumerate(list(text.lower()+str('_')))])
register.filter('as_words',as_words)

def get_html_type(field):
    field = str(field).replace('','')
    if 'type=' not in field:
        return None
    else:
        fl=field.split(' ')
        for i in fl:
            if 'type=' in i:
                fl=(i.replace('type=','')).replace('"','')
                break
                
        return fl
register.filter('get_html_type',get_html_type)

def mask_text_ends(txt):
    try:        
        txtlen = len(list(str(txt)))
        return "".join([i if not counter<math.floor(txtlen/4) and not counter>=(txtlen-math.floor(txtlen/4)) else '*' for counter,i in enumerate(list(str(txt)))])
    except:
        return
    
register.filter('mask_text_ends',mask_text_ends)

def mask_text_mid(txt):
    try:        
        txtlen = len(list(str(txt)))
        return "".join(['*' if not counter<math.floor(txtlen/4) and not counter>=(txtlen-math.floor(txtlen/4)) else i for counter,i in enumerate(list(str(txt)))])
    except:
        return
    
register.filter('mask_text_mid',mask_text_mid)

def multiply_str(txt,occurences):
    try:        
        return str(txt)*int(occurences)
    except:
        return
    
register.filter('multiply_str',multiply_str)

def is_even(num):
    try:        
        return True if int(num) % 2 == 0 else False
    except:
        return
    
register.filter('is_even',is_even)

def time_greeting(t):
    try:
        current_time = timezone.localtime().hour
        if current_time < 12:
            return str(t) + 'Morning'
        elif current_time >=12 and current_time < 17:
            return str(t) + 'Afternoon'
        elif current_time >=17 and current_time < 24:
            return str(t) + 'Evening'
        else:
            return str(t) + 'Day'
    except:
        return t
    
register.filter('time_greeting',time_greeting)