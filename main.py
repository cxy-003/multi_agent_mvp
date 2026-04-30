from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import sqlite3
import uuid
import time

app = FastAPI()

conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    name TEXT,
    status TEXT,
    result TEXT
)''')
conn.commit()

class TaskCreate(BaseModel):
    name: str

def notify_feishu(msg):
    print(f"[Feishu Webhook Placeholder]: {msg}")

def agent_planner(task_id):
    return {"steps": ["collect_data", "analyze", "generate_report"]}

def agent_executor(step):
    time.sleep(1)
    return f"done_{step}"

def run_task(task_id):
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", ("running", task_id))
    conn.commit()

    plan = agent_planner(task_id)
    results = []

    for step in plan["steps"]:
        res = agent_executor(step)
        results.append(res)

    final = ",".join(results)

    cursor.execute("UPDATE tasks SET status=?, result=? WHERE id=?",
                   ("finished", final, task_id))
    conn.commit()

    notify_feishu(f"Task {task_id} finished")

@app.post("/tasks")
def create_task(task: TaskCreate, bg: BackgroundTasks):
    task_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO tasks VALUES (?,?,?,?)",
                   (task_id, task.name, "pending", ""))
    conn.commit()

    bg.add_task(run_task, task_id)
    return {"task_id": task_id}

@app.get("/tasks")
def list_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    return rows
