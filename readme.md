# Flask API




## Notes

#regarding the logs : added the Elapsed_time and the fields of logs :
 timestamp, Elapsed_time, remote-addr, request-method,request-scheme, full_path, status
``` 
[2021-03-28 06:29:24,945] ERROR in app: [2021-Mar-28 06:29] 764.2476670742035 127.0.0.1 GET http /book? 200 OK 

```

## how to test


#to get all details of all:
-the api : /
-the body: nothing!


#to show all books
-the api : /show_books
-the body: nothing!

#to get details about specific book
-the api : /book
-the body:
```
{
    "title":"book_name"
}
```


#to add new book
-the api : /add_one
-the body:
```
{
    "title":"book_name"
}
```


#to delete book
-the api : /delete_book
-the body:
```
{
    "title" : "Hellion"  # "title":
}

```

