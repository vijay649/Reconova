// const API_URL =
// "https://YOUR-RENDER-URL.onrender.com";

// async function signup() {

//     const name =
//         document.getElementById("name").value;

//     const email =
//         document.getElementById("email").value;

//     const password =
//         document.getElementById("password").value;

//     const response = await fetch(

//         `${API_URL}/auth/signup`,

//         {
//             method: "POST",

//             headers: {
//                 "Content-Type":
//                 "application/json"
//             },

//             body: JSON.stringify({

//                 name,
//                 email,
//                 password

//             })
//         }
//     );

//     const data = await response.json();

//     document.getElementById(
//         "message"
//     ).innerText = data.message;

//     if (response.ok) {

//         localStorage.setItem(
//             "verify_email",
//             email
//         );

//         window.location.href =
//             "verify-otp.html";
//     }
// }
const signupForm =
document.getElementById("signupForm");

signupForm.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const name =
        document.getElementById("name").value.trim();

        const email =
        document.getElementById("email").value.trim();

        const password =
        document.getElementById("password").value.trim();

        if (!name || !email || !password) {

            alert(
                "All fields are required"
            );

            return;
        }

        try {

            const response =
            await fetch(

                `${API_BASE_URL}/auth/signup`,

                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({

                        name,
                        email,
                        password

                    })
                }
            );

            const data =
            await response.json();

            if (response.ok) {

                alert(
                    data.message
                );

                localStorage.setItem(
                    "email",
                    email
                );

                window.location.href =
                "verify_otp.html";
            }

            else {

                alert(
                    data.detail ||
                    "Signup failed"
                );
            }

        }

        catch (error) {

            console.error(error);

            alert(
                "Cannot connect to backend server"
            );
        }
    }
);