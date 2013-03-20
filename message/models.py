from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import truncate_words
from django.contrib.auth.models import User
from message.managers import (MessageManager, MessageContactManager)

class MessageContact(models.Model):
    from_user = models.ForeignKey(User, verbose_name=_("from user"),
                                  related_name=('from_users'))

    to_user = models.ForeignKey(User, verbose_name=_("to user"),
                                related_name=('to_users'))

    latest_message = models.ForeignKey('Message',
                                       verbose_name=_("latest message"))

    objects = MessageContactManager()

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['latest_message']
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")

    def __unicode__(self):
        return (_("%(from_user)s and %(to_user)s")
                % {'from_user': self.from_user.username,
                   'to_user': self.to_user.username})

    def opposite_user(self, user):
        if self.from_user == user:
            return self.to_user
        else: return self.from_user


class Message(models.Model):
    """ Private message model, from user to user(s) """
    body = models.TextField(_("body"))

    sender = models.ForeignKey(User,
                               related_name='sent_messages')
    receiver = models.ForeignKey(User,
                               related_name='receive_messages')

    sent_at = models.DateTimeField(_("sent at"),
                                   auto_now_add=True)
    read_at = models.DateTimeField(_("read at"),
                                   null=True,blank=True)

    sender_deleted_at = models.DateTimeField(_("sender deleted at"),
                                             null=True,
                                             blank=True)
    receiver_deleted_at = models.DateTimeField(_("sender deleted at"),
                                             null=True,
                                             blank=True)

    objects = MessageManager()

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __unicode__(self):
        """ Human representation, displaying first ten words of the body. """
        truncated_body = truncate_words(self.body, 10)
        return "%(truncated_body)s" % {'truncated_body': truncated_body}


    def update_contacts(self, to_user_list):
        """
        Updates the contacts that are used for this message.

        :param to_user_list:
            List of Django :class:`User`.

        :return:
            A boolean if a user is contact is updated.

        """
        updated = False
        for user in to_user_list:
            MessageContact.objects.update_contact(self.sender,
                                                  user,
                                                  self)
            updated = True
        return updated
