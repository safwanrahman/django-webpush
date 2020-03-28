
Django-Webpush
===================
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/safwanrahman)

Django-Webpush is a Package made for integrating and sending [Web Push Notification](https://developer.mozilla.org/en/docs/Web/API/Push_API) in Django Application.

Currently, it Supports Sending Push Notification to **Firefox 46+ and Chrome 52+**.

----------


Installation and Setup
-------------

You can install it easily from pypi by running

    pip install django-webpush

After installing the package, add `webpush` in in your `INSTALLED_APPS` settings

```python
INSTALLED_APPS = (
    ...
    'webpush',
)
```

If you would like to send notification to Google Chrome Users, you need to add a ``WEBPUSH_SETTINGS`` entry with the **Vapid Credentials** Like following:
```python
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "Vapid Public Key",
    "VAPID_PRIVATE_KEY":"Vapid Private Key",
    "VAPID_ADMIN_EMAIL": "admin@example.com"
}
```
**Replace ``"Vapid Public Key"`` and ``"Vapid Private Key"`` with your Vapid Keys. Also replace ``admin@example.com`` with your email so that the push server of browser can reach to you if anything goes wrong.**

> **To know how to obtain Vapid Keys please see this [`py_vapid`](https://github.com/web-push-libs/vapid/tree/master/python) and [Google Developer Documentation](https://developers.google.com/web/fundamentals/push-notifications/subscribing-a-user#how_to_create_application_server_keys). You can obtain one easily from [web-push-codelab.glitch.me](https://web-push-codelab.glitch.me/). ``Application Server Keys`` and ``Vapid Keys`` both are same.**

Then include `webpush` in the `urls.py`

```python
urlpatterns =  [
    url(r'^webpush/', include('webpush.urls'))
]
  ```


`django-webpush` is shipped with built in **`jinja`** support.
If you would like to use with jinja backend,
pass ``pipeline.jinja2.PipelineExtension`` to your jinja environment. Like following:

```python
{
    "BACKEND": "django_jinja.backend.Jinja2",
    "OPTIONS": {
      'extensions': ['webpush.jinja2.WebPushExtension'],
    }
},
```


**Then run Migration by ***`python manage.py migrate`*****



Adding Web Push Information in Template
-------------------

So in template, you need to load `webpush_notifications` custom template tag by following:
- If you are using built in templating engine, add `{% load webpush_notifications %}` in the template
- If you are using **jinja** templating engine, you do not need to load anything.

Next, inside the `<head></head>` tag add `webpush_header` according to your templating engine:

```html
<head>
  # For django templating engine
  {% webpush_header %}
  # For jinja templating engine
  {{ webpush_header() }}
</head>
```
Next, inside the `<body></body>` tag, insert `webush_button` where you would like to see the **Subscribe to Push Messaging** Button. Like following

```html
<body>
  <p> Hello World! </p>
  # For django templating engine
  {% webpush_button %}
  # For jinja templating engine
  {{ webpush_button() }}
</body>
```

Or if you want to add custom classes (e.g. bootstrap)

```html
<body>
  <p> Hello World! </p>
  # For django templating engine
  {% webpush_button with_class="btn btn-outline-info" %}
  # For jinja templating engine
  {{ webpush_button(with_class="btn btn-outline-info") }}
</body>
```

 >**Note:** The Push Notification Button will show only if the user is logged in or any `group` named is passed through `webpush` context

 ***If you would like to mark the subscription as a group, like all person subscribe for push notification from the template should be marked as group and would get same notification, you should pass a `webpush` context to the template through views. The `webpush` context should have a dictionary like `{"group": group_name}`*** . Like following

```python
 webpush = {"group": group_name } # The group_name should be the name you would define.

return render(request, 'template.html',  {"webpush":webpush})
```
> **Note:** If you dont pass `group` through the `webpush` context, only logged in users can see the button for subscription and able to get notification.

----------

Sending Web Push Notification
-------------------

A Web Push generally have a header and body. According to the W3C Specification, the data should be encrypted in transmission. The data is addressed as payload generally. Also a TTL header should be included indicating how much time the web push server store the data if the user is not online.
So in order to send notification, see below.

- If you would like to send notification to a specific group, do like following:


    ```python
    from webpush import send_group_notification

    payload = {"head": "Welcome!", "body": "Hello World"}

    send_group_notification(group_name="my_group", payload=payload, ttl=1000)
    # All subscribe subscribe through "my_group" will get a web push notification.
    # A ttl of 1000 is passed so the web push server will store
    # the data maximum 1000 seconds if any user is not online

    ```

- If you would like to send Notification to a specific user, do like following
    ```python
    from webpush import send_user_notification

    payload = {"head": "Welcome!", "body": "Hello World"}

    send_user_notification(user=user, payload=payload, ttl=1000)
    # Here in the user parameter, a user object should be passed
    # The user will get notification to all of his subscribed browser. A user can subscribe many browsers.
    ```

    **And the subscribers will get a notification like:**

![Web Push Notification](http://i.imgur.com/VA6cxRc.png)

- If you notification should have an icon or open a url when clicked, you can add those to the payload:

    ``` python
    from webpush import send_user_notification
    
    from webpush import send_group_notification

    payload = {"head": "Welcome!", "body”: "Hello World", 
               "icon": "https://i.imgur.com/dRDxiCQ.png“, "url": "https://www.example.com"}

    send_group_notification(group_name="my_group", payload=payload, ttl=1000)
    ```
**And the subscribers will get a notification like:**

![Web Push Notification icon](http://i.imgur.com/Vr1RMvF.png)

**That will open https://www.example.com if clicked.**
 
- If you want fine grained control over sending a single push message, do like following


    ```python
    from webpush.utils import send_to_subscription

    payload = {"head": "Welcome!", "body": "Hello World"}

    user = request.user
    push_infos = user.webpush_info.select_related("subscription")
    for push_info in push_infos:
        send_to_subscription(push_info.subscription, payload)

    ```
    


 
 
 **And the subscribers will get a notification like**
 ![Web Push Notification](http://i.imgur.com/VA6cxRc.png)


License
=======
----
Copyright © 2018 Safwan Rahman

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
