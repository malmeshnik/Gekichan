import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { useTaskStore } from '../store';
import { Plus, Filter } from 'lucide-react';

const TasksPage = () => {
  const { tasks, setTasks, projects, setProjects, addTask } = useTaskStore();
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [selectedProject, setSelectedProject] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tasksRes, projectsRes] = await Promise.all([
          api.get('/tasks/'),
          api.get('/projects/')
        ]);
        setTasks(tasksRes.data.results || tasksRes.data);
        setProjects(projectsRes.data.results || projectsRes.data);
      } catch (error) {
        console.error('Failed to fetch tasks/projects', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTitle || !selectedProject) return;
    try {
      const response = await api.post('/tasks/', {
        title: newTitle,
        project: selectedProject,
        status: 'todo'
      });
      addTask(response.data);
      setNewTitle('');
      setIsAdding(false);
    } catch (error) {
      alert('Failed to add task');
    }
  };

  const filteredTasks = filter
    ? tasks.filter(t => t.status === filter)
    : tasks;

  if (loading) return <div className="p-4 text-center">Loading tasks...</div>;

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <button
          onClick={() => setIsAdding(!isAdding)}
          className="bg-blue-600 text-white p-2 rounded-full shadow-lg"
        >
          <Plus size={24} />
        </button>
      </div>

      {isAdding && (
        <form onSubmit={handleAddTask} className="mb-6 p-4 bg-white rounded-lg shadow-sm border">
          <input
            type="text"
            placeholder="Task Title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            className="w-full p-2 border rounded mb-3"
            required
          />
          <select
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value)}
            className="w-full p-2 border rounded mb-3"
            required
          >
            <option value="">Select Project</option>
            {projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
          <div className="flex gap-2">
            <button type="submit" className="flex-1 bg-green-600 text-white p-2 rounded">Save</button>
            <button type="button" onClick={() => setIsAdding(false)} className="flex-1 bg-gray-200 p-2 rounded">Cancel</button>
          </div>
        </form>
      )}

      <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
        {['', 'todo', 'in_progress', 'done'].map(status => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-1 rounded-full text-sm capitalize whitespace-nowrap ${
              filter === status ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600'
            }`}
          >
            {status || 'All'}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filteredTasks.length === 0 ? (
          <p className="text-gray-500 text-center py-10">No tasks found.</p>
        ) : (
          filteredTasks.map(task => (
            <div key={task.id} className="p-4 bg-white rounded-lg shadow-sm border flex justify-between items-center">
              <div>
                <h3 className="font-medium">{task.title}</h3>
                <p className="text-xs text-gray-500 uppercase">{task.status.replace('_', ' ')}</p>
              </div>
              <div className={`w-3 h-3 rounded-full ${
                task.status === 'done' ? 'bg-green-500' :
                task.status === 'in_progress' ? 'bg-yellow-500' : 'bg-gray-300'
              }`} />
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TasksPage;
