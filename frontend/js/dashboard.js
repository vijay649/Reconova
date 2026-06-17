// const token =
// localStorage.getItem("token");

// if (!token) {

//     window.location.href =
//     "login.html";
// }

// async function loadDashboard() {

//     try {

//         // =========================
//         // USER PROFILE
//         // =========================

//         const profileResponse =
//         await fetch(

//             `${API_BASE_URL}/dashboard/me`,

//             {
//                 headers: {
//                     Authorization:
//                     `Bearer ${token}`
//                 }
//             }
//         );

//         const profileData =
//         await profileResponse.json();

//         if (!profileResponse.ok) {

//             alert(
//                 profileData.detail ||
//                 "Authentication Failed"
//             );

//             localStorage.clear();

//             window.location.href =
//             "login.html";

//             return;
//         }

//         document.getElementById(
//             "username"
//         ).innerText =
//         `Welcome ${profileData.name}`;

//         document.getElementById(
//             "email"
//         ).innerText =
//         `Email: ${profileData.email}`;

//         document.getElementById(
//             "role"
//         ).innerText =
//         `Role: ${profileData.role}`;

//         // =========================
//         // DASHBOARD SUMMARY
//         // =========================

//         const summaryResponse =
//         await fetch(

//             `${API_BASE_URL}/dashboard/summary`,

//             {
//                 headers: {
//                     Authorization:
//                     `Bearer ${token}`
//                 }
//             }
//         );

//         const summaryData =
//         await summaryResponse.json();

//         if (summaryResponse.ok) {

//             document.getElementById(
//                 "amazonCount"
//             ).innerText =
//             summaryData.amazon || 0;

//             document.getElementById(
//                 "swiggyCount"
//             ).innerText =
//             summaryData.swiggy || 0;

//             document.getElementById(
//                 "zomatoCount"
//             ).innerText =
//             summaryData.zomato || 0;

//             document.getElementById(
//                 "blinkitCount"
//             ).innerText =
//             summaryData.blinkit || 0;

//             document.getElementById(
//                 "flipkartCount"
//             ).innerText =
//             summaryData.flipkart || 0;
//         }
//     }

//     catch (error) {

//         console.error(error);

//         alert(
//             "Unable to connect to server"
//         );
//     }
// }

// function goToParser() {

//     window.location.href =
//     "index.html";
// }

// function logout() {

//     localStorage.removeItem(
//         "token"
//     );

//     localStorage.removeItem(
//         "user"
//     );

//     localStorage.removeItem(
//         "email"
//     );

//     window.location.href =
//     "login.html";
// }

// loadDashboard();


// =====================================
// AUTH CHECK
// =====================================


const token =
localStorage.getItem("token");


const userData =
JSON.parse(
    localStorage.getItem("user")
);



if(!token){

    window.location.href =
    "login.html";

}



// =====================================
// ROLE CHECK
// =====================================


if(
    userData &&
    userData.role === "admin"
){

    window.location.href =
    "admin-dashboard.html";

}





// =====================================
// LOAD DASHBOARD
// =====================================


async function loadDashboard(){


try{


// =====================================
// PROFILE
// =====================================


const profileResponse =
await fetch(

`${API_BASE_URL}/dashboard/me`,

{

headers:{

Authorization:
`Bearer ${token}`

}

}

);



const profileData =
await profileResponse.json();



if(!profileResponse.ok){


localStorage.clear();


window.location.href =
"login.html";


return;


}




// USER INFO


document.getElementById(
"username"
).innerText =
`Welcome ${profileData.name} 👋`;



document.getElementById(
"email"
).innerText =
`Email: ${profileData.email}`;



document.getElementById(
"role"
).innerText =
`Role: ${profileData.role}`;





// =====================================
// SUMMARY ANALYTICS
// =====================================



const summaryResponse =
await fetch(


`${API_BASE_URL}/dashboard/summary`,


{

headers:{

Authorization:
`Bearer ${token}`

}

}

);



const summary =
await summaryResponse.json();





if(summaryResponse.ok){



document.getElementById(
"totalUploads"
).innerText =
summary.total_uploads || 0;



document.getElementById(
"amazonCount"
).innerText =
summary.amazon || 0;



document.getElementById(
"swiggyCount"
).innerText =
summary.swiggy || 0;



document.getElementById(
"zomatoCount"
).innerText =
summary.zomato || 0;



document.getElementById(
"blinkitCount"
).innerText =
summary.blinkit || 0;



document.getElementById(
"flipkartCount"
).innerText =
summary.flipkart || 0;


}





// =====================================
// ACTIVITY LOAD
// =====================================


loadActivity();



}

catch(error){


console.error(
error
);


alert(
"Unable to load dashboard"
);


}



}







// =====================================
// RECENT ACTIVITY
// =====================================


async function loadActivity(){


try{


const response =
await fetch(

`${API_BASE_URL}/dashboard/my-source-analytics`,

{

headers:{

Authorization:
`Bearer ${token}`

}

}

);



const data =
await response.json();



const container =
document.getElementById(
"activityList"
);



if(!container)
return;




container.innerHTML="";



if(data.length===0){


container.innerHTML=
`
<p>
No activity found
</p>
`;


return;


}




data.forEach(item=>{


container.innerHTML +=
`

<div class="activity-item">


<h4>
${item.source.toUpperCase()} Parser
</h4>


<p>
${item.pdf_count} PDF files processed
</p>


</div>

`;



});




}

catch(error){


console.log(
"Activity error",
error
);


}


}






// =====================================
// GO TO PARSER
// =====================================


function goToParser(){


window.location.href =
"index.html";


}





// =====================================
// LOGOUT
// =====================================


function logout(){


localStorage.removeItem(
"token"
);


localStorage.removeItem(
"user"
);


window.location.href =
"login.html";


}






// START

loadDashboard();