from flask import jsonify
from flask_login import login_required

from app.libs.auth import admin_only
from app.libs.error_code import CreateSuccess, DeleteSuccess, NotFound
from app.libs.red_print import RedPrint
from app.models.competition import Competition
from app.validators.competition import (BaseSearchCompetitionForm,
                                        CreateCompetitionForm,
                                        ModifyCompetitionForm)

api = RedPrint('competition')


@api.route('/', methods=['GET'])
def get_competition_api():
    form = BaseSearchCompetitionForm().validate_for_api().data_
    competition_list = Competition.search_from_now(**form)
    return jsonify({
        'code': 0,
        'data': competition_list
    })


@api.route('/', methods=['POST'])
@login_required
@admin_only
def create_competition_api():
    form = CreateCompetitionForm().validate_for_api().data_
    Competition.create(**form)
    raise CreateSuccess('Competition has been created')


@api.route('/<int:id_>', methods=['PUT'])
@login_required
@admin_only
def modify_competition_api(id_):
    competition = Competition.get_by_id(id_)
    if competition is None:
        raise NotFound('Competition not found')

    form = ModifyCompetitionForm().validate_for_api().data_
    competition.modify(**form)
    raise CreateSuccess('Competition has been modified')


@api.route('/<int:id_>', methods=['DELETE'])
@login_required
@admin_only
def delete_competition_api(id_):
    competition = Competition.get_by_id(id_)
    if competition is None:
        raise NotFound('Competition not found')

    competition.delete()
    raise DeleteSuccess('Competition has been deleted')
