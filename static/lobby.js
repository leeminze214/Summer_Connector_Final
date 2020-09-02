$(document).ready(()=>{    
    namespaces = {'/':'/','/test':'/test','d':'sdf'}
    name = $('#name').text()
    $('#test').on('click',()=>{
        
        const socket = io()
        
        socket.emit('change',{'namespaces':namespaces,'this':'/'})
        $('#chat').on('submit', (e)=>{
            e.preventDefault() //prevent the default post request, turns to socket.send instead
            var msg = $('#chat_message').val()//use .val() to access input fields
            $('#chat_message').val('')
        
            socket.emit('message_sent',{'user_name':name,'msg':msg,'room':'main'});//room is the topic of the chatroom
        });
       
        socket.on('connect', ()=>{
            socket.emit('connected')
            console.log('joinlobby');
            alert(' joined the main lobby')
        });

        socket.on('message',(message)=>{
            $('h1#chatspace').append('<div class="container"><p id = "chatmsg">'+message+'</p></div>');
        });

        socket.on('disconnect', ()=>{
            console.log('disconnmain');
            alert('disconnmain')
        });
    });
    //-------------------------------------------------------------------------------
    $('#test2').on('click',()=>{
        
        const test = io('/test')
        
        test.emit('change',{'namespaces':namespaces,'this':'/test'})
        
        test.on('connect', ()=>{
            test.emit('connected')
            console.log('joinlobby');
            alert(' joined the second lobby')
        });

        $('#chat').on('submit', (e)=>{
            e.preventDefault() //prevent the default post request, turns to socket.send instead
            var msg = $('#chat_message').val()//use .val() to access input fields
            $('#chat_message').val('')
            console.log({'user_name':name,'msg':msg,'room':'test'});
            test.emit('message_sent',{'user_name':name,'msg':msg,'room':'test'});//room is the topic of the chatroom
        });

        test.on('message',(message)=>{
            $('h1#chatspace').append('<div class="container"><p id = "chatmsg">'+message+'</p></div>');
        });

        test.on('disconnect', ()=>{
            console.log('disconn222');
            alert('disconn222')
        });
    });
        
 




});