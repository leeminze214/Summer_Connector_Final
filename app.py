from flask import Flask, redirect, render_template, request, url_for, session, abort,flash
from flask_socketio import SocketIO, join_room, leave_room, emit, send, disconnect, Namespace
from db_class import methods, db_uri


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasf2(*H)83hf0283f)#*'
socketio = SocketIO(app)
execute = methods(db_uri) #database methods and connection 



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


#logout button will access this route redirect user to login
@app.route('/logout')
def logout():

    for i in list(session.keys()):
        session.pop(None,i)

    return redirect('/')



#------------------------------------socket-------------------------------#
#rooms = ['lobby','basketball','soccer','swimming']
@socketio.on('connected')
def connection(name):
    join_room('lobby')
    send(name +' has joined the lobby', room='lobby')
    print('join lobby')

@socketio.on('message_sent')
def message_received(data):
    print(data)
    send(data['user_name']+': '+data['msg'], room=data['room'])

@socketio.on('logout')
def logingout():
    print('logout')
    disconnect()

@socketio.on('join_room')
def specific_room(data):
    
    prev_room = data['prev']
    room = data['room']
    if prev_room != room:
        send(data['name']+' has left '+prev_room, room = prev_room)
        emit('clear_chat')
        
        
        leave_room(prev_room)
        print(prev_room,room)
        join_room(room)
        if room !='lobby':
            emit('new_room')
            send(data['name']+' has joined '+data['room'],room=data['room'])
        
if __name__ == '__main__':
    socketio.run(app, debug = True)#, using heroku now so no need
    #app.run()
