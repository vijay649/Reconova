// =====================================
// Reconova Authentication Guard
// =====================================


const token = localStorage.getItem("token");


const user =
JSON.parse(
    localStorage.getItem("user")
);




// =====================================
// LOGIN CHECK
// =====================================


if(!token || !user){


    localStorage.clear();


    window.location.href="/login";


}




// =====================================
// CURRENT ROUTE
// =====================================


const path =
window.location.pathname;



// =====================================
// ADMIN PROTECTION
// =====================================


if(
    path.includes("/admin")
){


    if(
        user.role !== "admin"
    ){


        alert(
            "Admin access required"
        );


        window.location.href="/dashboard";


    }


}





// =====================================
// PARSER PROTECTION
// =====================================


if(
    path.includes("/index.html") ||
    path === "/"
){


    if(
        user.role !== "user" &&
        user.role !== "admin"
    ){


        window.location.href="/login";


    }


}