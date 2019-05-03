from flask import Flask, request, redirect, render_template
from multiprocessing import Process

import sys

sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")  #OPTIONAL: Only if need to access Python packages installed on a local (non-global) directory
sys.path.insert(2, "PATH TO FLASK DIRECTORY")      #OPTIONAL: Only if you need to add the directory of your flask app

app = Flask(__name__)

@app.route('/') 
def sql_database():
    from tools.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM AllProducts''')
    msg = ''
    return render_template('all-products.html', results=results, msg=msg)   

@app.route('/interested',methods = ['POST', 'GET']) #this is when user submits an insert
def userInterested():
    from tools.sqlquery import sql_edit_insert, sql_query
    if request.method == 'GET':
        from tools.sqlquery import sql_query
        results = sql_query(''' SELECT * FROM AllProducts''')
        msg = ''
        return render_template('all-products.html', results=results, msg=msg)  

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
            return render_template('all-products.html',results=results ,msg="Your Details are being sent!") 
        
        except Exception as e:
            print (e)
            return render_template('all-products.html',results=results ,msg="Some error occured make sure details are correct.") 


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

if __name__ == "__main__":
    app.run(debug=True)



