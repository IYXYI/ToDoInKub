import React, { useEffect, useState } from 'react';

function App() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState('');

  useEffect(() => {
    fetch('/api/todos')
      .then(res => res.json())
      .then(setTodos);
  }, []);

  const addTodo = async () => {
    const res = await fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const todo = await res.json();
    setTodos([...todos, todo]);
    setText('');
  };

  const toggleTodo = async (id, done) => {
    await fetch(`/api/todos/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !done })
    });
    setTodos(todos.map(t => t.id === id ? { ...t, done: !done } : t));
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>Kube TODO</h2>
      <input value={text} onChange={e => setText(e.target.value)} placeholder="Add todo..." />
      <button onClick={addTodo} disabled={!text}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id} style={{ textDecoration: todo.done ? 'line-through' : '' }}>
            <input type="checkbox" checked={todo.done} onChange={() => toggleTodo(todo.id, todo.done)} />
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
