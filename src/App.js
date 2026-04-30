import React, { useState, useEffect } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [name, setName] = useState("");

  const fetchTasks = async () => {
    const res = await fetch("http://localhost:8000/tasks");
    const data = await res.json();
    setTasks(data);
  };

  const createTask = async () => {
    await fetch("http://localhost:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    });
    setName("");
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Multi-Agent Automation Console</h1>

      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Task name"
      />
      <button onClick={createTask}>Create Task</button>

      <ul>
        {tasks.map(t => (
          <li key={t[0]}>
            {t[1]} - {t[2]} - {t[3]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
