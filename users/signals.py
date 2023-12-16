
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile, Message
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)


        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

def sendNotification(sender, instance, created, **kwargs):
    if created:
        subject = f"You have a new message ({instance.recipient.unreadCount} unread message)"
        context = {'recipient_name': instance.recipient.name, 'sender_name': instance.sender.name, 'message': instance.body, 'subject': instance.subject}
        html_message = render_to_string('users/new_message_noti.html', context)
        plain_message = strip_tags(html_message)
        recipient_email = instance.recipient.email

        try:
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(e)
            pass

    #print('Unread Count:', instance.recipient.unreadCount)


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(sendNotification, sender=Message)