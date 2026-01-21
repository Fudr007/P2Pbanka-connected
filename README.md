# P2Pbanka ESSENTIALS

This is a TCP-based bank node implementing a P2P network.  
Each node represents a bank and supports commands for creating accounts, depositing, withdrawing, checking balances, and more.

---

## Requirements

- Python 3.10+  
- cx_Oracle library
- Oracle client / connection details  
- Access to local network for TCP connections  

---

## Setup and usage
1. Download zip source code
2. Install Python dependencies:

```bash
pip install cx_Oracle
```
3. Configure your database credentials, file paths and server details in config.ini
```ini
[server]
host = IP ADDRESS OF YOUR SERVER (PC)
port = PORT ON WHICH YOU WANT TO RUN THE SERVER (65525 - 65535)
timeout = TIMOUT TIME IN SECONDS
[database]
user = ORACLE XE DB USER YOU WANT TO USE
password = PASSWORD TO THAT USER
host = IP ADDRESS OF THE ORACLE XE SERVER
port = PORT ON WHICH THE DATAABSE SERVER RUN
service = SERVICE NAME
encoding = ENCODING OF SQL
[path]
db_code = PATH TO THE SQL TABLE CREATION CODE
log = PATH WHERE YOU WANT TO SAVE THE LOG
```
4. In CMD (or similar alternative) go to the source folder(where the main.py is)
5. Run this command to start the program:
```bash
py main.py
```
6. Then if server is running you can open PuTTY(or similar), connect to the server via the displayed server credentials in CMD
7. Now you can use these commands and after each hit enter for execute:
* ```BC``` returns code(ip) of the bank
* ```AC``` creates new account and retuns its <number>/<bank code>
* ```AD account_number/bank_code amount``` deposits amount to the selected account
* ```AW account_number/bank_code amount``` withdraw amount for the selected account if enough funds
* ```AB account_number/bank_code``` returns balance that is on the selected account
* ```AR account_number/bank_code``` removes the selected account
* ```BA``` returns how much resources is in the accounts combined
* ```BN``` returns how many accounts are in the bank

## Reusable resources:
* https://github.com/Fudr007/DBhallReservationD1/blob/main/Src/DBconnect.py (without Singleton)
* https://github.com/Fudr007/DBhallReservationD1/blob/main/Src/Config/Sql_load.py
* https://github.com/Fudr007/DBhallReservationD1/blob/main/Src/Config/Config_load.py (customised for this project)

## Resources:
* https://chatgpt.com/share/696cc9d0-a2f4-8003-aa7d-f5f3d39b8a2d
* https://gemini.google.com/share/9b6a6959e7e4
