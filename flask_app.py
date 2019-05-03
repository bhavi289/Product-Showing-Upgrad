from flask import Flask, request, redirect, render_template
from multiprocessing import Process

import sys

sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")  #OPTIONAL: Only if need to access Python packages installed on a local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")      #OPTIONAL: Only if you need to add the directory of your flask app

app = Flask(__name__)

@app.route('/') 
def sql_database():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM AllProducts''')
    msg = 'SELECT * FROM AllProducts'
    return render_template('sqldatabase.html', results=results, msg=msg)   
@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        sql_edit_insert(''' INSERT INTO AllProducts (first_name,last_name,address,city,state,zip) VALUES (?,?,?,?,?,?) ''', (first_name,last_name,address,city,state,zip) )
    results = sql_query(''' SELECT * FROM AllProducts''')
    msg = 'INSERT INTO AllProducts (first_name,last_name,address,city,state,zip) VALUES ('+first_name+','+last_name+','+address+','+city+','+state+','+zip+')'
    return render_template('sqldatabase.html', results=results, msg=msg) 

def send_email(user, pwd, recipient, title, body):
    import smtplib
    from email.mime.application import MIMEApplication
    from os.path import basename
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import sys, traceback
    from email.utils import COMMASPACE, formatdate
    # from email.MIMEBase import MIMEBase
    # from email import Encoders
    try:
        print ("Sending")
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = recipient
        msg['Subject'] = title
        message = body
        msg.attach(MIMEText(message))
        
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(user, pwd)
        
        mailserver.sendmail(user,recipient,msg.as_string())
        
        mailserver.quit()
        print ("Sent Email")
    except Exception as e:
        print (e)
        send_email(user, pwd, recipient, title)


@app.route('/interested',methods = ['POST', 'GET']) #this is when user submits an insert
def userInterested():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        results = sql_query(''' SELECT * FROM AllProducts''')
        try:
            print ("success post")
            product_name = request.form['product_name']
            print(product_name)
            email = request.form['user_email']
            product_index = request.form['product_index']
            # q = " SELECT * FROM AllProducts WHERE index='"+ (product_index) + "'"
            # print (q)
            product = sql_query(" SELECT * FROM AllProducts WHERE product_name='"+ (product_name) + "'")
            print("product is ", product[0]['product_name'],email)
            title = "Your Requested Product(" + product[0]['product_name'] + ") Details Are Here!"
            body = "Description Of Product - '" + product[0]['product_description'] + "'"

            p = Process(target=send_email, kwargs={"user":'csb.iiits@gmail.com',"pwd": 'csb@iiits',"recipient" : str(email) , "title":title ,"body":body})
            p.daemon = False
            p.start()
            # send_email('csb.iiits@gmail.com', 'csb@iiits', str(email), title, body)
            return render_template('sqldatabase.html',results=results ,msg="Your Details are being sent!") 
        
        except Exception as e:
            print (e)
            return render_template('sqldatabase.html',results=results ,msg="Some error occured make sure details are correct.") 


@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'GET':
        lname = request.args.get('lname')
        fname = request.args.get('fname')
        sql_delete(''' DELETE FROM AllProducts where first_name = ? and last_name = ?''', (fname,lname) )
    results = sql_query(''' SELECT * FROM AllProducts''')
    msg = 'DELETE FROM AllProducts WHERE first_name = ' + fname + ' and last_name = ' + lname
    return render_template('sqldatabase.html', results=results, msg=msg)
@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    from functions.sqlquery import sql_query, sql_query2
    if request.method == 'GET':
        elname = request.args.get('elname')
        efname = request.args.get('efname')
        eresults = sql_query2(''' SELECT * FROM AllProducts where first_name = ? and last_name = ?''', (efname,elname))
    results = sql_query(''' SELECT * FROM AllProducts''')
    return render_template('sqldatabase.html', eresults=eresults, results=results)
@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        old_last_name = request.form['old_last_name']
        old_first_name = request.form['old_first_name']
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        sql_edit_insert(''' UPDATE AllProducts set first_name=?,last_name=?,address=?,city=?,state=?,zip=? WHERE first_name=? and last_name=? ''', (first_name,last_name,address,city,state,zip,old_first_name,old_last_name) )
    results = sql_query(''' SELECT * FROM AllProducts''')
    msg = 'UPDATE AllProducts set first_name = ' + first_name + ', last_name = ' + last_name + ', address = ' + address + ', city = ' + city + ', state = ' + state + ', zip = ' + zip + ' WHERE first_name = ' + old_first_name + ' and last_name = ' + old_last_name
    return render_template('sqldatabase.html', results=results, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)



