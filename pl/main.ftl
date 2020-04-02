# LICENSE

welcome-hello-world = Witaj, świecie!

## Notifiactions

# $count (Number) - The count of new notifications.
notifications-new = {$count ->
    [one] W skrzynce odbiorczej jest jedno nowe powiadomienie.
    [few] W skrzynce odbiorczej jest {$count} nowe powiadomienia.
   *[many] W skrzynce odbiorczej jest {$count} nowych powiadomień.
}

# $lastDate (Date) - The date when the most recent notification was received.
notifications-last =
    Ostatnie powiadomienie otrzymano w dniu
    {DATETIME($lastDate, month: "long", day: "numeric")}.
