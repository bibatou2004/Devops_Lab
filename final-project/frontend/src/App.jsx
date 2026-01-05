import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch statistics
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Create task
  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!newTask.title) return;

    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
      });
      const data = await response.json();
      setTasks([...tasks, data]);
      setNewTask({ title: '', description: '' });
      fetchStats();
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  // Update task
  const handleToggleTask = async (taskId, completed) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !completed })
      });
      const updated = await response.json();
      setTasks(tasks.map(t => t.id === taskId ? updated : t));
      fetchStats();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  // Delete task
  const handleDeleteTask = async (taskId) => {
    try {
      await fetch(`${API_URL}/tasks/${taskId}`, { method: 'DELETE' });
      setTasks(tasks.filter(t => t.id !== taskId));
      fetchStats();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // Load data on mount
  useEffect(() => {
    fetchTasks();
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>📋 DevOps Task Manager</h1>
        <p>CI/CD Data Pipeline on Kubernetes</p>
      </header>

      <main className="app-main">
        {/* Statistics */}
        <section className="stats">
          <div className="stat-card">
            <div className="stat-label">Total Tasks</div>
            <div className="stat-value">{stats.total_tasks || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Completed</div>
            <div className="stat-value">{stats.completed_tasks || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Pending</div>
            <div className="stat-value">{stats.pending_tasks || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Rate</div>
            <div className="stat-value">{Math.round(stats.completion_rate || 0)}%</div>
          </div>
        </section>

        {/* Form */}
        <section className="form-section">
          <form onSubmit={handleCreateTask}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Task title..."
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Description (optional)..."
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              />
              <button type="submit">Add Task</button>
            </div>
          </form>
        </section>

        {/* Tasks List */}
        <section className="tasks-section">
          <h2>Tasks</h2>
          {loading ? (
            <p>Loading...</p>
          ) : tasks.length === 0 ? (
            <p className="no-tasks">No tasks yet. Create one to get started!</p>
          ) : (
            <ul className="tasks-list">
              {tasks.map(task => (
                <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleTask(task.id, task.completed)}
                    />
                    <div className="task-text">
                      <h3>{task.title}</h3>
                      {task.description && <p>{task.description}</p>}
                      <small>{new Date(task.created_at).toLocaleDateString()}</small>
                    </div>
                  </div>
                  <button
                    className="delete-btn"
                    onClick={() => handleDeleteTask(task.id)}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>

      <footer className="app-footer">
        <p>🚀 Built with FastAPI, React, PostgreSQL & Kubernetes</p>
      </footer>
    </div>
  );
}

export default App;
