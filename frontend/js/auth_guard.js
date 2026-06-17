// const token = localStorage.getItem("token");


// if(!token){

//     alert(
//         "Please login first"
//     );

//     window.location.href =
//     "login.html";

// }


// =====================================
// Reconova Authentication Guard
// =====================================


// Get JWT token

const token = localStorage.getItem(
    "token"
);


// Get logged user

const user =
JSON.parse(
    localStorage.getItem("user")
);




// =====================================
// TOKEN CHECK
// =====================================

if(!token || !user){


    localStorage.clear();


    window.location.href =
    "login.html";


}



// =====================================
// OPTIONAL ROLE CHECK
// =====================================


// Current page name

const currentPage =
window.location.pathname
.split("/")
.pop();




// =====================================
// ADMIN PAGE PROTECTION
// =====================================


if(
    currentPage === "admin-dashboard.html"
){


    if(
        user.role !== "admin"
    ){


        alert(
            "Admin access required"
        );


        window.location.href =
        "dashboard.html";


    }

}





// =====================================
// USER PARSER ACCESS
// =====================================


// Parser page allowed for
// both user and admin

if(
    currentPage === "index.html"
){


    if(
        user.role !== "user" &&
        user.role !== "admin"
    ){


        window.location.href =
        "login.html";


    }

}