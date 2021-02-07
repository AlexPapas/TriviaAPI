from backend.models import Category, Question, db, setup_db
from flask import Flask, abort, flash, json, jsonify, request
from flask_cors import CORS
from flask_cors.core import parse_resources
from flask_sqlalchemy import SQLAlchemy

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selections):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # jsonfy the SQL alchemy output
    questions = [question.format() for question in selections]
    current_questions = questions[start:end]
    print(current_questions)
    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    # """
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        categories = db.session.query(Category).all()
        categories_dict = [cat.format() for cat in categories]

        if len(categories) == 0:
            abort(404)

        return jsonify({"success": True, "categories": categories_dict})

    #   """
    #   @TODO- Done:
    #   Create an endpoint to handle GET requests for questions,
    #  including pagination (every 10 questions).
    #  This endpoint should return a list of questions,
    #  number of total questions, current category, categories.
    @app.route("/questions")
    def get_paginated_questions():
        # selection = Question.query.order_by(Question.id).all()
        selection = Question.query.all()
        questions = paginate_questions(request, selection)

        categories = db.session.query(Category).all()
        # categories = Category.query.all()
        categories_dict = {cat.id: cat.type for cat in categories}

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories_dict,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": None,
            }
        )

    #   """
    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    @app.route("/questions/<int:id>", methods=["GET", "DELETE"])
    def delete_question(id):
        # might page be out of index
        try:
            question = Question.query.get(id)
        except:
            abort(404)
        question.delete()

        return jsonify({"success": True, "deleted_id": id})

    #   """
    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # """

    @app.route("/add", methods=["POST"])
    def add_question():

        body = request.get_json()
        if not all([len(str(value)) > 0 for value in body.values()]):
            abort(422)

        question = Question(
            question=body.get("question"),
            answer=body["answer"],
            category=body["category"],
            difficulty=body["difficulty"],
        )
        try:
            question.insert()
            questions = Question.query.all()
            print("question was added")
            current_questions = paginate_questions(request, questions)

            print(len(questions))
            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                }
            )
        except:
            abort(404)

        #   """

    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    #   """

    # -- Error Handling --
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app


#     """
#   @TODO:
#   Create a GET endpoint to get questions based on category.

#   TEST: In the "List" tab / main screen, clicking on one of the
#   categories in the left column will cause only questions of that
#   category to be shown.
#   """

#     """
#   @TODO:
#   Create a POST endpoint to get questions to play the quiz.
#   This endpoint should take category and previous question parameters
#   and return a random questions within the given category,
#   if provided, and that is not one of the previous questions.

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not.
#   """

#   """
#   @TODO:
#   Create error handlers for all expected errors
#   including 404 and 422.
#   """

# API-digestible error handlers
# These override the default HTML response when we call abort
###############################
