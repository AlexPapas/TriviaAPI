import json
import unittest

from backend.app.app import create_app
from backend.models import Category, Question, port, setup_db, user
from flask_sqlalchemy import SQLAlchemy


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user = "postgres:alex@localhost"
        self.port = "5432"
        self.database_path = "postgres://{}:{}/{}".format(
            self.user, self.port, self.database_name
        )

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

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_questions"] <= 10)

    # @TODO : FIc test

    def test_delete_question_id(self):
        question = Question(
            question="question_to_be_deleted", answer="answer", difficulty=2, category=2
        )
        question.insert()
        id = question.id
        res = self.client().get("/questions/{}".format(id))
        data = json.loads(res.data)

        check_question_in_db = Question.query.get(id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_id"], id)
        self.assertTrue(check_question_in_db == None)

    def test_add_question(self):
        question = {
            "question": "question_to_be_added",
            "answer": "answer",
            "difficulty": 2,
            "category": 2,
        }

        old_questions = len(Question.query.all())

        res = self.client().post("/add", json=question)
        data = json.loads(res.data)
        new_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(old_questions < new_questions)

    def test_get_questions(self):
        print(self)
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
