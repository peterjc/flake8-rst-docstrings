"""Module description here.

This is an example from the Sphinx documentation, although
I'm not sure how one might put it into the function's docstring,
the point here is to use a Sphinx directive:

.. py:function:: send_message(sender, recipient, message_body, [priority=1])

   Send a message to a recipient

   :param str sender: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring

The end.
"""


class X(object):
    """This is :class:`X` which is an example.

    Can also include the Python namespace in the Sphinx
    notation :py:class:`X` as well.

    The point of this test is to check we don't get::

        RST304 Unknown interpreted text role "class".
        RST304 Unknown interpreted text role "py:class".

    This is because these are now on the default list of roles.
    """

    pass
