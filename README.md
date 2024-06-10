# Socket Programming Project
## Setup Development Enviroment
We must using Python 3.9.6.
### Installation docker for linux
1. Install docker For Debian/Ubuntu or Debian-based
```
# update and install necessary tools
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# add key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
### Running services and docker
1. Running services
```
sh start_services.sh
```
2. Running docker (mongoDB)
```
sh start_docker.sh
```

## Using services
### Create client account
1. Using domain http://localhost:5000/signup to signup an account
- We should use Postman to create an account with the structure:
```
{
  "username": "example@gmail.com",
  "password": "secretpassword",
  "nameaccount": "example1"
}
```
### Login client account
1. Using domain http://localhost:5000/login to login an account
- The structure to login an account:
```
{
  "username": "example@gmail.com",
  "password": "secretpassword"
}
```
2. After login into the client account the server will response a json file have information about client and one accessToken key using for login to the client programming.
```
{
    "Access Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaGFuaGxvbmdkZXB0cmFpOEBnbWFpbC5jb20gbG9uZ2RlcHRyYWkiLCJleHAiOjE3MTgwNDEwMjl9.V78PN2xSgOpDURw-6o5aCDyj9yUsdTA8nxgLXMFoYwe",
    "Name Account": "example1",
    "User Name": "example@gmail.com",
    "User Password": "secretpassword"
}
```
### Running client program
1. we must go to the client file in the api source.
```
cd services/client
```
2. Running client file
```
python InitializeSocketClient.py
```
3. Write the accessToken for service's require:
```
Please input the Access Token: '...'
```
4. Choose chat mode we want to client using (private or group chat)
```
Choose chat mode (private/group): 'private/group'
```
5. If we choose private the server will response for us the text to announce us to input the nickname of another client we want to communicate
   - For example if we have 2 accounts with username are 'example1' and 'example2':
     + We must login 2 accounts on the program and using account 'example1' to connect with the account 'example2', and vice versa.
     + After that they can communicate together.
```
Account example1: Enter the nickname of the user you want to chat with: 'example2'
Account example2: Enter the nickname of the user you want to chat with: 'example1'
```
6. If we choose group, the server will bring the client to the broadcast and all client joined can talk together.




