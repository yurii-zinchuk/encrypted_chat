# Encrypted Chat
## Description
This is final project of the discrete maths course. We had to develop a messenger that would allow users to chat securely without bothering that any of the exchanged information might be intercepted. Our chat uses RSA algorithms for encrypting messages that are being sent. It also has a nice GUI that makes it easy to use.

## Usage
To use the messenger, you will have to undertake several steps, once you have cloned the project and navigated to its directory in terminal on your machine.

Firstly, you will have to set up the server, since our messenger runs on it. It is very easy to do:
```bash
python3 server.py
```
Once you have your server running, you can start clients that will join the group chat. This is also extremely easy:
```bash
python3 client.py
```
You will see a window asking for a username. You will have to enter it before joining the chat. After you do that, you will see a GUI chat window. From this point everything is easily understood. Write your message in the box at the bottom of the window, send it using "Send" button or by pressing "Enter" on the keyboard.
!!! One important thing: messenger only supports English alphabet, numbers and basic punctuation. !!!

## Algorithms
Apart from RSA that is being used in the chat, we have also developed oher encryption algorithms. These are: DSA, ECC, El-Gamal, and Rabin Cryptosystem. You can see their broader description in the project's Wiki.
