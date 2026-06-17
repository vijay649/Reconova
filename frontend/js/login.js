const loginForm =
document.getElementById("loginForm");


loginForm.addEventListener(
"submit",
async (e)=>{


e.preventDefault();



const email =
document
.getElementById("email")
.value
.trim();



const password =
document
.getElementById("password")
.value
.trim();



if(!email || !password){


alert(
"Email and Password are required"
);


return;


}



try{


const response =
await fetch(

`${API_BASE_URL}/auth/login`,

{

method:"POST",


headers:{


"Content-Type":
"application/json"

},


body:JSON.stringify({

email,

password

})

}

);



const data =
await response.json();




if(response.ok){



localStorage.clear();



localStorage.setItem(

"token",

data.access_token

);



localStorage.setItem(

"user",

JSON.stringify(
data.user
)

);




console.log(
"LOGIN USER:",
data.user
);



alert(
"Login Successful"
);





const role =
data.user.role.toLowerCase();





// =============================
// VERCEL ROUTES
// =============================


if(role === "admin"){


window.location.href =
"/admin-dashboard";


}


else{


window.location.href =
"/dashboard";


}



}




else{


alert(

data.detail ||

"Login failed"

);


}



}



catch(error){


console.error(

"LOGIN ERROR:",

error

);


alert(

"Cannot connect to backend server"

);


}



});