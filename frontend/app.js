const API = "http://127.0.0.1:8009";


// =========================
// 🔐 REGISTER USER
// =========================
async function registerUser() {
    try {
        const username = document.getElementById("registerUsername").value;
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;

        const res = await fetch(`${API}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await res.json();

        document.getElementById("registerResult").innerText =
            data.message || data.detail || "Something went wrong";

    } catch (err) {
        document.getElementById("registerResult").innerText =
            "Error: " + err.message;
    }
}


// =========================
// 🔐 LOGIN USER
// =========================
async function loginUser() {
    try {
        const email = document.getElementById("loginEmail").value;
        const password = document.getElementById("loginPassword").value;

        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (data.token) {
            localStorage.setItem("token", data.token);
            document.getElementById("loginResult").innerText =
                "Login successful ✅";
        } else {
            document.getElementById("loginResult").innerText =
                data.detail || "Login failed";
        }

    } catch (err) {
        document.getElementById("loginResult").innerText =
            "Error: " + err.message;
    }
}


// =========================
// 💬 CHAT (AI AGENT)
// =========================
async function chat() {
    try {
        const msg = document.getElementById("chatMsg").value;
        const token = localStorage.getItem("token");

        const res = await fetch(`${API}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": token ? `Bearer ${token}` : ""
            },
            body: JSON.stringify({
                user_id: 1,
                message: msg
            })
        });

        const data = await res.json();

        document.getElementById("chatResult").innerText =
            data.response || data.detail || "No response";

    } catch (err) {
        document.getElementById("chatResult").innerText =
            "Error: " + err.message;
    }
}


// =========================
// 📦 ORDER TRACKING
// =========================
async function trackOrder() {
    try {
        const orderId = document.getElementById("orderId").value;

        const res = await fetch(`${API}/track-order`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ order_id: orderId })
        });

        const data = await res.json();

        document.getElementById("orderResult").innerText =
            data.response || data.detail || "No response";

    } catch (err) {
        document.getElementById("orderResult").innerText =
            "Error: " + err.message;
    }
}