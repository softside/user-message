from django.db import models
from django.db.models import Q
import datetime

class MessageContactManager(models.Manager):
    """ Manager for the :class:`MessageContact` model """

    def get_or_create(self, from_user, to_user, message):
        """
        Get or create a Contact

        We override Django's :func:`get_or_create` because we want contact to
        be unique in a bi-directional manner.

        """
        created = False
        try:
            contact = self.get(Q(from_user=from_user, to_user=to_user) |
                               Q(from_user=to_user, to_user=from_user))

        except self.model.DoesNotExist:
            created = True
            contact = self.create(from_user=from_user,
                                  to_user=to_user,
                                  latest_message=message)

        return (contact, created)

    def update_contact(self, from_user, to_user, message):
        """ Get or update a contacts information """
        contact, created = self.get_or_create(from_user,
                                              to_user,
                                              message)

        # If the contact already existed, update the message
        if not created:
            contact.latest_message = message
            contact.save()
        return contact

    def get_contacts_for(self, user):
        """
        Returns the contacts for this user.

        Contacts are other users that this user has received messages
        from or send messages to.

        :param user:
            The :class:`User` which to get the contacts for.

        """
        contacts = self.filter(Q(from_user=user) | Q(to_user=user))
        return contacts

class MessageManager(models.Manager):
    """ Manager for the :class:`Message` model. """

    def send_message(self, sender, to_user, body):
        """
        Send a message from a user, to a user.

        :param sender:
            The :class:`User` which sends the message.

        :param to_user_list:
            A list which elements are :class:`User` to whom the message is for.

        :param message:
            String containing the message.

        """
        msg = self.model(sender=sender,receiver=to_user,
                         body=body)
        msg.save()
        return msg

    def get_conversation_between(self, from_user, to_user):
        """ Returns a conversation between two users """
        messages = self.filter(Q(sender=from_user, receiver=to_user,
                                 sender_deleted_at__isnull=True)|
                               Q(sender=to_user, receiver=from_user,                                                                       receiver_deleted_at__isnull=True))
        return messages

    def count_unread_messages_for(self,user):
        unread_total = self.filter(receiver=user,
                                   read_at__isnull=True,
                                   receiver_deleted_at__isnull=True).count()
        return unread_total

    def count_unread_messages_between(self,from_user,to_user):
        unread_total = self.filter(sender=from_user,
                                   receiver=to_user,
                                   read_at__isnull=True,
                                   sender_deleted_at__isnull=True).count()

        return unread_total
