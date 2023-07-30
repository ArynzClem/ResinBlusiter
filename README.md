# ResinBlusiter
ResinBlusiter is a script for performing ddos attacks

#installation and run 
git clone https://github.com/ArynzClem/ResinBlusiter/

cd ResinBlusiter

pip3 install -r requirements.txt

python3 RB.py

#Features
1. HTTP Flood
2. TCP Flood
3. UDP Flood
4. Random UDP Attack
5. DNS Reflection Attack
6. Layer 7 Attack (HTTP/TCP)
7. Slowloris Attack
8. SYN Flood
9. FTP Flood
10. SCTP Flood


#Note
if there is error server.bind(("0.0.0.0", 1337)) OSError: [Errno 98} address aleredy use

indicates that the port you are trying to use (port 1337) is already in use by another process

Stop Process Using Port 1337:

You can try to find processes using port 1337 and stop them. On Linux or macOS, you can use the following command to find processes using port 1337:
css
Copy code
sudo lsof -i :1337
Then, you can terminate the process by using its process ID:
bash
Copy code
kill -9 <PID>
