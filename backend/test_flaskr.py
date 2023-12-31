import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format("student", "abc", "127.0.0.1:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions_success(self):
        response = self.client().get('/questions?page=1')
        data_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_json['success'], True)

    def test_create_question_success(self):
        new_question = {
            'question': 'What is the capital of VietNam?',
            'answer': 'Ha Noi',
            'difficulty': 2,
            'category': 3
        }
        response = self.client().post('/questions', json=new_question)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question has been added successfully!')

    def test_create_question_invalid(self):
        invalid_question = {
            'question': 'What is the capital of France?',
            'difficulty': 2,
            'category': 3
        }
        response = self.client().post('/questions', json=invalid_question)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid Request!')
    
    def test_delete_question_seccess(self):
        response = self.client().delete('/questions/6') # Change number 6 to a valid id for this test case to pass
        data_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_json['success'], True)
        self.assertEqual(data_json['message'], 'The question has been successfully deleted!')
    
    def test_delete_question_but_not_found_id(self):
        response = self.client().delete('/questions/5555') # Change number 5555 to a invalid id for this test case to pass
        data_json = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data_json['success'], False)
        self.assertEqual(data_json['message'], 'Page Not found!')

    def test_get_categories_success(self):
        response = self.client().get('/categories')
        data_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_json['success'], True)
    
    def test_get_questions_base_on_category_not_found_id(self):
        response = self.client().get('/categories/200/questions') # Change number 200 to a invalid id for this test case to pass
        data_json = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data_json['success'], False)
        self.assertEqual(data_json['message'], 'Page Not found!')
    
    def test_get_questions_base_on_category_success(self):
        response = self.client().get('/categories/1/questions') # Change number 1 to a valid id for this test case to pass
        data_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_json['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()