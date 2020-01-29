from flask import jsonify
from flask_login import login_required

from app.libs.auth import admin_only
from app.libs.error_code import NotFound, CreateSuccess, Success, DeleteSuccess
from app.libs.red_print import RedPrint
from app.models.problem_set import ProblemSet
from app.validators.problem_set import CreateProblemSetForm, ModifyProblemSetForm

api = RedPrint('problem_set')


@api.route("/<int:id_>", methods=['GET'])
def get_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    fields = problem_set.fields.copy()
    fields.extend(['problem_list', 'detail'])
    problem_set.fields = fields
    return jsonify({
        "code": 0,
        "data": problem_set
    })


@api.route("", methods=['POST'])
@login_required
@admin_only
def create_problem_set_api():
    form = CreateProblemSetForm().validate_for_api().data_
    ProblemSet.create(**form)
    raise CreateSuccess('Problem set has been created')


@api.route("/<int:id_>", methods=['PATCH'])
@login_required
@admin_only
def modify_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    form = ModifyProblemSetForm().validate_for_api().data_
    problem_set.modify(**form)
    raise Success('Problem set has been modified')


@api.route("/<int:id_>", methods=['DELETE'])
@login_required
@admin_only
def delete_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    problem_set.delete()
    raise DeleteSuccess('Problem set has been deleted')
