# This is a peer to peer file sharing python CLI application

Clone this repo to your local machine

Move to P2P_filesharing folder and run below command to start the flask server

###### python server\controller\request_controller.py

This starts the flask server and listens in localhost:5000
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/server_start.PNG)
Open up another terminal and run the below command inside P2P_filesharing folder

###### python client\scripts\p2p_filesharing.py
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/client_start.PNG)
This start the client application and prompts the user to enter the commands(Ping, search, download, exit)

## Ping functionality
Select ping command and select default host. This will list down the files available inside the host as below
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/ping_response.PNG)

## Search functionality
Select search command and enter filename to search. This will searches the file and sends back the server
ip and port which is having the entered filename
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/file_search.PNG)

## Download functionality
Select download command and enter filename to download. Enter the ip and port details obtained from above
search results. This will connects to the download api and a socket will be created from the server to the client
and the file will be transferred to the client and saved locally
ip and port which is having the entered filename
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/download_progress.PNG)

## Exit functionality
Select exit command and this will terminates the client and removes the client address from the active
peer list bucket in S3(This functioanlity is just having the prototype, not completely implemented)
![alt text](https://github.com/naveenpragathesh/p2pfileshare/blob/master/readme_images/exit.PNG)


