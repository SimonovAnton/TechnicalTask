# TechnicalTask
A daemon that will provide an HTTP API for upload,
download (download) and delete files.

Use HTTP requests GET, POST, DELETE

Upload:
- having received the file from the client,  returns in a separate field http response hash of the uploaded file
-  saves the file to disk in the following directory structure:
store / ab / abcdef12345 ...
where "abcdef12345 ..." is a file name that matches its hash.
/ ab / - a subdirectory consisting of the first two characters of the file hash

Download:
Download request: the client passes the parameter - the hash of the file. Demon seeks file in local storage and gives it if it finds it.

Delete:
Delete request: the client passes the file hash parameter. Demon seeks file in local storage and deletes it if found.
