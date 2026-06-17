const verifyForm =
document.getElementById("verifyForm");

verifyForm.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const email =
        localStorage.getItem("email");

        if (!email) {

            alert(
                "Please signup first"
            );

            window.location.href =
            "signup.html";

            return;
        }

        const otp =
        document.getElementById("otp").value;

        try {

            const response =
            await fetch(

                `${API_BASE_URL}/auth/verify-otp`,

                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({

                        email,
                        otp

                    })
                }
            );

            const data =
            await response.json();

            if (response.ok) {

                alert(
                    data.message
                );

                localStorage.removeItem(
                    "email"
                );

                window.location.href =
                "login.html";
            }

            else {

                alert(
                    data.detail ||
                    "OTP verification failed"
                );
            }

        } catch (error) {

            console.error(error);

            alert(
                "Server connection failed"
            );
        }
    }
);