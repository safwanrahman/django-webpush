let url;
// Register event listener for the 'push' event.
self.addEventListener('push', function(event) {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  let payload = event.data ? event.data.text() : {"head": "No Content", "body": "No Content", "icon": "", "url": ""},
    data = JSON.parse(payload),
    head = data.head,
    body = data.body,
    icon = data.icon;
  // Url needs to be acessed from outside this method.
  url = data.url

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    // Show a notification with title 'ServiceWorker Cookbook' and use the payload
    // as the body.
    self.registration.showNotification(head, {
      body: body,
      icon: icon,
    })
  );
});

// When user clicks in the notification, opens a new window with the url 
// and closes the notification.
self.addEventListener('notificationclick', function (event) {
  event.waitUntil(
    self.clients.openWindow(url),
    event.notification.close()
  );
})

