import random
import sqlite3
import PySimpleGUI as sg
from datetime import datetime

# connect to the DB
con = sqlite3.connect('CS281_Stage3.db')
cur = con.cursor()

# global variables
login_user_id = -1
login_user_name = -1
login_user_surname= -1
login_user_role= ""
aucList = []

# window functions

###Main ###  
def Main():
    choices = ('SELLER', 'BUYER', 'ADMIN')
    layout = [[sg.Text('Welcome to the Online Auction System! Please enter your role.')],
              [sg.Combo(choices, size=(15, len(choices)), key='chosen_role')],
              [sg.Button('To Login')],
              [sg.Button('Create Account Window')]]
    
    return sg.Window('Main Window', layout)
            
def set_role(values):
    global window
    global login_user_role
    if not values['chosen_role']:
        sg.popup('Please choose a role.')

    login_user_role = values['chosen_role']
    window.close()
    window = window_login()


###Registering#####
def window_register():

    layout = [[sg.Text('Please enter your information.')],
        [sg.Text('SSN:',size =(16,1)), sg.Input(size=(20,1), key='ssn2')],
        [sg.Text('Password:', size =(16,1)), sg.Input(size=(20,1), key='password2')],
        [sg.Text('Name:', size =(16,1)), sg.Input(size=(20,1), key='name')],
        [sg.Text('Last Name:', size =(16,1)), sg.Input(size=(20,1), key='last_name')],
        [sg.Text('Date Of Birth:', size =(16,1)), sg.Input(size=(20,1), key='date_of_birth')],
        [sg.Text('IBAN:', size =(16,1)), sg.Input(size=(20,1), key='iban')],
        [sg.Button('Create Account'),sg.Button('Return to Main Window')]]

    return sg.Window("Register Window", layout)

def button_to_account_create(values):
    global window
    global login_user_role
    if not values['chosen_role']:
        sg.popup('Please choose a role.')
        window.close()
        window = Main()
        return

    login_user_role = values['chosen_role']
    window.close()
    window = window_register()    

def button_create_account(values):
    global window  
    global login_user_role

    if not (values['ssn2'] or values['password2'] or values['name'] or values['last_name'] or values['date_of_birth'] or values['iban']): 
        sg.popup("bad creditientials!") 
        window.close()
        window = Main()
        return  

    data = (int(values['ssn2']), values['password2'], values['name'], values['last_name'], values['date_of_birth'], values['iban'])
    sql = """INSERT OR IGNORE INTO """ + login_user_role + """ (
                       SSN,
                       PASSWORD,
                       FIRST_NAME,
                       LAST_NAME,
                       DATE_OF_BIRTH,
                       IBAN
                   )
                   VALUES (
                       ?,
                       ?,
                       ?,
                       ?,
                       ?,
                       ?
                   );"""    

    cur.execute(sql, data)
    sg.popup("Account Created")    
    window.close()
    window = Main()


###LOGGING IN###
def window_login():
    
    layout = [[sg.Text('Please enter your information.')],
              [sg.Text('SSN:',size =(10,1)), sg.Input(size=(10,1), key='ssn')],
              [sg.Text('Password:', size =(10,1)), sg.Input(size=(10,1), key='password')],
              [sg.Button('Login'),sg.Button('Return to Main Window')]]

    return sg.Window('Login Window', layout)

        
def button_login(values):
    
    global login_user_id 
    global login_user_name
    global login_user_surname
    global window
    
    ssn = values['ssn']
    passw = values['password']
    if ssn == '':
        sg.popup('SSN cannot be empty')
    elif passw == '':
        sg.popup('Password cannot be empty')
    else:
        cur.execute('''SELECT * FROM ''' + login_user_role + ''' 
                    WHERE SSN=? 
                    AND Password = ?'''
                    ,(int(ssn),passw))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('SSN or password is wrong!')
        else:
            login_user_id = ssn
            login_user_name = row[2]
            login_user_surname = row[3]
            
            sg.popup('Welcome, ' + str(login_user_name) + ' ' + str(login_user_surname) )
            window.close()
            window = seller_homepage()

###SELLER WINDOWS & BUTTONS###
def seller_homepage():
    layout = [[sg.Text('Welcome ' + login_user_name + login_user_surname)],
              [sg.Button('My Auctions')], #done
              [sg.Button('Update My Profile')],
              [sg.Button('Logout')]]
    return sg.Window('Seller Homepage', layout)

def seller_my_auction_window():
    layout = [[sg.Text('Welcome ' + login_user_name + login_user_surname)],
              [sg.Button('Finished Auctions')],
              [sg.Button('Ongoing Auctions')],
              [sg.Button('Rejected Auctions')],
              [sg.Button('Create Auction Page')], #done
              [sg.Button('Delete Auction Page')],
              [sg.Button('Return to Seller Homepage')]]

    return sg.Window('Seller My Auctions', layout)

    ### Create Auction ###
def seller_create_auction_window():    
    layout = [[sg.Text('Please enter NEW AUCTION information.')],
        [sg.Text('ID (Should Be Unique):',size =(16,1)), sg.Input(size=(20,1), key='id')],
        [sg.Text('Category:', size =(16,1)), sg.Input(size=(20,1), key='category')],
        [sg.Text('Title:', size =(16,1)), sg.Input(size=(20,1), key='title')],
        [sg.Text('Description:', size =(16,1)), sg.Input(size=(20,1), key='description')],
        [sg.Text('Start Price:', size =(16,1)), sg.Input(size=(20,1), key='start_price')],
        [sg.Text('Buy Now Price:', size =(16,1)), sg.Input(size=(20,1), key='buy_now_price')],
        [sg.Text('Start Date:', size =(16,1)), sg.Input(size=(20,1), key='start_date')],
        [sg.Text('End Date:', size =(16,1)), sg.Input(size=(20,1), key='end_date')],
        [sg.Button('Create Auction')],
        [sg.Button('Return to Seller Homepage')]]

    return sg.Window("Auction Creation", layout)

def button_create_auction(values):
    global window  
    global login_user_role
    global login_user_id

    if not (values['id'] or values['category'] or 
    values['title'] or values['description'] or 
    values['start_price'] or values['buy_now_price'] or
    values['start_date'] or values['end_date']): 
        sg.popup("bad creditientials!") 
        return  

    data = (int(values['id']), int(login_user_id), False, "Not Determined", values['start_date'], values['end_date'], values['title'], values['description'],"Not Determined",int(values['start_price']),0 , -1, int(values['buy_now_price']),values['category'],False)
    sql = """INSERT OR IGNORE INTO AUCTIONS (
                         ID,
                         SSN,
                         IS_ACCEPTED,
                         WHO_ACCEPTED,
                         START_DATE,
                         END_DATE,
                         TITLE,
                         DESCRIPTION,
                         STATUS,
                         START_PRICE,
                         CURRENT_PRICE,
                         BIDDER_SSN,
                         BUY_NOW_PRICE,
                         CATEGORY,
                         IS_FINISHED
                     )
                     VALUES (
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?,
                         ?
                     );"""    
    cur.execute(sql, data)
    sg.popup("Auction Created")    

def seller_delete_auction_window():
    global login_user_name
    global login_user_surname
    global login_user_id
    global aucList

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s auctions")],
        [sg.Text('All Auctions IDs:')]]   

    sql = """SELECT ID,
       SSN,
       IS_ACCEPTED,
       WHO_ACCEPTED,
       START_DATE,
       END_DATE,
       TITLE,
       DESCRIPTION,
       STATUS,
       START_PRICE,
       CURRENT_PRICE,
       BIDDER_SSN,
       BUY_NOW_PRICE,
       CATEGORY,
       IS_FINISHED
  FROM AUCTIONS
  WHERE SSN = ?;""" 
    data = (int(login_user_id),)
    row = cur.execute(sql, data)
    allList = row.fetchall()
    a = []
    for auc in allList:
        a.append(auc[0])  
    layout.append([sg.Listbox(a, enable_events=True, size=(3,5), key='auction_to_delete',)])
    layout.append([sg.Button('Delete Auction')])
    layout.append([sg.Button('Return to Seller Homepage')])
    return sg.Window("Auction Del", layout)

def button_delete_auction(values):
    global login_user_id
    sql = """DELETE OR IGNORE FROM AUCTIONS
      WHERE ID = ?;
    """
    data = (int(values['auction_to_delete']),)
    cur.execute(sql, data)

#####################################################################################################
window = Main()              
while True:
    event, values = window.read()
    
    if event == 'To Login':
        set_role(values)

    ### Account Creation ###     
    elif event == 'Create Account Window':
        button_to_account_create(values)

    elif event == 'Create Account':
        button_create_account(values)

    ## Log Functionality ###    
    elif event == 'Login':
        button_login(values)
    elif event == 'Logout':
        login_user_id = -1
        login_user_name = -1
        login_user_surname= -1
        window.close()
        window = Main()

    ### Return / Quit ###        
    elif event == 'Return to Main Window':
        login_user_id = -1
        login_user_name = -1
        login_user_surname= -1
        window.close()
        window = Main()
    elif event == sg.WIN_CLOSED:
        break

    ### Seller Functions ###
    elif event == 'Return to Seller Homepage':
        window.close()
        window = seller_homepage() 
        
    elif event == 'My Auctions':
        window.close()
        window = seller_my_auction_window() 

    elif event == 'Create Auction Page':
        window.close()
        window = seller_create_auction_window()

    elif event == 'Create Auction':
        button_create_auction(values)    

    elif event == 'Delete Auction Page':
        window.close()
        window = seller_delete_auction_window()     

    elif event == 'Delete Auction':
        button_delete_auction(values)      
              
window.close()

con.commit()
con.close()          