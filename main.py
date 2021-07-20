from flask import Flask, request, render_template
import instainfo

import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = 'database.db'
# conn = sqlite3.connect('database.db')


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def update_task(conn, task):
    sql = ''' UPDATE userstats
              SET profile_pic = ? ,
                  followers_count = ? ,
                  followed_count = ? ,
                  isPrivate = ? ,
                  isBusiness = ? 
              WHERE username = ?'''
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/admin/all", methods=['GET'])
def ListAll():
    conn = sqlite3.connect('database.db')
    conn.cursor.execute('''SELECT * from userstats''')
    allusersstats = conn.cursor.fetchall()
    return render_template('listall.html', allusersstats=allusersstats)

@app.route('/api/<username>', methods=['GET'])
def GetInstaStats(username):
    # Create an instance of the class
    print(username)
    userObj = instainfo.UserProfile(username)
    # Prints the users profile picture URL
    userStats = {   
        'profile_pic': userObj.GetProfilePicURL(),
        'followers_count': userObj.FollowersCount(),
        'followed_count': userObj.FollowedByCount(),
        'isPrivate': userObj.IsPrivate(),
        'isBusiness': userObj.IsBusinessAccount()

    }
    # conn = sqlite3.connect('database.db')

    # update_task(conn, (str(userStats['profile_pic']),int(userStats['followers_count']),int(userStats['followed_count']),str(userStats['isPrivate']),str(userStats['isBusiness']),str(username)))
    
    return render_template('index.html', userStats=userStats, username=username)


    

if __name__ == "__main__":
    try:
        conn = sqlite3.connect('database.db')
        sql_create_userStats_table = """ CREATE TABLE IF NOT EXISTS userstats (
                                        username text PRIMARY KEY,
                                        profile_pic text NOT NULL,
                                        followers_count integer NOT NULL,
                                        followed_count integer NOT NULL,
                                        isPrivate text,    
                                        isBusiness text
                                    ); """
        if conn is not None:
        # create projects table
            create_table(conn, sql_create_userStats_table)
        else:
            print("Error! cannot create the database connection.")

    except Error as e:
        print(e)

    # conn = sqlite3.connect('database.db')
    app.run(debug=True)