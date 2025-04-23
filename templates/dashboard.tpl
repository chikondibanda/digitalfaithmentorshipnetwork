<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <h1>Welcome, <%= user[1] %> <%= user[2] %>!</h1>
    <p>Email: <%= user[4] %></p>
    <p>Phone: <%= user[5] %></p>
    <p>Profile Picture: <img src="<%= user[6] %>" alt="Profile Picture" width="150" height="150"></p>
    <a href="/logout">Logout</a>
</body>
</html>