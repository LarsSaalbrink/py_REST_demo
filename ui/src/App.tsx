import { useRef, useState } from "react";
import "./App.css";

const serverUrl = "http://127.0.0.1:8000";

function App() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    // Keep reference to the refresh timer
    const refreshTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    const login = async (user: string, pass: string) => {
        try {
            const body = new URLSearchParams({
                username: user,
                password: pass,
            });

            const response = await fetch(serverUrl + "/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body,
            });
            if (!response.ok) {
                // TODO: Visualise this
                throw new Error("Login failed");
            }

            const data = await response.json();
            sessionStorage.setItem("access_token", data.access_token);

            // Queue token refresh after 15 minutes
            if (refreshTimeoutRef.current) {
                clearTimeout(refreshTimeoutRef.current);
            }
            refreshTimeoutRef.current = setTimeout(
                () => {
                    login(user, pass);
                },
                15 * 60 * 1000,
            );
        } catch (err) {
            console.error(err);
        }
    };

    const handleContinue = () => {
        login(username, password);
    };

    return (
        <>
            <div
                style={{
                    position: "absolute",
                    top: "20px",
                    right: "20px",
                    width: "80px",
                    height: "80px",
                    borderRadius: "40px",
                    backgroundColor: "#908164",
                    fontSize: "50px",
                    textAlign: "center",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    cursor: "pointer",
                }}
                title="Create free account"
            >
                ✚
            </div>
            <h1>Sign in</h1>
            <div className="card">
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "50px",
                        padding: "40px",
                        backgroundColor: "#908164",
                        borderRadius: "20px",
                    }}
                >
                    <input
                        className="loginInput"
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        className="loginInput"
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <button className="loginButton" onClick={handleContinue}>
                    Continue
                </button>
            </div>
        </>
    );
}

export default App;
