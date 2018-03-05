Django-Webpush
==============

Django-Webpush is a Package made for integrating and sending `Web Push
Notification`_ in Django Application. **This is a Work in Progress
package. As the `Web Push Notification specification`_ is still in
draft, things may change soon. So keep updated.**

Currently, it Supports Sending Push Notification to **Firefox 46+ and
Chrome 52+**.

--------------

Installation and Setup
----------------------

You can install it easily from pypi by running

::

    pip install django-webpush

After installing the package, add ``webpush`` in in your
``INSTALLED_APPS`` settings

.. code:: python

        INSTALLED_APPS = (
            ...
            'webpush',
        )

If you would like to send notification to Google Chrome Users, you need
to add a ``WEBPUSH_SETTINGS`` entry with the **Vapid Credentials** Like
following:

.. code:: python

    WEBPUSH_SETTINGS = {
        "VAPID_PUBLIC_KEY": "Vapid Public Key",
        "VAPID_PRIVATE_KEY":"Vapid Private Key",
        "VAPID_ADMIN_EMAIL": "admin@example.com"
    }

**Replace ``"Vapid Public Key"`` and ``"Vapid Private Key"`` with your
Vapid Keys. Also replace ``admin@example.com`` with your email so that
the push server of browser can reach to you if anything goes wrong.**

    **To know how to obtain Vapid Keys please see this ```py_vapid```_
    and `Google Developer Documentation`_. You can obtain one easily
    from `web-push-codelab.glitch.me`_. ``Application Server Keys`` and
    ``Vapid Keys`` both are same.**

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

..

    **Note:** The Push Notification Button will show only if the user is
    logged in or any ``group`` named is passed through ``webpush``
    context

\***If you would like to mark the subscription as a gr

.. _Web Push Notification: https://developer.mozilla.org/en/docs/Web/API/Push_API
.. _Web Push Notification specification: https://www.w3.org/TR/push-api/
.. _``py_vapid``: https://github.com/web-push-libs/vapid/tree/master/python
.. _Google Developer Documentation: https://developers.google.com/web/fundamentals/push-notifications/subscribing-a-user#how_to_create_application_server_keys
.. _web-push-codelab.glitch.me: https://web-push-codelab.glitch.me/

