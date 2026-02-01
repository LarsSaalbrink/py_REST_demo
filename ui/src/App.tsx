import "./App.css";

function App() {
    return (
        <>
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
                    />
                    <input
                        className="loginInput"
                        type="password"
                        placeholder="Password"
                    />
                </div>
                <button
                    className="loginButton"
                    onClick={() => setCount((count) => count + 1)}
                >
                    Continue
                </button>
            </div>
        </>
    );
}

export default App;
