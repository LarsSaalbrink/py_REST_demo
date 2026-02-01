import { useState } from "react";
import "./App.css";
import { Login } from "./Login";
import { Tasks } from "./Tasks";
import { CreateAccount } from "./CreateAccount";

export const serverUrl = "http://127.0.0.1:8000";

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isCreatingAccount, setIsCreatingAccount] = useState(false);

    const login = (token: string) => {
        sessionStorage.setItem("access_token", token);
        setIsLoggedIn(true);
        setIsCreatingAccount(false);
    };

    const logout = () => {
        sessionStorage.removeItem("access_token");
        setIsLoggedIn(false);
        setIsCreatingAccount(false);
    };

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            logout();
        }
    });

    if (isLoggedIn) {
        return <Tasks logout={logout} />;
    } else {
        if (isCreatingAccount) {
            return (
                <CreateAccount
                    login={login}
                    back={() => setIsCreatingAccount(false)}
                />
            );
        }
        return (
            <Login
                login={login}
                createAccount={() => setIsCreatingAccount(true)}
            />
        );
    }
}

export default App;
