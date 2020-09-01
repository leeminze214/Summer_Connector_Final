from flask import Flask, redirect, render_template, request, url_for, session, abort,flash
from flask_socketio import SocketIO, join_room, leave_room
from db_class import config, methods

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkjhl2938h82h43ph9f0h8(*&go9d8fg'
io = SocketIO(app)
execute = methods(config) #database methods and connection 



#----------------------------------routes-------------------------------#

#login and signup page as default
@app.route('/', methods = ["GET","POST"])
def login():
    form = request.form.to_dict()

    if 'Username' in form and 'Password' in form:
        print('login',form)
        username = form['Username']
        password = form['Password']
        info = execute.login(username,password)

        if  info != False:
            
            session['username'] = info['name']
            session['age'] = info['age']
            session['location'] = info['location']
            
            return redirect(url_for('main_lobby'))

        flash("Invalid Login!")
    return render_template('login.html')

#signup submission will be sent here to process
@app.route('/signup', methods = ["GET","POST"])
def signup():
    form = request.form.to_dict()
    
    if 'Username' in form:

        print('signup',form)
        username = form['Username']
        password = form['Password']
        age = form['Age']
        location = form['Location']

        if execute.taken(username):

            flash('Username already exists!')
            return redirect('/')

        execute.signup(username,password,age,location)
        flash('Signup succesful! Login to connect now!')
    return redirect('/')

#after user logs in, they will be led to main lobby where they can join diff chatrooms
@app.route('/lobby')
def main_lobby():
    return render_template('lobby.html', name = session['username'])

#returns respective topic's chatroom, using socket.io rooms
@app.route('/lobby/<topic>')
def activity(topic):
    activities = ['basketball','swimming','hiking','soccer','camping']

    if topic in activities:

        return render_template('chat.html',topic = topic, name = session['username'])

    return abort(404, 'No chatroom found on topic')

#logout button will access this route redirect user to login
@app.route('/logout')
def logout():

    for i in session.keys():
        session.pop(None,i)

    return redirect('/')



#------------------------------------socket-------------------------------#

@io.on('connected')
def conn(data):
  
    room = data['room']
    join_room(room)
    
    print(room)
    print('a client ' + session['username']+' just joined room '+room ) 
 
    io.send(session['username']+' joined', room = room)

@io.on('disconnect')
def diss():
    leave_room()
    io.emit('disconnected')
    print('a client '+session['username']+' just left')

@io.on('message_sent')
def chatting(message_info):
    user_name =message_info['user_name']
    message_content =  message_info['message_val']
    room = message_info['room']
    print('A message has been sent: ',message_info)
    io.send(user_name+': '+message_content, room = room)

if __name__ == '__main__':
    io.run(app, debug = True)
