import os 
import json 

config = json.load(open('config.json'))

if os.path.exists(config['filepath']):
    os.remove(config['filepath'])

os.mkifo(config['filepath'],0o600)

print("FIFO named '%s' is crated successfully."% config['filepath'])
print("Type in what you would like to send to clients")

flag = True
while flag:
    inputstr = input()

    if(inputstr == 'exit'):
        flag = False
    else:
        with open(config['filepath'],'w') as f:
            f.write(inputstr)
os.remove(config['filepath'])