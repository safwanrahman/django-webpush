Django-Webpush
==============

Django-Webpush is a Package made for integrating and sending `Web Push
Notification <https://developer.mozilla.org/en/docs/Web/API/Push_API>`__
in Django Application. **This is a Work in Progress package. As the `Web
Push Notification specification <https://www.w3.org/TR/push-api/>`__ is
still in draft, things may change soon. So keep updated.**

\*Currently, it Supports Sending Push Notification to **Firefox 46+ and Chrome 50+**

--------------

Installation and Setup
----------------------

You can install it easily from pypi by running

::

    pip install django-webpush

After installing the package, add ``webpush`` in in your
``INSTALLED_APPS`` settings

::

    INSTALLED_APPS = (
        ...
        'webpush',
    )

If you would like to send notification to Google Chrome Users, you need
to add a ``WEBPUSH_SETTINGS`` entry with the **Google Cloud Messanging
ID and Key** Like following:

.. code:: python

    WEBPUSH_SETTINGS = {
        "GCM_ID": "Your GCM ID",
        "GCM_KEY":"Your GCM KEY"
    }

**Replace ``"Your GCM ID"`` and ``"Your GCM KEY"`` with your Google
Cloud Messanging ID and Key**

    **To know how to obtain GCM ID and Key please see this
    `Documentation from Google
    Developers <https://developers.google.com/web/fundamentals/getting-started/push-notifications/step-04?hl=en>`__
    and the `MDN
    Documentation <https://developer.mozilla.org/en-US/docs/Web/API/Push_API/Using_the_Push_API#Setting_up_Google_Cloud_Messaging>`__**

Then include ``webpush`` in the ``urls.py``

::

    urlpatterns =

        url(r'^webpush/', include('webpush.urls'))
    ]

Then run Migration by **``python manage.py migrate``**

Adding Web Push Information in Template
---------------------------------------

So in template, you need to load ``webpush_notifications`` custom
template tag by following: > - If you are using built in templating
engine, add ``{% load webpush_notifications %}`` in the template > - If
you are using jinja or other templating engine, you can manually add the
html header and button and other information. Documentation for them is
coming soon. Working on getting a automated way for jinja users. If you
would like to add support for them, patch are very much welcome.

Next, inside the ``<head></head>`` tag add ``{% webpush %}``. Like
following

::

    <head>
      {% webpush %}
    </head>

Next, inside the ``<body></body>`` tag, insert ``{% webush_button %}``
where you would like to see the **Subscribe to Push Messaging** Button.
Like following

::

    <body>
      <p> Hello World! </p>
      {% webpush_button %}
    </body>

    **Note:** The Push Notification Button will show only if the user is
    logged in or any ``group`` named is passed through ``webpush``
    context

***If you would like to mark the subscription as a group, like all
person subscribe for push notification from the template should be
marked as group and would get same notification, you should pass a
``webpush`` context to the template through views. The ``webpush``
context should have a dictionary like ``{"group": group_name}``*** .
Like following

::

     webpush = {"group": group_name } # The group_name should be the name you would define.

    return render(request, 'template.html',  {"webpush":webpush})

    **Note:** If you dont pass ``group`` through the ``webpush``
    context, only logged in users can see the button for subscription
    and able to get notification.

--------------

Sending Web Push Notification
-----------------------------

A Web Push generally have a header and body. According to the W3C
Specification, the data should be encrypted in transmission. the data is
addressed as payload generally. Also a TTL header should be included
indicating how much time the web push server store the data if the user
is not online. So in order to send notification, see below.

-  If you would like to send notification to a specific group, do like
   following:

   ::

       from webpush import send_group_notification

       payload = {"head": "Welcome!", "body": "Hello World"}

       send_group_notification(group_name="my_group", payload=payload, ttl=1000)
       # All subscribe subscribe through "my_group" will get a web push notification. A ttl of 1000 is passed so the web push server will store the data maximum 1000 milliseconds if any user is not online

-  If you would like to send Notification to a specific user, do like
   following \`\`\` from webpush import send\_user\_notification

   payload = {"head": "Welcome!", "body": "Hello World"}

   send\_user\_notification(user=user, payload=payload, ttl=1000) # Here
   in the user parameter, a user object should be passed # The user will
   get notification to all of his subscribed browser. A user can
   subscribe many browsers. \`\`\` **And the subscribers will get a
   notification like** |Web Push Notification|

License
=======

--------------

Copyright © 2016 by Safwan Rahman

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see http://www.gnu.org/licenses/.

.. |Web Push Notification| image:: http://i.imgur.com/VA6cxRc.png
