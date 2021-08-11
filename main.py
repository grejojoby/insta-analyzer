from sqlite3.dbapi2 import DatabaseError
from flask import Flask, request, render_template
import instainfo
import os
import sqlite3
from sqlite3 import Error
from datetime import date


app = Flask(__name__)

DATABASE = 'database.db'
# conn = sqlite3.connect('database.db')



def update_task(conn, task):
    conn.execute("INSERT INTO Info Values {}".format(task))
    conn.commit()

  
# update_task()
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/admin/all", methods=['GET'])
def ListAll():
    conn = sqlite3.connect('database.db')
    allusersstats =conn.execute('''SELECT * from Info''').fetchall()
    print(allusersstats)
    return render_template('listall.html', allusersstats=allusersstats,title="All User Stats")

@app.route("/admin/<username>", methods=['GET'])
def ListAllUsername(username):
    conn = sqlite3.connect('database.db')
    allusersstats =conn.execute('SELECT * from Info').fetchall()
    allusersstats=[i for i in allusersstats  if i[1]==username ]
    return render_template('listall.html', allusersstats=allusersstats,title="%s stats"%username)

@app.route('/api/<username>', methods=['GET'])
def GetInstaStats(username):
    # Create an instance of the class
    userObj = instainfo.UserProfile(username)
    # Prints the users profile picture URL
    userStats = {   
        'profile_pic': userObj.GetProfilePicURL(),
        'followers_count': userObj.FollowersCount(),
        'followed_count': userObj.FollowedByCount(),
        'isPrivate': userObj.IsPrivate(),
        'isBusiness': userObj.IsBusinessAccount()

    }
    conn = sqlite3.connect('database.db')
    today = date.today()
    update_task(conn, (str(today),username,int(userStats['followers_count']),int(userStats['followed_count']),str(userStats['isPrivate']),str(userStats['isBusiness'])))
    
    return render_template('index.html', userStats=userStats, username=username)


    

if __name__ == "__main__":
    # os.remove(DATABASE)
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS Info(date TEXT,username TEXT, followers_count INTEGER, followed_count INTEGER, isPrivate TEXT, isBusiness TEXT)''')
    conn.close()
    app.run(debug=True)
