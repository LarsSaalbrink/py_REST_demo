import { useState } from "react";
import "./App.css";
import { Login } from "./Login";
import { Tasks } from "./Tasks";

export const serverUrl = "http://127.0.0.1:8000";

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const login = (token: string) => {
        sessionStorage.setItem("access_token", token);
        setIsLoggedIn(true);
    };

    const logout = () => {
        sessionStorage.removeItem("access_token");
        setIsLoggedIn(false);
    };

    if (isLoggedIn) {
        return <Tasks />;
    } else {
        return <Login login={login} />;
    }
}

export default App;
