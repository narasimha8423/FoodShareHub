from flask import Flask, render_template, request,url_for,redirect,flash,session
import mysql.connector
from flask_mail import Mail, Message
import random
from datetime import datetime
import uuid 


app = Flask(__name__)
app.secret_key = '20' 
app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hackworriers6@fastmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] ='stmbdle78sva3lvg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


admin_email="narasimha@gmail.com"
admin_password="123456"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="food_share"
)
cursor = db.cursor()

@app.route('/')
def index():
    if 'logged_in' in session:
        user = session['email']
        return render_template('profile.html', user=user)
    return render_template('Main.html')



@app.route('/about_us')
def about_us():
    return render_template('about_us.html')
    
@app.route('/donate_now')
def donate_now():
    return render_template('donate_now.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/donate_item')
def donate_item():
    return render_template('donate_item.html')

@app.route('/athentication')
def athentication():
    alert_message = "Enter mail for Authentication !!!"
    return render_template('otp_verification_page.html',alert_message=alert_message)

@app.route('/send_otp', methods=['GET', 'POST'])
def send_otp():
    if request.method == 'POST':
        recipient = request.form['email']
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)]) 
        session['otp_code'] = otp_code
        message = Message(subject="Verification Email", 
                          sender=app.config.get('MAIL_USERNAME'),
                          recipients=[recipient])
        message.body = "Your Verification code is "+otp_code
        mail.send(message)
        # return redirect(url_for('index'))  # Redirect to homepage after sending email
        alert_message = "OTP Sent successfully!"
        return render_template('verification_page.html',alert_message=alert_message)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']
    stored_otp = session.get('otp_code')

    if user_otp == stored_otp:
        # OTP verification successful
        alert_message = "OTP verification successful"
        return render_template('food_donation_page.html',alert_message=alert_message)

    else:
        # OTP verification failed
        alert_message = "OTP verification failed"
        return render_template('Main.html',alert_message=alert_message)




@app.route('/login_submit', methods=['POST'])
def login_submit():
    cursor = db.cursor()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute("SELECT email,password FROM userlist where ")
        list = cursor.fetchall()
        

@app.route('/display_doners')
def display_doners():
    # Creating a cursor to interact with the database
    cursor = db.cursor()
    
    # Fetching donor data from the database
    cursor.execute("SELECT * FROM donations")
    donors = cursor.fetchall()
    
    # Closing cursor and database connection
    
    # Rendering HTML template with donor data
    return render_template('display_doners.html', donors=donors)

@app.route('/Login')
def Login():
    return render_template('login.html')

@app.route('/Registration')
def Registration():
    return render_template('registration_page.html')


            
# @app.route('/send_email')
# def send_email():
#     recipient = 'narasimha8423@gmail.com'  # Replace with the recipient's email address
#     message = Message(
#         subject='Test Email from Flask',
#         sender=app.config.get('MAIL_USERNAME'),
#         recipients=[recipient]
#     )
#     message.body = 'This is a test email sent from Flask!'
#     mail.send(message)
#     return 'Email sent successfully!'




@app.route('/user_types')
def user_types():
    return render_template('login_types.html')

# Route for registration page
@app.route('/profile')
def profile():
    return render_template('User_Regiatration.html')

# Route for handling registration form submission
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST' and 'logged_in' not in session:
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        
        # Check if the email is already registered
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            alert_message = "Email already registered. Please login or use a different email."
            return render_template('Main.html',alert_message=alert_message)
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO users(email, password) VALUES (%s, %s)", (email, password))
            db.commit()
            return redirect('/')
    else:
        alert_message="Already Logined!"
        return redirect('/user_details')
        

# Route for login page
@app.route('/User_login')
def User_login():
    return render_template('login.html')

# Route for handling login form submission
@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST' and 'logged_in' not in session:
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        
        # Verify user credentials
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if user[1]==password and user[0]==email:
            session['logged_in'] = True
            session['email'] = user[0]
            return redirect('/user_details')
        else:
            alert_message = "Login failed. Please check your credentials."
            return render_template('login.html',alert_message=alert_message)
    elif 'logged_in' in session:
        # cursor = db.cursor()
        # # Retrieve user details
        # cursor.execute("SELECT * FROM users WHERE email=%s", (session['email'],))
        # user = cursor.fetchone()
        return  redirect('/user_details')
    else:
        alert_message="Already Logined!"
        return redirect('/user_details')
            


@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/login_admin',methods=['POST'])
def login_admin():
    if request.method == 'POST' and 'logged_in' not in session :
        email = request.form['email']
        password = request.form['password']
        
        if admin_password==password and admin_email==email:
            session['logged_in'] = True
            session['email'] =admin_email
            return redirect('/dashboard')
        else:
            alert_message = "Login failed. Please check your credentials."
            return redirect('/dashboard')
    elif 'logged_in' in session:
        return redirect('/dashboard')
    else:
        alert_message="Already Logined!"
        return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT count(order_id) FROM donations")
    donations = cursor.fetchone()
    cursor.execute("SELECT count(email) FROM volunteer")
    volunteer = cursor.fetchone()
    cursor.execute("SELECT count(order_id) FROM donations WHERE delivery_status= %s",('Yes',))
    volunteer_count = cursor.fetchone()
    cursor.execute("SELECT * FROM donations")
    user_donations=cursor.fetchall()
    cursor.execute("SELECT * FROM donations")
    donations_list= cursor.fetchall()
    return render_template('dashboard.html',donations=donations,volunteer=volunteer,volunteer_count=volunteer_count,user_donations=user_donations,donations_list=donations_list)


# Route for registration page
@app.route('/volunteer')
def volunteer():
    return render_template('Volunter_register.html')

# Route for handling registration form submission
@app.route('/volunteer_Register', methods=['POST'])
def volunteer_Register():
    if request.method == 'POST' and 'logged_in' not in session:
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        
        # Check if the email is already registered
        cursor.execute("SELECT * FROM volunteer WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            alert_message = "Email already registered. Please login or use a different email."
            return render_template('Main.html',alert_message=alert_message)
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO volunteer(email, password) VALUES (%s, %s)", (email, password))
            db.commit()
            return redirect('/')
    else:
        alert_message="Already Logined!"
        return render_template('Mian.html',alert_message=alert_message)
        

# Route for login page
@app.route('/volunteers_login')
def volunteers_login():
    return render_template('volunteers_login.html')

# Route for handling login form submission
@app.route('/volunteer_after_login', methods=['POST'])
def volunteer_after_login():
    if request.method == 'POST' and 'logged_in' not in session:
        email = request.form['email']
        password = request.form['password']
        
        cursor = db.cursor()
        
        # Verify user credentials
        cursor.execute("SELECT * FROM volunteer WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        if user[1]==password and user[0]==email:
            session['logged_in'] = True
            session['email'] = user[0]
            return redirect('/Volumteer_data')
        else:
            alert_message = "Login failed. Please check your credentials."
            return render_template('volunteers_login.html',alert_message=alert_message)
    elif 'logged_in' in session:
        cursor = db.cursor()
        # Retrieve user details
        cursor.execute("SELECT * FROM volunteer WHERE email=%s", (session['email'],))
        user = cursor.fetchone()
        return redirect('/Volumteer_data')
    else:
        alert_message="Already Logined!"
        return redirect('/Volumteer_data')



# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/') 


@app.route('/user_details')
def user_details():
    if 'logged_in' not in session:
        return redirect(url_for('User_login'))
    cursor.execute("SELECT * FROM users WHERE email=%s", (session['email'],))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM donations WHERE email=%s", (session['email'],))
    donations = cursor.fetchall()

    return render_template('user_profile.html', user=user,donations=donations,session_id=app.secret_key)


@app.route('/donate')
def donate():
    return render_template("food_donation_page.html")


@app.route('/donate_food', methods=['GET', 'POST'])
def donate_food():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        food_type = request.form['food_type']
        food_name = request.form['food_name']
        current_date = datetime.now()
        order="available"
        cursor=db.cursor()
        delivery_status="No"
        order_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Process the donation data (e.g., save to database)
        cursor=db.cursor()
        cursor.execute("INSERT INTO donations (name, email, phone, address, food_type, food_name,date,order_available,order_id,delivery_status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s)", (name, email, phone, address, food_type, food_name,current_date,order,order_id,delivery_status))
        db.commit()
        cursor=db.cursor()
        cursor.execute("SELECT email FROM volunteer")
        users=cursor.fetchall()
        body=""
        for user in users:
            message = Message(subject="Alert Donation Email", 
                          sender=app.config.get('MAIL_USERNAME'),
                          recipients=[user[0]])
            message.html = render_template('email_template.html')
            mail.send(message)
        # return redirect(url_for('index'))  # Redirect to homepage after sending email
        alert_message="Your Donation has been Recorded.Please logout and login again to check!!"
        return render_template('timer.html',alert_message=alert_message)
    return redirect('/user_details')



@app.route('/Volumteer_data')
def Volumteer_data():
    if 'logged_in' not in session:
        return redirect(url_for('volunteers_login'))
    cursor.execute("SELECT * FROM volunteer WHERE email=%s", (session['email'],))
    user = cursor.fetchone()
    status="available"
    cursor.execute("SELECT * FROM donations WHERE order_available=%s",(status,))
    donations = cursor.fetchall()

    return render_template('volunteer_profile.html', user=user,donations=donations)


@app.route('/take_order' ,methods=['Post'])
def take_order():
    if 'logged_in' in session:
            # SQL UPDATE statement
        status="Not Available"
        donor_email=request.form.get('order_id')
        # Execute the UPDATE statement
        cursor.execute("UPDATE donations SET order_assigned= %s ,order_available = %s WHERE order_id = %s",(session['email'],status,donor_email,))

        # Commit the changes

        db.commit()
        alert_message="Your Order confirmed!"
        return redirect('/Volumteer_data')
    return redirect('/')

@app.route('/delivery_status')
def delivery_status():
    return render_template('delivery_status.html')


@app.route('/delivery_submit',methods=['POST'])
def delivery_submit():
    if request.method == 'POST':
        status=request.form.get('status')
        order_id=request.form['order_id']
        address=request.form['address']
            # Execute the UPDATE statement
        cursor.execute("UPDATE donations SET delivery_status= %s,delivery_address=%s WHERE order_id = %s",(status,address,order_id,))
        db.commit()
        return redirect('Volumteer_data')
    return render_template('delivery_status.html')

@app.route('/timer')
def timer():
    return redirect('/send_email')

@app.route('/send_email')
def send_email():
    cursor=db.cursor()
    cursor.execute("SELECT email FROM volunteer")
    users=cursor.fetchall()
    for user in users:
            message = Message(subject="Alert Warning", 
                          sender=app.config.get('MAIL_USERNAME'),
                          recipients=[user[0]])
            message.body = 'Please take order immediately to deliver  '
            mail.send(message)
    return redirect('/user_details') # Redirect to homepage after sending email




@app.route('/Confirm_order')
def Confirm_order():
    return redirect('/show_orders')


@app.route('/show_orders')
def show_orders():
    if 'logged_in' in session:
            # SQL UPDATE statement
        id=request.form.get('order_id')
        # Execute the UPDATE statement
        cursor.execute("SELECT * FROM volunteer WHERE email=%s", (session['email'],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM donations WHERE order_assigned=%s",(session['email'],))
        donations = cursor.fetchall()
        return render_template('show_confirmed_order.html', user=user,donations=donations)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
