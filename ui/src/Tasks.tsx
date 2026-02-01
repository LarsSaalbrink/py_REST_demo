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
    const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
    const [editValues, setEditValues] = useState<Partial<Task>>({});

    const fetchTasks = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${serverUrl}/tasks`, {
                headers: {
                    Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch tasks");
            }

            const text = await response.text();
            // Handle massive ints as strings
            const safeText = text.replace(/"id":\s*(\d{15,})/g, '"id":"$1"');
            const data = JSON.parse(safeText);

            setTasks(data);
        } catch (err) {
            console.error(err);
            setError("Could not load tasks");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    const handleEdit = (task: Task) => {
        setEditingTaskId(task.id);
        setEditValues({
            ...task,
            is_completed: task.is_completed ?? false,
        });
    };

    const handleCancelEdit = () => {
        setEditingTaskId(null);
        setEditValues({});
    };

    const handleSave = async (taskId: string) => {
        const token = sessionStorage.getItem("access_token");
        if (!token) {
            alert("Session expired");
            props.logout();
            return;
        }

        try {
            const bodyText = JSON.stringify(editValues);
            const body = bodyText.replace(/"id":\s*"(\d+)"/g, '"id":$1'); // Remove "" from ids
            const response = await fetch(`${serverUrl}/tasks/${taskId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: body,
            });

            if (!response.ok) {
                throw new Error("Failed to update task");
            }

            await fetchTasks();
            setEditingTaskId(null);
            setEditValues({});
        } catch (err) {
            console.error(err);
            alert("Could not save task: " + err);
        }
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

            await fetchTasks();
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
                        {tasks.map((task) => {
                            const isEditing = task.id === editingTaskId;
                            return (
                                <tr key={task.id}>
                                    <td>
                                        {isEditing ? (
                                            <input
                                                type="text"
                                                value={editValues.title}
                                                onChange={(e) =>
                                                    setEditValues((prev) => ({
                                                        ...prev,
                                                        title: e.target.value,
                                                    }))
                                                }
                                            />
                                        ) : (
                                            task.title
                                        )}
                                    </td>
                                    <td>
                                        {isEditing ? (
                                            <input
                                                type="text"
                                                value={editValues.description}
                                                onChange={(e) =>
                                                    setEditValues((prev) => ({
                                                        ...prev,
                                                        description:
                                                            e.target.value,
                                                    }))
                                                }
                                            />
                                        ) : (
                                            task.description
                                        )}
                                    </td>
                                    <td>
                                        {isEditing ? (
                                            <input
                                                type="date"
                                                value={
                                                    editValues.due_date?.split(
                                                        "T",
                                                    )[0]
                                                }
                                                onChange={(e) =>
                                                    setEditValues((prev) => ({
                                                        ...prev,
                                                        due_date:
                                                            e.target.value,
                                                    }))
                                                }
                                            />
                                        ) : (
                                            new Date(
                                                task.due_date,
                                            ).toLocaleDateString()
                                        )}
                                    </td>
                                    <td
                                        style={{
                                            textAlign: "center",
                                            cursor: isEditing
                                                ? "pointer"
                                                : "default",
                                            userSelect: "none",
                                        }}
                                    >
                                        {isEditing ? (
                                            <span
                                                onClick={() =>
                                                    setEditValues((prev) => ({
                                                        ...prev,
                                                        is_completed:
                                                            !prev.is_completed,
                                                    }))
                                                }
                                            >
                                                {(editValues.is_completed ??
                                                false)
                                                    ? "✔"
                                                    : "✗"}
                                            </span>
                                        ) : task.is_completed ? (
                                            "✔"
                                        ) : (
                                            "✗"
                                        )}
                                    </td>
                                    <td
                                        style={{
                                            textAlign: "center",
                                            cursor: "pointer",
                                            display: "flex",
                                            flexDirection: "row",
                                        }}
                                    >
                                        {isEditing ? (
                                            <>
                                                <span
                                                    key={`save-${task.id}`}
                                                    style={{
                                                        marginRight: "10px",
                                                    }}
                                                    onClick={() =>
                                                        handleSave(task.id)
                                                    }
                                                >
                                                    💾
                                                </span>
                                                <span
                                                    key={`cancel-${task.id}`}
                                                    onClick={handleCancelEdit}
                                                >
                                                    ✖️
                                                </span>
                                            </>
                                        ) : (
                                            <>
                                                <span
                                                    key={`edit-${task.id}`}
                                                    style={{
                                                        marginRight: "10px",
                                                    }}
                                                    onClick={() =>
                                                        handleEdit(task)
                                                    }
                                                >
                                                    ✏️
                                                </span>
                                                <span
                                                    key={`delete-${task.id}`}
                                                    onClick={() =>
                                                        handleDelete(task.id)
                                                    }
                                                >
                                                    🗑️
                                                </span>
                                            </>
                                        )}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </>
    );
}
