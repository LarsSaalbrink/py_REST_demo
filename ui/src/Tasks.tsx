import { useEffect, useState } from "react";
import { serverUrl } from "./App";
import "./Tasks.css";

type Task = {
    id: string;
    title: string;
    description: string;
    due_date: string;
    is_completed: boolean;
};

export function Tasks() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await fetch(serverUrl + "/tasks", {
                    headers: {
                        Authorization: `Bearer ${sessionStorage.getItem(
                            "access_token",
                        )}`,
                    },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch tasks");
                }

                const data = await response.json();
                setTasks(data);
            } catch (err) {
                console.error(err);
                setError("Could not load tasks");
            } finally {
                setLoading(false);
            }
        };

        fetchTasks();
    }, []);

    if (loading) {
        return <h1>Loading tasks…</h1>;
    }

    if (error) {
        return <h1>{error}</h1>;
    }

    return (
        <>
            <h1>Your tasks</h1>
            <div
                style={{
                    backgroundColor: "#908164",
                    padding: "30px",
                    borderRadius: "20px",
                    minWidth: "700px",
                }}
            >
                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse",
                        color: "white",
                        fontSize: "1.2em",
                    }}
                >
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Due date</th>
                            <th>Done</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks.map((task) => (
                            <tr key={task.id}>
                                <td>{task.title}</td>
                                <td>{task.description}</td>
                                <td>
                                    {new Date(
                                        task.due_date,
                                    ).toLocaleDateString()}
                                </td>
                                <td style={{ textAlign: "center" }}>
                                    {task.is_completed ? "✔" : "✗"}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
}
