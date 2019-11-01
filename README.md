This is our project crawler and model repository.
```
final
├── JSON					store the data for frontend, mainly graph object
├── Stream					tweet stream and search API
├── data					price, and tweet data retrieval and manipulation
├── model					model training and development (six in total)
└── requirement.txt				our project used modules
```
## Steps to run
1. run streaming: python3 Listener.py
2. run search: python3 Search.py
3. launch automatic crab: python3 crab.py

Then it will updated automatically at 1AM Melbourne time on a daily basis. 

Deployed Server:
http://45.113.234.255:3000

## Install Environment
1. git clone : git clone https://github.com/alanwangwyz/twitter-model.git
2. install virtualenv. **sudo pip3 install virtualenv**
3. create a new virtual environment: **virtualenv venv**
4. change to virtual environment: for Mac/Linux: **source venv/bin/activate**
5. **sudo pip3 install -r requirements.txt**  to install modules
6. leave environment: **deactivate**

This part provides the data for frontend. They should work together to show a complete picture.
https://github.com/bell0925/cryptographic
