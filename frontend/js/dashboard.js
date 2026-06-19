
// const token =
// localStorage.getItem("token");


// const userData =
// JSON.parse(
//     localStorage.getItem("user")
// );



// if(!token){

//     window.location.href =
//     "login.html";

// }



// // =====================================
// // ROLE CHECK
// // =====================================


// if(
//     userData &&
//     userData.role === "admin"
// ){

//     window.location.href =
//     "admin-dashboard.html";

// }





// // =====================================
// // LOAD DASHBOARD
// // =====================================


// async function loadDashboard(){


// try{


// // =====================================
// // PROFILE
// // =====================================


// const profileResponse =
// await fetch(

// `${API_BASE_URL}/dashboard/me`,

// {

// headers:{

// Authorization:
// `Bearer ${token}`

// }

// }

// );



// const profileData =
// await profileResponse.json();



// if(!profileResponse.ok){


// localStorage.clear();


// window.location.href =
// "login.html";


// return;


// }




// // USER INFO


// document.getElementById(
// "username"
// ).innerText =
// `Welcome ${profileData.name} 👋`;



// document.getElementById(
// "email"
// ).innerText =
// `Email: ${profileData.email}`;



// document.getElementById(
// "role"
// ).innerText =
// `Role: ${profileData.role}`;





// // =====================================
// // SUMMARY ANALYTICS
// // =====================================



// const summaryResponse =
// await fetch(


// `${API_BASE_URL}/dashboard/summary`,


// {

// headers:{

// Authorization:
// `Bearer ${token}`

// }

// }

// );



// const summary =
// await summaryResponse.json();





// if(summaryResponse.ok){



// document.getElementById(
// "totalUploads"
// ).innerText =
// summary.total_uploads || 0;



// document.getElementById(
// "amazonCount"
// ).innerText =
// summary.amazon || 0;



// document.getElementById(
// "swiggyCount"
// ).innerText =
// summary.swiggy || 0;



// document.getElementById(
// "zomatoCount"
// ).innerText =
// summary.zomato || 0;



// document.getElementById(
// "blinkitCount"
// ).innerText =
// summary.blinkit || 0;



// document.getElementById(
// "flipkartCount"
// ).innerText =
// summary.flipkart || 0;


// }





// // =====================================
// // ACTIVITY LOAD
// // =====================================


// loadActivity();



// }

// catch(error){


// console.error(
// error
// );


// alert(
// "Unable to load dashboard"
// );


// }



// }







// // =====================================
// // RECENT ACTIVITY
// // =====================================


// async function loadActivity(){


// try{


// const response =
// await fetch(

// `${API_BASE_URL}/dashboard/my-source-analytics`,

// {

// headers:{

// Authorization:
// `Bearer ${token}`

// }

// }

// );



// const data =
// await response.json();



// const container =
// document.getElementById(
// "activityList"
// );



// if(!container)
// return;




// container.innerHTML="";



// if(data.length===0){


// container.innerHTML=
// `
// <p>
// No activity found
// </p>
// `;


// return;


// }




// data.forEach(item=>{


// container.innerHTML +=
// `

// <div class="activity-item">


// <h4>
// ${item.source.toUpperCase()} Parser
// </h4>


// <p>
// ${item.pdf_count} PDF files processed
// </p>


// </div>

// `;



// });




// }

// catch(error){


// console.log(
// "Activity error",
// error
// );


// }


// }






// // =====================================
// // GO TO PARSER
// // =====================================


// function goToParser(){


// window.location.href =
// "index.html";


// }





// // =====================================
// // LOGOUT
// // =====================================


// function logout(){


// localStorage.removeItem(
// "token"
// );


// localStorage.removeItem(
// "user"
// );


// window.location.href =
// "login.html";


// }






// // START

// loadDashboard();




const token = localStorage.getItem("token");
const userData = JSON.parse(localStorage.getItem("user"));

// =====================================
// AUTH GUARD & VERCEL ROUTING FIX
// =====================================
if (!token) {
    // .html hataya taaki vercel rewrite works perfectly
    window.location.href = "/login"; 
}

// =====================================
// ROLE CHECK
// =====================================
if (userData && userData.role === "admin") {
    window.location.href = "/admin-dashboard";
}

// =====================================
// LOAD DASHBOARD
// =====================================
async function loadDashboard() {
    try {
        // =====================================
        // PROFILE
        // =====================================
        const profileResponse = await fetch(`${API_BASE_URL}/dashboard/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!profileResponse.ok) {
            localStorage.clear();
            window.location.href = "/login";
            return;
        }

        const profileData = await profileResponse.json();

        // USER INFO
        document.getElementById("username").innerText = `Welcome ${profileData.name} 👋`;
        document.getElementById("email").innerText = `Email: ${profileData.email}`;
        document.getElementById("role").innerText = `Role: ${profileData.role}`;

        // =====================================
        // SUMMARY ANALYTICS
        // =====================================
        const summaryResponse = await fetch(`${API_BASE_URL}/dashboard/summary`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (summaryResponse.ok) {
            const summary = await summaryResponse.json();

            document.getElementById("totalUploads").innerText = summary.total_uploads || 0;
            document.getElementById("amazonCount").innerText = summary.amazon || 0;
            document.getElementById("swiggyCount").innerText = summary.swiggy || 0;
            document.getElementById("zomatoCount").innerText = summary.zomato || 0;
            document.getElementById("blinkitCount").innerText = summary.blinkit || 0;
            document.getElementById("flipkartCount").innerText = summary.flipkart || 0;
        }

        // =====================================
        // ACTIVITY LOAD
        // =====================================
        loadActivity();

    } catch (error) {
        console.error(error);
        alert("Unable to load dashboard");
    }
}

// =====================================
// RECENT ACTIVITY
// =====================================
async function loadActivity() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/my-source-analytics`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await response.json();
        const container = document.getElementById("activityList");

        if (!container) return;

        container.innerHTML = "";

        if (data.length === 0) {
            container.innerHTML = `<p>No activity found</p>`;
            return;
        }

        data.forEach(item => {
            container.innerHTML += `
                <div class="activity-item">
                    <h4>${item.source.toUpperCase()} Parser</h4>
                    <p>${item.pdf_count} PDF files processed</p>
                </div>
            `;
        });

    } catch (error) {
        console.log("Activity error", error);
    }
}

// =====================================
// GO TO PARSER (FIXED 404 ERROR)
// =====================================
function goToParser() {
    // Jab user dashboard par parser button click karega, yeh use direct /index par bhejega
    window.location.href = "/index";
}

// =====================================
// LOGOUT
// =====================================
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
}

// START
loadDashboard();