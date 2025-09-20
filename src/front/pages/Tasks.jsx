import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const TasksPage = () => {

    const [tasks, setTasks] = useState([]);
    const [newTaskTitle, setNewTaskTitle] = useState("");
    const token = localStorage.getItem("token");
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem("user"))

    console.log(user)

    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    useEffect(() => {
        if (!token) {
            alert("Debes iniciar sesión");
            navigate("/");
            return;
        }
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const res = await fetch(backendUrl + "api/get_tasks", {
                headers: { Authorization: "Bearer " + token },
            });
            if (!res.ok) throw new Error("Error al cargar tasks");
            const data = await res.json();
            setTasks(data);
        } catch (err) {
            console.error(err);
        }
    };

    const addTask = async () => {
        if (!newTaskTitle) return;
        try {
            const res = await fetch(backendUrl + "api/add_task", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
                body: JSON.stringify({ title: newTaskTitle }),
            });
            const data = await res.json();
            setTasks(data.tasks);
            setNewTaskTitle("");
        } catch (err) {
            console.error(err);
        }
    };

    const toggleTask = async (id, done) => {
        try {
            const res = await fetch(backendUrl + `api/edit_task/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
                body: JSON.stringify({ done: !done }),
            });
            const data = await res.json();
            setTasks(data.tasks);
        } catch (err) {
            console.error(err);
        }
    };

    const deleteTask = async (id) => {
        try {
            const res = await fetch(backendUrl + `api/delete_task/${id}`, {
                method: "DELETE",
                headers: { Authorization: "Bearer " + token },
            });
            const data = await res.json();
            setTasks(data.tasks);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="text-center mb-4">📋Hola {user.username}, estas son tus tareas:</h2>

            <div className="input-group mb-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Nueva tarea..."
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                />
                <button className="btn btn-primary" onClick={addTask}>
                    Agregar
                </button>
            </div>

            <ul className="list-group">
                {tasks.length === 0 ? (
                    <li className="list-group-item text-muted">No tienes tareas.</li>
                ) : (
                    tasks.map((task) => (
                        <li
                            key={task.id}
                            className="list-group-item d-flex justify-content-between align-items-center"
                        >
                            <div>
                                <input
                                    type="checkbox"
                                    className="form-check-input me-2"
                                    checked={task.done}
                                    onChange={() => toggleTask(task.id, task.done)}
                                />
                                <span className={task.done ? "text-decoration-line-through" : ""}>
                                    {task.title}
                                </span>
                            </div>
                            <button
                                className="btn btn-sm btn-danger"
                                onClick={() => deleteTask(task.id)}
                            >
                                🗑️
                            </button>
                        </li>
                    ))
                )}
            </ul>
        </div>
    );
};
