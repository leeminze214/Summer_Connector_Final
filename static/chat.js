$(document).ready(()=>{
    var name = $('#name').text()
    console.log(name)
    const room = $('#topic').text()
    const socket = io()
    socket.on('connect', ()=>{
    
        console.log("A CLIENT "+name+" HAS CONNECTED");
        socket.emit('connected',{'room':room})
    });
 
    socket.on('disconnected',()=>{

        $('h1#chatspace').append('<div class="container"><p id = "chatmsg">'+name+' has disconnected</p></div>');

    });
    socket.on('message',(message)=>{
        $('h1#chatspace').append('<div class="container"><p id = "chatmsg">'+message+'</p></div>');
    });
    $('#chat').on('submit', (e)=>{
        e.preventDefault() //prevent the default post request, turns to socket.send instead
        var msg = $('#chat_message').val()//use .val() to access input fields
        $('#chat_message').val('')
        console.log(room)
        socket.emit('message_sent',{'user_name':name,'message_val':msg,'room':room});//room is the topic of the chatroom
    });

});