import json

from channels import Group

from api.models import Message
from django.contrib.auth.models import User

def message(message):
    data = json.loads(message.content['text'])
    print(data)
    if (data['type'] == 'handshake'):
        Group(str(data['user'])).add(message.reply_channel)
    elif (data['type'] == 'message'):
        new_message = Message.objects.create(
            text=data['text'],
            date_sent=int(data['date_sent']),
            author=User.objects.get(pk=data['author']),
            recipient=User.objects.get(pk=data['recipient'])
        )
        new_message.save()
        
        broadcast = {
            'type': 'new_message',
            'author': data['author'],
            'text': data['text']
        }
        Group(str(data['recipient'])).send({
            'text': json.dumps(broadcast)
        })
        
        reply = {
            'type': 'message_echo',
            'recipient': data['recipient'],
            'text': data['text']
        }
        message.reply_channel.send({
            'text': json.dumps(reply) 
        })
    elif (data['type'] == 'messages_read'):
        author = data['author']
        recipient = data['recipient']
        query = Message.objects.filter(author=author, recipient=recipient)
        for message in query:
            message.read = True
            message.save()
