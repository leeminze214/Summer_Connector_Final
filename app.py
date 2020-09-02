from flask import Flask, redirect, render_template, request, url_for, session, abort,flash
from flask_socketio import SocketIO, join_room, leave_room, emit, send, disconnect
from db_class import config, methods

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkjhl2938h82h43ph9f0h8(*&go9d8fg'
socketio = SocketIO(app)
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
    socketio.emit('joined lobby', {'name':session['username']})
    return render_template('lobby.html', name = session['username'])


#logout button will access this route redirect user to login
@app.route('/logout')
def logout():

    for i in session.keys():
        session.pop(None,i)

    return redirect('/')



#------------------------------------socket-------------------------------#
@socketio.on('connected')
def connection():
    print('join lobby')
@socketio.on('connected', namespace='/test')
def connection1():
    print('join lobby test')
'''
@socketio.on('disconnect')
def dis():
    print('discconectmain')
@socketio.on('disconnect', namespace='/test')
def dis2():
    print('disssecond')
'''
@socketio.on('message_sent')
def message_received(data):
    print(data)
    send(data['user_name']+': '+data['msg']+' from '+data['room'])

@socketio.on('message_sent', namespace ='/test')
def message_received1(data):
    print(data)
    send(data['user_name']+': '+data['msg']+' from '+data['room'])

@socketio.on('change')
def changing(data):
    del data['namespaces']['/']
    for i in data['namespaces'].keys():

        disconnect(namespace=i)
        print('disconnect from '+i)
    
@socketio.on('change', namespace='/test')
def changin2g(data):
    del data['namespaces']['/test']
    for i in data['namespaces'].keys():
        disconnect(namespace=i)
        print('disconnect from '+i)


if __name__ == '__main__':
    socketio.run(app, debug = True)
