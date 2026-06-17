// -------------------------------------------------------------------------------------------------------


const token = localStorage.getItem("token");

if (!token || token.trim() === "") {
    window.location.href = "login.html";
}

let users = [];
let deleteId = null;

// Helper function to extract numbers from any dynamic API response object
function extractCount(responseObj, defaultKey) {
    if (responseObj === null || responseObj === undefined) return 0;
    
    if (typeof responseObj === "number") return responseObj;
    if (typeof responseObj === "string" && !isNaN(responseObj)) return parseInt(responseObj);

    if (typeof responseObj === "object") {
        if (responseObj[defaultKey] !== undefined) return responseObj[defaultKey];
        if (responseObj.count !== undefined) return responseObj.count;
        if (responseObj.total !== undefined) return responseObj.total;
        if (responseObj.data !== undefined) {
            if (typeof responseObj.data === "number") return responseObj.data;
            if (Array.isArray(responseObj.data)) return responseObj.data.length;
        }

        for (let key in responseObj) {
            if (typeof responseObj[key] === "number") return responseObj[key];
            if (typeof responseObj[key] === "string" && !isNaN(responseObj[key])) return parseInt(responseObj[key]);
        }
    }
    return 0;
}

// API Fetch Function (CLEANED & REMOVED SENSITIVE LOGS)
async function api(url) {
    try {
        const response = await fetch(API_BASE_URL + url, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.warn(`Unauthorized access (401) on ${url}. Redirecting...`);
                logout();
            }
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        // Removed sensitive user payload console.log from here to protect data leak in F12!
        return data;
    } catch (err) {
        console.error(`❌ Fetch failed for ${url}:`, err);
        return null;
    }
}

// Safe Individual Loading
async function loadDashboard() {
    console.log("🔄 Loading Dashboard Data...");

    // 1. Load Total Users
    const totalData = await api("/admin/total-users");
    document.getElementById("totalUsers").innerText = extractCount(totalData, "total_users");

    // 2. Load Verified Users
    const verifiedData = await api("/admin/verified-users");
    document.getElementById("verifiedUsers").innerText = extractCount(verifiedData, "verified_users");

    // 3. Load Total Uploads
    const uploadsData = await api("/admin/total-uploads");
    document.getElementById("totalUploads").innerText = extractCount(uploadsData, "total_uploads");

    // 4. Load Users List
    const userList = await api("/admin/users");
    if (userList) {
        if (Array.isArray(userList)) {
            users = userList;
        } else if (userList.users && Array.isArray(userList.users)) {
            users = userList.users;
        } else if (userList.data && Array.isArray(userList.data)) {
            users = userList.data;
        } else {
            users = [];
        }
        renderUsers(users);
    }

    // 5. Load Analytics & Charts Safely
    const analytics = await api("/admin/parser-analytics");
    if (analytics && Array.isArray(analytics)) {
        loadCharts(analytics);
    } else if (analytics && analytics.data && Array.isArray(analytics.data)) {
        loadCharts(analytics.data);
    } else {
        loadCharts([{ parser: "No Data", total_files: 1 }]);
    }
}

function renderUsers(data) {
    const tableBody = document.getElementById("userTable");
    if (!tableBody) return;
    
    if (!data || data.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 30px;">No users found in database.</td></tr>`;
        return;
    }

    let html = "";
    data.forEach(user => {
        const totalUploads = user.total_uploads ?? user.uploads ?? 0;
        const userId = user.id ?? user._id ?? "N/A";
        const userName = user.name ?? user.username ?? "Unknown";
        const userEmail = user.email ?? "No Email";
        const userRole = user.role ?? "user";

        html += `
            <tr>
                <td>${userId}</td>
                <td>${userName}</td>
                <td>${userEmail}</td>
                <td><span class="role-badge">${userRole}</span></td>
                <td>${totalUploads}</td>
                <td>
                    <button class="delete-btn" onclick="openDelete(${userId})">Delete</button>
                </td>
            </tr>
        `;
    });
    tableBody.innerHTML = html;
}

function searchUsers() {
    const searchValue = document.getElementById("search").value.toLowerCase().trim();
    const filteredUsers = users.filter(user => {
        const name = (user.name ?? "").toLowerCase();
        const email = (user.email ?? "").toLowerCase();
        return name.includes(searchValue) || email.includes(searchValue);
    });
    renderUsers(filteredUsers);
}

function loadCharts(analyticsData) {
    const textPrimary = getComputedStyle(document.body).getPropertyValue('--text-primary') || '#1e293b';
    const accentBlue = getComputedStyle(document.body).getPropertyValue('--accent-blue') || '#2563eb';

    const chart1 = document.getElementById("parserChart");
    if(chart1) {
        Chart.getChart(chart1)?.destroy();
        new Chart(chart1, {
            type: "doughnut",
            data: {
                labels: analyticsData.map(x => x.parser ?? x.name ?? "Unknown"),
                datasets: [{
                    data: analyticsData.map(x => x.total_files ?? x.count ?? x.value ?? 0),
                    backgroundColor: [accentBlue, '#16a34a', '#dc2626', '#facc15', '#a855f7'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: textPrimary } } }
            }
        });
    }

    const chart2 = document.getElementById("uploadChart");
    if(chart2) {
        Chart.getChart(chart2)?.destroy();
        new Chart(chart2, {
            type: "line",
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Uploads',
                    data: [120, 150, 140, 200, 180, 100, 90],
                    borderColor: accentBlue,
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { display: false }, x: { ticks: { color: textPrimary } } }
            }
        });
    }
}

// Tab Switching Navigation
document.querySelectorAll('.sidebar nav a').forEach(tab => {
    tab.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelectorAll('.sidebar nav a').forEach(a => a.classList.remove('active'));
        this.classList.add('active');

        const targetText = this.textContent.trim();
        const cardsSection = document.querySelector('.cards');
        const chartsSection = document.querySelector('.charts');
        const usersSection = document.querySelector('.users');

        if (targetText.includes("Dashboard")) {
            cardsSection.style.display = "grid";
            chartsSection.style.display = "grid";
            usersSection.style.display = "block";
        } else if (targetText.includes("Manage Users")) {
            cardsSection.style.display = "none";
            chartsSection.style.display = "none";
            usersSection.style.display = "block";
        } else if (targetText.includes("Parser Analytics")) {
            cardsSection.style.display = "none";
            chartsSection.style.display = "grid";
            usersSection.style.display = "none";
        }
    });
});

function exportCSV() {
    let csv = "ID,Full Name,Email Address,Role,Total Uploads\n";
    users.forEach(u => {
        csv += `${u.id ?? ""},"${u.name ?? ""}","${u.email ?? ""}",${u.role ?? ""},${u.total_uploads ?? 0}\n`;
    });
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `users-export.csv`;
    a.click();
}

function openDelete(id) {
    deleteId = id;
    document.getElementById("deleteModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("deleteModal").style.display = "none";
}

document.getElementById("confirmDelete").onclick = async () => {
    try {
        await fetch(API_BASE_URL + "/admin/delete-user/" + deleteId, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` }
        });
        closeModal();
        loadDashboard();
    } catch (err) {
        console.error("Error deleting user:", err);
    }
};

function toggleDarkMode() {
    const body = document.body;
    if (body.classList.contains("light-mode")) {
        body.classList.replace("light-mode", "dark-mode");
        localStorage.setItem("theme", "dark-mode");
    } else {
        body.classList.replace("dark-mode", "light-mode");
        localStorage.setItem("theme", "light-mode");
    }
    loadDashboard();
}

const savedTheme = localStorage.getItem("theme") || "light-mode";
document.body.className = savedTheme;

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// Initial Call
loadDashboard();

