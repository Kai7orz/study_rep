const net = require('net');

const client = new net.Socket();
const message = JSON.stringify({
    "method": "floor",
    "params": 1.4,
    "param_types": "float",
    "id": 1
});

const message2 = JSON.stringify({
    "method": "nroot",
    "params": [2,81],
    "param_types": "float",
    "id": 1
});

const message3 = JSON.stringify({
    "method": "reverse",
    "params": "thisistest",
    "param_types": "string",
    "id": 1
});

const message4 = JSON.stringify({
    "method": "validAnagram",
    "params": ["thisistest","testthisis"],
    "param_types": "string",
    "id": 1
});

const message5 = JSON.stringify({
    "method": "sort",
    "params": ["thisistest","mytest","hello"],
    "param_types": ["string","string","string"],
    "id": 1
});

client.connect(8000,'localhost',()=>{
    client.write(message3);
});

client.on('data', data => {
    console.log('Received: ' + data)
        console.log("continue")
    
});

client.on("close",function(){
    
    console.log("closed");
})