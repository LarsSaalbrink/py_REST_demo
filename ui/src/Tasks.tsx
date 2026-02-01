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

type TasksProps = {
    logout: () => void;
};

export function Tasks(props: TasksProps) {
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

                const text = await response.text();
                // Convert huge numbers to strings
                const safeText = text.replace(
                    /"id":\s*(\d{15,})/g,
                    '"id":"$1"',
                );
                const data = JSON.parse(safeText);

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

    const handleEdit = (taskId: string) => {
        console.log("Edit task", taskId);
        // TODO
    };

    const handleDelete = async (taskId: string) => {
        const token = sessionStorage.getItem("access_token");

        if (!token) {
            alert("Session expired");
            props.logout();
            return;
        }

        try {
            const response = await fetch(`${serverUrl}/tasks/${taskId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error("Failed to delete task");
            }

            // Remove task from UI
            setTasks((prevTasks) =>
                prevTasks.filter((task) => task.id !== taskId),
            );
        } catch (err) {
            console.error(err);
            alert("Could not delete task: " + err);
        }
    };

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
                            <th />
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
                                <td
                                    style={{
                                        textAlign: "center",
                                        cursor: "pointer",
                                        display: "flex",
                                        flexDirection: "row",
                                    }}
                                >
                                    <span
                                        style={{ marginRight: "10px" }}
                                        onClick={() => handleEdit(task.id)}
                                    >
                                        ✏️
                                    </span>
                                    <span onClick={() => handleDelete(task.id)}>
                                        🗑️
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
}
