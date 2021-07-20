from flask import Flask, request, render_template
import joblib
import smtplib
import sqlite3

app = Flask(__name__)


def sendMail(msg, subject, toaddrs="sakshi.bhoyar27@gmail.com"):
    try:
        fromaddr = 'sakshi.bhoyar27@gmail.com'
        username = 'sakshi.bhoyar27@gmail.com'
        msg = 'Subject: {}\n\n{}'.format(subject, msg)
        password = 'delpvvpfjuzguifk'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

    except:
        print('failed to send')


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('database.db')
    data = {
        'pat': conn.execute("select * from patients").fetchall(),
        'doc': conn.execute("select * from doctor").fetchall()
    }
    return render_template('admin.html', data=data)


@app.route("/patient", methods=['GET', 'POST'])
def patient():

    return render_template('patientform.html')


@app.route("/doctor", methods=['GET', 'POST'])
def doctor():

    return render_template('doctorform.html')


@app.route("/doctorresults", methods=['GET', 'POST'])
def doctorresults():
    # getting data from form
    docname = request.form['name']
    name = request.form['pname']
    email = request.form['email']
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    cp = int(request.form['cp'])
    thal = int(request.form['thal'])
    nomv = int(request.form['nomv'])
    sp = int(request.form['sp'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    ca = int(request.form['ca'])
    exang = int(request.form['exang'])
    trestbps = int(request.form['trestbps'])
    oldpeak = float(request.form['oldpeak'])

    cholestrol = int(request.form['chol'])

    mdl = joblib.load('testop3.sav')
    conn = sqlite3.connect('database.db')

    t = [docname, name, age, gender, cp, trestbps, cholestrol, fbs, restecg, thal, exang,
         oldpeak, sp, ca, thal, 1]
    t = [str(i) for i in t]
    t = tuple(t)

    conn.execute(
        "INSERT INTO doctor Values {}".format(t))

    conn.commit()
    tempList = [[age, gender, cp, trestbps, cholestrol, fbs, restecg,
                 thal, exang, oldpeak, sp, ca, thal]]
    ans = f" According to the analysis, {name}, is highly susceptible to having heart related diseases." if mdl.predict(tempList)[
        0] == 0 else f"According to the analysis, {name} is unlikely to have heart related diseases."

    sendMail(ans, 'Test results', email)
    data = {
        'msg': ans,


    }

    if('susceptible' in ans):
        return render_template('danger.html', data=data)
    else:
        return render_template('healthy.html', data=data)


@app.route("/results", methods=['GET', 'POST'])
def result():
    # getting data from form
    name = request.form['name']
    email = request.form['email']
    age = int(request.form['age'])*365
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    gender = int(request.form['gender'])
    highBP = int(request.form['highBP']
                 ) if request.form['highBP'] != 'NA'else None
    lowBP = int(request.form['lowBP']
                ) if request.form['lowBP'] != 'NA'else None
    cholestrol = int(request.form['cholestrol'])
    gluc = int(request.form['gluc'])
    smoking = int(request.form['smoking'])
    alcohol = int(request.form['alcohol'])
    cvd = int(request.form['cvd'])

    tempList = [[age, gender, height, weight, highBP,
                 lowBP, cholestrol, gluc, smoking, alcohol, cvd]]
    # print(tempList)

    # no = [[20228, 1, 156, 85.0, 140, 90, 3, 1, 0, 0, 1]]
    # yes = [[18393, 2, 168, 62.0, 110, 80, 1, 1, 0, 0, 1]]
    mdl = joblib.load('testop2.sav')
    conn = sqlite3.connect('database.db')
    t = [name, email, age, height, weight, gender,
         highBP, lowBP, cholestrol, gluc, alcohol, cvd, smoking, mdl.predict(tempList)[0]]
    t = [str(i) for i in t]
    t = tuple(t)

    conn.execute(
        "INSERT INTO patients Values {}".format(t))

    conn.commit()

    ans = f"Hey {name}, According to the analysis you are highly susceptible to having heart related diseases." if mdl.predict(tempList)[
        0] == 0 else f"Hey {name} ,According to the analysis you are unlikely to have heart related diseases."

    sendMail(ans, 'Test results', email)
    data = {
        'msg': ans,

    }

    if('susceptible' in ans):
        return render_template('danger.html', data=data)
    else:
        return render_template('healthy.html', data=data)


if __name__ == "__main__":
    conn = sqlite3.connect('database.db')

    try:

        # create
        conn.execute('''CREATE TABLE patients(name TEXT, email TEXT, age TEXT, height TEXT, weight TEXT, gender TEXT, highBp TEXT, lowBp TEXT, cholestrol TEXT,
                                    gluc TEXT, alcohol TEXT, CVD TEXT, smoking TEXT, pred TEXT)''')

        conn.execute(
            '''CREATE TABLE doctor (name TEXT,dname TEXT,age TEXT, sex TEXT, cp TEXT, trestbps TEXT,chol TEXT,fbs TEXT,restecg TEXT,thalach TEXT ,exang TEXT,
        oldpeak TEXT,slope TEXT , ca TEXT, thal TEXT, pred TEXT )''')
    except:
        pass
    app.run(debug=True)
