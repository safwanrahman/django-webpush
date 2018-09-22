// Register event listener for the 'push' event.
self.addEventListener('push', function(event) {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  let payload = event.data ? event.data.text() : {"head": "No Content", "body": "No Content", "icon": ""},
    data = JSON.parse(payload),
    head = data.head,
    body = data.body,
    icon = data.icon;
    // If no url was received, it opens the home page of the website that sent the notification
    // Whitout this, it would open undefined or the service worker file.
    url = data.url ? data.url: self.location.origin;

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    // Show a notification with title 'ServiceWorker Cookbook' and use the payload
    // as the body.
    self.registration.showNotification(head, {
      body: body,
      icon: icon,
      data: {url: url}	
    })
  );
});

self.addEventListener('notificationclick', function (event) {
  event.waitUntil(
    event.preventDefault(),
    event.notification.close(),
    self.clients.openWindow(event.notification.data.url)
  );
})

