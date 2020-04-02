# LICENSE

welcome-hello-world = Hello, world!
# $userName (String) - The user's first name.
welcome-hello-user = Hello, {$userName}!
welcome-about = Welcome to {-product-name} by {-brand-name}.

## Notifications

# $count (Number) - The count of unread notifications.
notifications-unread = You have {$count ->
    [one] one unread notification
   *[other] {$count} unread notifications
} in your inbox.


# $count (Number) - The count of new notifications.
notifications-new = {$count ->
    [one] You have one new notification in your inbox.
   *[other] You have {$count} unread notifications in your inbox.
}

# $lastDate (Date) - The date when the most recent notification was received.
notifications-last = Last notification received on {DATETIME($lastDate, weekday: "long")}.
