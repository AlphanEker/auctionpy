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
auction_id = -1


# window functions

def Main():
    choices = ('Seller', 'Buyer', 'Admin')
    layout1 = [[sg.Text('Welcome to the Online Auction System! Please enter your role.')],
              [sg.Combo(choices, size=(15, len(choices)), key='chosen_role')],
              [sg.Button('OK')]]
    
    return sg.Window('Main Window', layout1)


def window_login_seller():
    
    layout2 = [[sg.Text('Please enter your information.')],
              [sg.Text('SSN:',size =(10,1)), sg.Input(size=(10,1), key='ssn')],
              [sg.Text('Password:', size =(10,1)), sg.Input(size=(10,1), key='password')],
              [sg.Button('Login'),sg.Button('Return to Main Window')]]

    return sg.Window('Login Window', layout2)

            
        

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
        cur.execute('''SELECT SSN, FirstName, 
                    LastName 
                    FROM User 
                    WHERE SSN=? 
                    AND Password = ?'''
                    ,(ssn,passw))
        row = cur.fetchone()
        
        if row is None:
            sg.popup('SSN or password is wrong!')
        else:
            login_user_id = ssn
            login_user_name = row[1]
            login_user_surname = row[2]
            
            sg.popup('Welcome, ' + str(login_user_name) + ' ' + str(login_user_surname) )
            window.close()
            window = window_seller()
            
def bill_button_function(values):
    
    global window
    selected_auction = values['billslist']
    if len(selected_auction) == 0:
        sg.popup('Please select an auction!')
    else:
        auction_id = selected_auction[0][0]
        window.close()
        window= window_billinfo(auction_id)
        
def button_createAuction(values):
    
    category = values['category']
    cat=category[0]
    description = values['description']
    binprice = values['binprice']
    curprice = values['cprice']
    title = values['title']
        
    if category == '':
        sg.popup('You should select a category!')
                  
    cur.execute('SELECT MAX(AuctionID) FROM Auction')
    row = cur.fetchone()
    new_id = row[0] + 1
    default = 0
    
    cur.execute('INSERT INTO Auction VALUES(?,?,null,null,null,?,?,null,?,?,null,?,?,null,null)',(new_id,str(description), binprice, curprice, str(title), default, cat, login_user_id)) 

    sg.popup('Auction is successfully inserted ' + str(title) + 'with id' + ' '  + str(new_id))
            
    window.Element('category').Update(value='')
    window.Element('description').Update(value='')
    window.Element('binprice').Update(value='')
    window.Element('cprice').Update(value='')
    window.Element('title').Update(value='')
                       
              
def button_role(values):
    global window
    if not values['chosen_role']:
        sg.popup('Please choose a role.')
    if values['chosen_role']=='Seller':
        window.close()
        window = window_login_seller()
    if values['chosen_role']=='Admin' or values['chosen_role']=='Buyer':
        window.close()
        sg.popup('Close') 
 

 
window = Main()              
while True:
    event, values = window.read()
    if event == 'OK':
        button_role(values)
    elif event == 'Login':
        button_login(values)
    elif event == 'Return to Main Window':
        window.close()
        window = Main()
    elif event == 'Logout':
        login_user_id = -1
        login_user_name = -1
        login_user_surname= -1
        auction_id = -1
        window.close()
        window = window_login_seller()
    elif event == sg.WIN_CLOSED:
        break
              
window.close()

con.commit()
con.close()          