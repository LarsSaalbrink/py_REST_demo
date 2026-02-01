import { useRef, useState } from "react";
import "./App.css";
import { serverUrl } from "./App";

type CreateAccountProps = {
    login: (token: string) => void;
    back: () => void;
};

export function CreateAccount(props: CreateAccountProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const refreshTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(
        null,
    );

    const scheduleRefresh = (user: string, pass: string) => {
        refreshTimeoutRef.current = setTimeout(
            async () => {
                await login(user, pass);
            },
            15 * 60 * 1000,
        );
    };

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

            if (!response.ok) throw new Error("Login failed");

            const data = await response.json();
            props.login(data.access_token);

            if (refreshTimeoutRef.current) {
                clearTimeout(refreshTimeoutRef.current);
            }
            // Eternally log in again every 15 minutes
            // Ideally, server would have API for refreshing tokens,
            // but this demo does not have such an api currently.
            scheduleRefresh(user, pass);
        } catch (err) {
            console.error(err);
            scheduleRefresh(user, pass);
        }
    };

    const handleContinue = async () => {
        try {
            const response = await fetch(serverUrl + "/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const text = await response.text();
                alert("Registration failed: " + text);
                return;
            }

            // Registration succeeded, proceed to login
            await login(username, password);
        } catch (err) {
            console.error(err);
            alert("An error occurred during registration.");
        }
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
                title="Back"
                onClick={props.back}
            >
                ↩
            </div>
            <h1>Create account</h1>
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
