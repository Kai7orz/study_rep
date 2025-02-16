let count = 1; 

function userRead(){
  return new Promise((resolve)=>{
    const readInterface = require('readline').createInterface({
      input:process.stdin,
      output:process.stdout
    });

   
   if(count %3 == 1)
    {
      readInterface.question("入力:method ",(inputString)=>{
      readInterface.close();
      resolve(inputString);
      count +=1
    });
  }

  if(count %3 == 2)
    { 
      readInterface.question("入力:param ",(inputString)=>{
      readInterface.close();
      resolve(inputString);
      count +=1
    });
  }

  if(count %3 == 0)
    { 
      readInterface.question("入力:param_types ",(inputString)=>{
      readInterface.close();
      resolve(inputString);
      count +=1
    });
  }
 
  });

}

async function userInput(){
  let words = "";
    method = await userRead(); 
    params = await userRead(); 
    params_type = await userRead(); 
    

    const message = JSON.stringify({
      "method": method,
      "params": params,
      "param_types": params_type,
      "id": 1
  });

    return message 
}


async function main(){
 
  const client = require('net').createConnection('/tmp/server_address');
  m = await userInput()
  

  client.write(m, () => {
    console.log("送信完了");
});


  client.on('data', data => {
    console.log('Received: ' + data)
    client.end(); 
    });


}
main();


//await　はPromise がresolveになるまで待つ仕様だから,await つけた関数はPromise化しておく必要がある