import random
import sqlite3
import PySimpleGUI as sg
from datetime import datetime

# connect to the DB
con = sqlite3.connect('DB.db')
cur = con.cursor()

# global variables
login_user_id = -1
login_user_name = -1
login_user_surname= -1
login_user_role= ""

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
        elif login_user_role == "SELLER":
            login_user_id = ssn
            login_user_name = row[2]
            login_user_surname = row[3]
            
            sg.popup('Welcome, ' + str(login_user_name) + ' ' + str(login_user_surname) )
            window.close()
            window = seller_homepage()

        elif login_user_role == "ADMIN":
            login_user_id = ssn
            login_user_name = row[2]
            login_user_surname = row[3]
            
            sg.popup('Welcome, ' + str(login_user_name) + ' ' + str(login_user_surname) )
            window.close()
            window = admin_homepage()       

        elif login_user_role == "BUYER":
            login_user_id = ssn
            login_user_name = row[2]
            login_user_surname = row[3]
            
            sg.popup('Welcome, ' + str(login_user_name) + ' ' + str(login_user_surname) )
            window.close()
            window = buyer_homepage()  
            
###UPDATE USER###
def window_user_update():
    layout = [[sg.Text('Please enter your new information.')],
            [sg.Text('Password:', size =(10,1)), sg.Input(size=(10,1), key='new_password'), sg.Button('Update New Password')],
            [sg.Text('IBAN:', size =(10,1)), sg.Input(size=(10,1), key='new_iban'), sg.Button('Update New IBAN'),],
            [sg.Button('Return to Main Window')]]

    return sg.Window("User Update Window", layout)
 
def button_update_password(values):
    global login_user_role
    global login_user_id
    sql = """UPDATE """+login_user_role+"""
   SET PASSWORD = ?
 WHERE SSN = ?;"""
    data = (str(values['new_password']), int(login_user_id))
    cur.execute(sql, data)

def button_update_iban(values):
    global login_user_role
    global login_user_id
    sql = """UPDATE """+login_user_role+"""
   SET IBAN = ?
 WHERE SSN = ?;"""
    data = (str(values['new_iban']), int(login_user_id))
    cur.execute(sql, data)

###BUYER FUNCTION###
def buyer_homepage():
    layout = [[sg.Text('Welcome ' + login_user_name + " " + login_user_surname)],
              [sg.Button('Auctions')], 
              [sg.Button('Update My Profile')],
              [sg.Button('Logout')]]
    return sg.Window('Return to Seller Homepage', layout)

def buyer_auctions_window():
    global login_user_name
    global login_user_surname
    global login_user_id

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s auctions")],
        [sg.Text('Select Category:')]]   

    sql = """SELECT CATEGORY
  FROM AUCTIONS
  WHERE IS_ACCEPTED = 1
  AND IS_FINISHED = 0
  AND IS_RESPONDED = 1;""" 
    row = cur.execute(sql)
    allList = row.fetchall()
    allCate = []
    for auc in allList:
        if not allCate.__contains__(auc[0]):
            allCate.append(auc[0])
    layout.append([[sg.Combo(allCate,key= 'chosen_category')],[sg.Button('Find Category')]])
    
    layout.append([sg.Button('Return to Buyer Homepage')])
    return sg.Window("Auction Find", layout)

def button_categorized_auction(values):
    global login_user_name
    global login_user_surname
    global login_user_id
    global window
    if not values['chosen_category']:
        sg.popup('Category Not Chosen')
        return
    window.close()
    window = buyer_categorized_auction_window(values['chosen_category'])
    
def buyer_categorized_auction_window(category):
    global login_user_name
    global login_user_surname
    global login_user_id

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s auctions")],
        [sg.Text('All Auctions:')]]   

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE CATEGORY = ?
  AND IS_ACCEPTED = 1
  AND IS_FINISHED = 0
  AND IS_RESPONDED = 1;""" 
    data = (str(category),)
    row = cur.execute(sql, data)
    allList = row.fetchall()

    if allList is not None:
        for auc in allList:
            layout.append([sg.Text("**************************")])
            layout.append([sg.Text("ID: "+ str(auc[0])),
            sg.Text("TITLE: "+ str(auc[6])),
            sg.Text("DESCRIPTION: "+ str(auc[7]))])
            layout.append([sg.Text("Start Date: "+ str(auc[4])),
            sg.Text("End Date: "+ str(auc[5])),
            sg.Text("Current Price: "+ str(auc[10])),
            sg.Text("Current Bidder: "+ str(auc[11])),
            sg.Text("Buy Now Price: "+ str(auc[12]))])
            layout.append([sg.Text("Bid:"),sg.Input(size=(5,1), key= 'bid_user_'+str(auc[0])),
            sg.Button(str(auc[0]), key= 'bid_auction_now')])
            layout.append([sg.Text("**************************")])
    
    layout.append([sg.Button('Return to Buyer Homepage')])
    return sg.Window("Auction Bid", layout)

def button_bid_to_auction(idOfAuc, bid):
    global window
    global login_user_id
    global login_user_name
    global window
    sql = """SELECT CURRENT_PRICE,
    BUY_NOW_PRICE
  FROM AUCTIONS
  WHERE IS_ACCEPTED = 1
  AND IS_FINISHED = 0
  AND IS_RESPONDED = 1
  AND ID = ?;""" 
    data = (int(idOfAuc),)
    cur.execute(sql, data)
    row = cur.fetchone()
    if ((int(row[0]) > int(bid)) or (int(row[1]) < int(row[0]))):
        sg.popup('Either buynow value is reached or bid is less then current price')
        return
    if not bid:
        return
    
    sql = """UPDATE AUCTIONS
   SET CURRENT_PRICE = ?,
       BIDDER_SSN = ?
 WHERE ID = ?;"""
    data = (int(bid),str(login_user_id), int(idOfAuc))
    cur.execute(sql, data)
    
    window.close()
    window = buyer_auctions_window()
    
    
###ADMIN WINDOWNS & BUTTONS###
def admin_homepage():
    layout = [[sg.Text('Welcome ' + login_user_name+ " " + login_user_surname)],
              [sg.Button('Auctions To Accept')],
              [sg.Button('Logout')]]
    return sg.Window('Admin Homepage', layout)

def admin_auctions_to_accept_window():
    global login_user_name
    global login_user_surname
    global login_user_id
    
    layout = [[sg.Text("AUCTIONS AWAITING APPROVAL:")],
        [sg.Text('All Auctions:')]]   

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE IS_ACCEPTED = 0
  AND IS_RESPONDED = 0;""" 
    row = cur.execute(sql)
    allList = row.fetchall()
    if allList is not None:
        for auc in allList:
            layout.append([sg.Text("id: "+ str(auc[0])),sg.Text("title: "+ auc[6]),sg.Text("Description: "+ auc[7]),sg.Text("Accept=>"),sg.Button(str(auc[0]), key= 'Accept Auction'),sg.Text("Deny=>"),sg.Button(str(auc[0]), key= 'Deny Auction')])
    
    layout.append([sg.Button('Return to Admin Homepage')])
    return sg.Window("Auction response", layout)

def button_accept_auction(idOfAuc):
    global window
    global login_user_id
    global login_user_name
    sql = """UPDATE AUCTIONS
   SET IS_ACCEPTED = 1,
       IS_RESPONDED = 1,
       WHO_ACCEPTED = ?
 WHERE ID = ?;"""
    data = (str(login_user_name), int(idOfAuc))
    cur.execute(sql, data)
    window.close()
    window = admin_auctions_to_accept_window()

def button_deny_auction(idOfAuc):
    global window
    global login_user_id
    global login_user_name
    sql = """UPDATE AUCTIONS
   SET IS_ACCEPTED = 0,
       IS_RESPONDED = 1,
       WHO_ACCEPTED = ?
 WHERE ID = ?;"""
    data = (str(login_user_name), int(idOfAuc))
    cur.execute(sql, data)
    window.close()
    window = admin_auctions_to_accept_window()

###SELLER WINDOWS & BUTTONS###
def seller_homepage():
    layout = [[sg.Text('Welcome ' + login_user_name + " " + login_user_surname)],
              [sg.Button('My Auctions')], #done
              [sg.Button('Update My Profile')],
              [sg.Button('Logout')]]
    return sg.Window('Seller Homepage', layout)

def seller_my_auction_window():
    layout = [[sg.Text('Welcome ' + login_user_name + login_user_surname)],
              [sg.Button('Finished Auctions Page')],
              [sg.Button('Ongoing Auctions Page')],
              [sg.Button('Rejected Auctions Page')],
              [sg.Button('Create Auction Page')], #done
              [sg.Button('Delete Auction Page')], #done
              [sg.Button('Return to Seller Homepage')]] #done

    return sg.Window('Seller My Auctions', layout)

    ### Create Auction ###
def seller_create_auction_window():    
    layout = [[sg.Text('Please enter NEW AUCTION information.')],
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

    if not (values['category'] or 
    values['title'] or values['description'] or 
    values['start_price'] or values['buy_now_price'] or
    values['start_date'] or values['end_date']): 
        sg.popup("bad creditientials!") 
        return  

    data = ((random.randint(1,10000)), int(login_user_id), False, "Not Determined", values['start_date'], values['end_date'], values['title'], values['description'],"Not Determined",int(values['start_price']),0 , -1, int(values['buy_now_price']),values['category'],False,False)
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
                         IS_FINISHED,
                         IS_RESPONDED
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
                         ?,
                         ?
                     );"""    
    cur.execute(sql, data)
    sg.popup("Auction Created")    

def seller_delete_auction_window():
    global login_user_name
    global login_user_surname
    global login_user_id

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s auctions")],
        [sg.Text('All Auctions:')]]   

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE SSN = ?
  AND IS_ACCEPTED = 1
  AND IS_FINISHED = 0
  AND IS_RESPONDED = 1;""" 
    data = (int(login_user_id),)
    row = cur.execute(sql, data)
    allList = row.fetchall()

    if allList is not None:
        for auc in allList:
            layout.append([sg.Text("id: "+ str(auc[0])),sg.Text("title: "+ auc[6]),sg.Text("for Deletion click =>"),sg.Button(str(auc[0]), key= 'Delete Auctions')])
    
    layout.append([sg.Button('Return to Seller Homepage')])
    return sg.Window("Auction Del", layout)

def button_delete_auction(idOfAuc):
    global login_user_id
    global window
    sql = """DELETE FROM AUCTIONS
      WHERE ID = ?;"""
    data = (int(idOfAuc),)
    cur.execute(sql, data)
    window.close()
    window = seller_delete_auction_window()

def seller_finished_auction_window():
    global login_user_name
    global login_user_surname
    global login_user_id
    global aucList
    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s Finished Auctions")],
        [sg.Text('All Finished Auctions:')]]

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE SSN = ?
  AND IS_FINISHED = 1
  AND IS_RESPONDED = 1
  AND IS_ACCEPTED = 1;""" 


    data = (int(login_user_id),)
    row = cur.execute(sql, data)
    allList = row.fetchall()

    for auc in allList:
        layout.append([sg.Text("id: "+ str(auc[0])),sg.Text("show bill of "+ auc[6]),sg.Button(str(auc[0]), key= 'Show Bill')])

    layout.append([sg.Button('Return to Seller Homepage')])
    return sg.Window("Auction Finished", layout)
    
def seller_show_bill_window(idOfAuc):
    global login_user_name
    global login_user_surname
    global window
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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE ID = ?
  AND IS_FINISHED = 1;""" 
    data = (int(idOfAuc),)
    row = cur.execute(sql, data)
    info = row.fetchone()

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s Auction")],
        [sg.Text('ID of Auction: ' + str(info[0]))],
        [sg.Text('Who accepted Auction: ' + str(info[3]))],
        [sg.Text('Sold for: ' + str(info[10]))],
        [sg.Text('Buyer SSN: ' + str(info[11]))],
        [sg.Text('Tax of Company: ' + str(float(info[10]) * 0.08))],
        [sg.Button('Return to Seller Homepage')]]

    return sg.Window("Bill Info", layout)

def seller_ongoing_auction_window():
    global login_user_name
    global login_user_surname
    global login_user_id
    global aucList

    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s ongoing auctions")],
        [sg.Text('All ongoing Auctions:')]]   

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE SSN = ?
  AND IS_ACCEPTED = 1
  AND IS_FINISHED = 0
  AND IS_RESPONDED = 1;""" 
    data = (int(login_user_id),)
    row = cur.execute(sql, data)
    allList = row.fetchall()

    if allList is not None:
        for auc in allList:
            layout.append([sg.Text("**************************")])
            layout.append([sg.Text("ID: "+ str(auc[0])),
            sg.Text("TITLE: "+ str(auc[6])),
            sg.Text("DESCRIPTION: "+ str(auc[7]))])
            layout.append([sg.Text("Start Date: "+ str(auc[4])),
            sg.Text("End Date: "+ str(auc[5])),
            sg.Text("Current Price: "+ str(auc[10])),
            sg.Text("Current Bidder: "+ str(auc[11]))])
            layout.append([sg.Text("for Ending click =>"),
            sg.Button(str(auc[0]), key= 'End Auction')])
            layout.append([sg.Text("**************************")])
    
    layout.append([sg.Button('Return to Seller Homepage')])
    return sg.Window("Ongoing Auction", layout)

def button_end_auction(idOfAuc):
    global login_user_id
    global login_user_name
    global window
    sql = """UPDATE AUCTIONS
   SET IS_FINISHED = 1
 WHERE ID = ?;"""
    data = (int(idOfAuc),)
    cur.execute(sql, data)
    window.close()
    window = seller_ongoing_auction_window()

def seller_rejected_auction_window():
    global login_user_name
    global login_user_surname
    global login_user_id
    global aucList
    layout = [[sg.Text(login_user_name + "  " + login_user_surname + "'s Finished Auctions")],
        [sg.Text('All Finished Auctions:')]]

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
       IS_FINISHED,
       IS_RESPONDED
  FROM AUCTIONS
  WHERE SSN = ?
  AND IS_RESPONDED = 1
  AND IS_ACCEPTED = 0;""" 


    data = (int(login_user_id),)
    row = cur.execute(sql, data)
    allList = row.fetchall()

    for auc in allList:
        layout.append([sg.Text("id: "+ str(auc[0])),sg.Text("title: "+ auc[6]),sg.Text("Description: "+ auc[6]),sg.Text("REJECTED BY: " + auc[3])])
    layout.append([sg.Button('Return to Seller Homepage')])
    return sg.Window("Auction Rejected Page", layout)
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
    ### User Update ###
    elif event == 'Update New Password':
        button_update_password(values)

    elif event == 'Update New IBAN':
        button_update_iban(values)
    ### Return / Quit ###        
    elif event == 'Return to Main Window':
        login_user_id = -1
        login_user_name = -1
        login_user_surname= -1
        window.close()
        window = Main()
    elif event == sg.WIN_CLOSED:
        break

    ### Buyer Functions & Windows ###
    elif event == 'Return to Buyer Homepage':
        window.close()
        window = buyer_homepage() 
    
    elif event == 'Auctions':
        window.close()
        window = buyer_auctions_window() 
        
    elif event == 'Find Category':
        button_categorized_auction(values)
        
    elif event.__contains__('bid_auction_now'):
        button_bid_to_auction(window[event].get_text(),int(values['bid_user_'+str(window[event].get_text())]))
        
    ### Admin Functions ###
    elif event == 'Return to Admin Homepage':
        window.close()
        window = admin_homepage() 

    elif event == 'Auctions To Accept':
        window.close()
        window = admin_auctions_to_accept_window() 

    elif event.__contains__('Accept Auction'):
        button_accept_auction(window[event].get_text()) 

    elif event.__contains__('Deny Auction'):
        button_deny_auction(window[event].get_text()) 

    ### Seller Functions ###
    elif event == 'Update My Profile':
        window.close()
        window = window_user_update() 

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

    elif event.__contains__('Delete Auctions'):
        button_delete_auction(window[event].get_text())     

    elif event == 'Finished Auctions Page':
        window.close()
        window = seller_finished_auction_window()  

    elif event.__contains__('Show Bill'):
        window.close()
        window = seller_show_bill_window(window[event].get_text())  

    elif event == 'Ongoing Auctions Page':
        window.close()
        window = seller_ongoing_auction_window() 

    elif event.__contains__('End Auction'):
        button_end_auction(window[event].get_text())  

    elif event == 'Rejected Auctions Page':
        window.close()
        window = seller_rejected_auction_window() 
              
window.close()

con.commit()
con.close()          
