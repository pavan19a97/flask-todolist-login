
console.log("hi i am their");


function sendPostRequest(inite, kd){
    console.log(inite, kd);
    editText = document.getElementById("{{ task.id }}").value;
    console.log(editText);
    let xhr = new XMLHttpRequest(); 
    let url = "/update/{{ task.id }}"; 

    // open a connection 
    xhr.open("POST", url, true); 

    // Set the request header i.e. which type of content you are sending 
    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 

            // Print received data from server 
            result.innerHTML = this.responseText; 

        } 
    }; 

    // Converting JSON data to string 
    var data = JSON.stringify({ "updatedTask": editText }); 

    // Sending data with the request 
    xhr.send(data); 
    console.log("hello there from function")
}


