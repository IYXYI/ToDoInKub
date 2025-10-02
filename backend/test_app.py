import unittest
from unittest.mock import MagicMock
from app import create_app

class TodoApiTestCase(unittest.TestCase):
    def setUp(self):
        # Mock the database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        # Setup default fetchall/fetchone for endpoints
        self.mock_cursor.fetchall.return_value = [(1, 'Test', False)]
        self.mock_cursor.fetchone.side_effect = [[1], [1]]  # For add_todo and get_todo_count
        self.app = create_app(test_conn=self.mock_conn).test_client()

    def test_get_todos(self):
        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_add_todo(self):
        response = self.app.post('/todos', json={'text': 'Test task'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Test task')
        self.assertFalse(data['done'])

    def test_update_todo(self):
        # Add a todo first
        self.mock_cursor.fetchone.side_effect = [[2], [1]]
        add_response = self.app.post('/todos', json={'text': 'To update'})
        todo_id = add_response.get_json()['id']
        # Update the todo
        update_response = self.app.put(f'/todos/{todo_id}', json={'done': True})
        self.assertEqual(update_response.status_code, 200)
        self.assertTrue(update_response.get_json()['done'])

    def test_metrics(self):
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn('todo_count', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
