from flask import Flask, render_template, request,jsonify,session,redirect,url_for;
from  mailsend import send_myemail;
from  KnowledgeTransfer import read_knowledge;
from ResultKnowledge import save_result;
from CaptchaGenerator import create_captcha;
from Graphgenerator import create_graphs;

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def open_home():
    return render_template('home.html')

@app.route('/aboutus')
def open_aboutus():
    return render_template('aboutus.html')

@app.route('/categorizedresult')
def open_categorizedresult():
    create_graphs(); #call to create graph
    return render_template('categorizedresult.html')


@app.route('/advice')
def open_advice():
    return render_template('advice.html')


@app.route('/feedback')
def open_feedback():
    pname=create_captcha();
    return render_template('feedback.html',captcha_img_name=pname);
# route to generate new captcha image

@app.route('/getnew_captcha',methods=["GET"])
def new_captcha():
    pname=create_captcha();
    return jsonify(pname);

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/testajax')
def open_testajax():
    return render_template('addition.html')

@app.route('/addnum',methods=["GET"])
def call_testajax():
   x=request.args.get("fnum");
   y=request.args.get("snum");
   result=int(x)+int(y);
   msg="Addition is: "+str(result);
   return jsonify(msg);

#to test email sending
@app.route("/send")
def mail_test():
    r = send_myemail(app, "ektapal73@gmail.com", "Test Message", "Hello, how are you?")
    if r:
        return "Email sent successfully.";
    else:
        return "Sorry! Unable to send email.";

@app.route('/selfassessment', methods=["POST"])
def open_selfassessment():
    session["name"] = request.form.get("Name")
    session["email"] = request.form.get("Email")
    session["gender"] = request.form.get("Gender")
    session["age"] = int(request.form.get("Age"))

    my_dict = read_knowledge();
    cur_qno = 1;
    session["cur_qno"]=cur_qno; # storing current question number in session 
    session["total_marks"]=0;
    total_questions = len(my_dict);
    process_per = (cur_qno * 100) / total_questions;

    return render_template('selfassessment.html',data=my_dict[0],cqno=cur_qno,
    per=process_per,total_qcount=total_questions);
# To get next question on button click 
@app.route('/process_assessment',methods=["POST"])
def next_assessment():
    btnvalue=request.form.get("btn").strip();
    cur_marks = int(request.form.get("op", 0));
    session["total_marks"]=int(session.get("total_marks"))+cur_marks;
    if btnvalue=="Next":
        # start: to fetch next question
        my_dict = read_knowledge();
        cur_qno = int(session.get("cur_qno"))+1;
        session["cur_qno"]=cur_qno;
        total_questions = len(my_dict);
        process_per = (cur_qno * 100) / total_questions;
        #end: to fetch next question
        return render_template("selfassessment.html",data=my_dict[cur_qno-1],cqno=cur_qno,
        per=process_per,total_qcount=total_questions);
    else:
         #start: to save and display assessment result
         # save result in assessment knowledgebase

         #end: to save and display assessment result
         return redirect(url_for("open_result",tmarks=session.get("total_marks")));

@app.route('/result')
def open_result():
    save_result(); #saving new result in knowledgebase excel
    return render_template("result.html");


# setting secret key for session
app.secret_key="asdasd fdsfdsf";
@app.route('/selfassessment')
def open_user():
    return render_template("userdata.html")

@app.route('/userdata')
def open_userdata():
    return render_template('userdata.html')

@app.route("/submit_feedback",methods=["POST"])
def  save_feed():
    msg="";
    #reading and validating captcha
    user_code=request.form.get("tcaptcha")
    or_code=session.get("code")
    # read data from form
    if user_code==or_code:
        name=request.form.get("name");
        email=request.form.get("email");
        gender=request.form.get("gender");
        feedback=request.form.get("feedback");
        #creating email message to owner
        mail_msg = ( "Hi Admin,<br>"
        "A person with name <b>" + name + "</b> has submitted a feedback on your <b>Mental Health Assessment</b> portal.<br>"
        "Details of the feedback are:<br><br>""<b>Name:</b> " + name + "<br>" "<b>Email ID of person:</b> " + email + "<br>"
        "<b>Gender:</b> " + gender + "<br>" "<b>Feedback Message is:</b> " + feedback + "<br><br><br>""From:<br>""Health")
        #sending email alert to owner
        send_myemail(app, "ektapal73@gmail.com", "A new feedback received",mail_msg);
        msg="thanks for your valuable feedback. we will get back to you shortly."
        #creating email message for user
        user_email = request.form.get("email")  # or request.form.get("email") if not using session
        user_name = request.form.get("name")
        user_marks = session.get("total_marks")
        #sending email to user
        user_msg = f"""Hi {user_name},<br><br>Thank you for your valuable feedback on our Mental Health Assessment portal.<br>
        We appreciate your time and effort in sharing your thoughts.<b>Your Mental Health Score is:</b> {user_marks} / 45,{{<br>
        <br><br>We will get back to you shortly if needed.<br><br>Best regards,<br>Mental Health Support Team"""
        send_myemail(app,email, "Thank you for your feedback", user_msg)
    else:
        msg="Invalid captcha code. Please try again";
    #generating new captcha
    pname=create_captcha();
    return render_template('feedback.html',captcha_img_name=pname,msg=msg);
# Run the project
if __name__ == '__main__':
    app.run(debug=True)
