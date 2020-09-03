$(document).ready(()=>{ 
    room = 'lobby'
    name = $('#name').text()
    const socket = io()
    //--------------------------------
    $('#lobby').on('click',()=>{
        prev_room = room
        room = 'lobby'
        console.log(prev_room,room)
        socket.emit('join_room',{'room':room,'prev':prev_room,'name':name})
        
    })
    $('#basketball').on('click',()=>{
        prev_room = room
        room = 'basketball'
        console.log(prev_room,room);
        socket.emit('join_room',{'room':room,'prev':prev_room,'name':name})
        
    })
    $('#soccer').on('click',()=>{
        prev_room = room
        room = 'soccer'
        console.log(prev_room,room);
        socket.emit('join_room',{'room':room,'prev':prev_room,'name':name})
        
    })
    $('#swimming').on('click',()=>{
        prev_room = room
        room = 'swimming'
        console.log(prev_room,room);
        socket.emit('join_room',{'room':room,'prev':prev_room,'name':name})
        
    })
    //--------------------------------------------------------


    socket.on('connect', ()=>{
        socket.emit('connected', name)
        console.log('joinlobby');
        
    });
    socket.on('disconnect', ()=>{
        console.log('disconnected');
    });
    socket.on('message',(message)=>{
        console.log(message);
        $('#chathead').append('<div class="container"><p id = "chatmsg">'+message+'</p></div>');
    });
    socket.on('clear_chat',()=>{

        $('#chathead').empty()
    });

    $('#chat').on('submit', (e)=>{
        e.preventDefault() //prevent the default post request, turns to socket.send instead
        var msg = $('#chat_message').val()//use .val() to access input fields
        $('#chat_message').val('')
        socket.emit('message_sent',{'user_name':name,'msg':msg,'room':room});//room is the topic of the chatroom
    });

    $('#logout').on('click',()=>{
        socket.emit('logout')
    });

});
