// Local Backend
const LOCAL_API =
"http://127.0.0.1:8000";


// Production Backend (Render)
const PROD_API =
"https://reconova-983m.onrender.com";


// Automatically select API

const API_BASE_URL =
window.location.hostname === "localhost" ||
window.location.hostname === "127.0.0.1"

? LOCAL_API

: PROD_API;