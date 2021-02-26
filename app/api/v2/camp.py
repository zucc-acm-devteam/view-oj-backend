from flask import jsonify
from flask_login import current_user, login_required
from sqlalchemy import func

from app.libs.auth import admin_only
from app.libs.error_code import AuthFailed, CreateSuccess, NotFound, Success
from app.libs.red_print import RedPrint
from app.libs.spider_service import submit_crawl_course_info_task
from app.models.base import db
from app.models.camp_models.camp import Camp
from app.models.camp_models.camp_accept_problem import CampAcceptProblem
from app.models.camp_models.camp_oj import CampOJ
from app.models.camp_models.camp_problem import CampProblem
from app.models.camp_models.course import Course
from app.models.camp_models.course_contest import CourseContest
from app.models.camp_models.course_oj_username import CourseOJUsername
from app.models.camp_models.user_contest import UserContest
from app.models.user import User
from app.validators.camp import (AppendContestForm, CreateCampForm,
                                 CreateCourseForm, ModifyCampNameForm,
                                 ModifyCourseForm, ModifyCourseUsernameForm)

api = RedPrint('camp')


@api.route('/valid_oj', methods=['GET'])
def valid_oj_api():
    oj_list = CampOJ.search(status=1, page_size=-1)['data']
    return jsonify({
        'code': 0,
        'data': oj_list
    })


@api.route('/summary', methods=['GET'])
def summary_api():
    camps = Camp.search(page_size=-1, order={'id': 'desc'})['data']
    return jsonify({
        'code': 0,
        'data': [{
            'id': i.id,
            'name': i.name,
            'courses': i.courses
        } for i in camps]
    })


@api.route('/<int:id_>/rating', methods=['GET'])
def get_camp_rating(id_):
    camp = Camp.get_by_id(id_)
    if camp is None:
        raise NotFound('Camp not found')
    res = []
    data = db.session. \
        query(User, func.sum(UserContest.rating)). \
        filter(User.username == UserContest.username, CourseContest.course_id == Course.id,
               UserContest.contest_id == CourseContest.id). \
        filter(User.status == 1, Course.camp_id == id_). \
        group_by(User.username).all()
    for item in data:
        user = item[0]
        res.append({
            'user': user,
            'rating': round(item[1], 3)
        })
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route('', methods=['POST'])
@login_required
@admin_only
def create_camp_api():
    form = CreateCampForm().validate_for_api().data_
    Camp.create(**form)
    raise CreateSuccess('Course set has been created')


@api.route('/modify_camp_name/<int:id_>', methods=['POST'])
@login_required
@admin_only
def modify_camp_name_api(id_):
    camp = Camp.get_by_id(id_)
    if camp is None:
        raise NotFound('Course set not found')
    form = ModifyCampNameForm().validate_for_api().data_
    camp.mofify(**form)
    raise Success('Course set has been modified')


@api.route('/course/<int:id_>', methods=['GET'])
def course_detail_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    return jsonify({
        'code': 0,
        'data': course
    })


@api.route('/course/<int:id_>', methods=['POST'])
@login_required
@admin_only
def create_course(id_):
    camp = Camp.get_by_id(id_)
    if camp is None:
        raise NotFound('Course set not found')
    form = CreateCourseForm().validate_for_api().data_
    Course.create(camp_id=camp.id, **form)
    raise Success('Course has been created')


@api.route('/course/<int:id_>', methods=['PUT'])
@login_required
@admin_only
def modify_course_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    form = ModifyCourseForm().validate_for_api().data_
    course.modify(**form)
    raise Success('Course has been modified')


@api.route('/course/<int:id_>/append_contest', methods=['POST'])
@login_required
@admin_only
def append_contest_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    form = AppendContestForm().validate_for_api().data_
    course.append_contest(**form)
    raise Success('Contest appended')


@api.route('/course/<int:id_>/rating', methods=['GET'])
def get_course_rating_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    data = db.session. \
        query(CourseOJUsername.oj_username, func.sum(UserContest.rating)). \
        filter(CourseOJUsername.course_id == id_, CourseOJUsername.username == UserContest.username). \
        filter(CourseContest.course_id == id_, UserContest.contest_id == CourseContest.id). \
        group_by(CourseOJUsername.oj_username).all()
    temp = {}
    for item in data:
        temp.setdefault(item[0], {
            'rating': item[1],
            'members': []
        })
    data = db.session.query(CourseOJUsername.oj_username, CourseOJUsername.username, User.nickname). \
        filter(CourseOJUsername.username == User.username). \
        filter(CourseOJUsername.course_id == id_).all()
    for item in data:
        temp.setdefault(item[0], {
            'rating': 0,
            'members': []
        })
        temp[item[0]]['members'].append({
            'username': item[1],
            'nickname': item[2]
        })
    for item in temp.keys():
        rating = temp[item]['rating'] / len(temp[item]['members'])
        temp[item]['rating'] = round(rating, 3)
    res = []
    for name, info in temp.items():
        res.append({
            'team_name': name if len(info['members']) > 1 else info['members'][0]['nickname'],
            'members': info['members'],
            'rating': info['rating']
        })
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route('/course/<int:id_>/oj_username', methods=['GET'])
@login_required
def get_course_username_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    oj = CampOJ.get_by_id(course.camp_oj_id)
    if current_user.permission != 1:
        data = CourseOJUsername.get_by_username_and_course_id(
            current_user.username,
            id_
        )
        if data is None:
            data = [{
                'username': current_user.username,
                'nickname': current_user.nickname,
                'oj': oj,
                'oj_username': None,
                'last_success_time': None
            }]
        else:
            data = [data]
    else:
        data = []
        for user in User.search(status=1, page_size=-1)['data']:
            oj_username = None
            last_success_time = None
            res = CourseOJUsername.get_by_username_and_course_id(
                user.username,
                id_
            )
            if res:
                oj_username = res.oj_username
                last_success_time = res.last_success_time
            data.append({
                'username': user.username,
                'nickname': user.nickname,
                'oj': oj,
                'oj_username': oj_username,
                'last_success_time': last_success_time
            })

    return jsonify({
        'code': 0,
        'data': data
    })


@api.route('/course/<int:id_>/oj_username', methods=['POST'])
@login_required
def modify_course_username_api(id_):
    course = Course.get_by_id(id_)
    if course is None:
        raise NotFound('Course not found')
    form = ModifyCourseUsernameForm().validate_for_api().data_
    if current_user.username != form['username'] and current_user.permission != 1:
        raise AuthFailed()
    course_oj_username = CourseOJUsername.get_by_username_and_course_id(
        form['username'],
        id_
    )
    if form['oj_username'] == '' or form['oj_username'] is None:
        if course_oj_username is not None:
            course_oj_username.delete()
    elif course_oj_username is None:
        CourseOJUsername.create(
            oj_id=course.camp_oj_id,
            course_id=course.id,
            **form
        )
    else:
        course_oj_username.modify(oj_username=form['oj_username'])
    raise Success('Course username modified')


@api.route('/contest/<int:id_>/detail', methods=['GET'])
def get_contest_detail_api(id_):
    contest = CourseContest.get_by_id(id_)
    if contest is None:
        raise NotFound('Contest not found')
    data = db.session. \
        query(CourseOJUsername.oj_username, CampAcceptProblem). \
        filter(CourseOJUsername.course_id == contest.course_id). \
        filter(CampAcceptProblem.contest_id == id_). \
        filter(CampAcceptProblem.username == CourseOJUsername.username).all()
    temp = {}
    data = list(set(data))
    for item in data:
        temp.setdefault(item[0], {
            'rating': 0,
            'accepted_problems': [],
            'members': []
        })
        temp[item[0]]['accepted_problems'].append(item[1])
    data = db.session. \
        query(CourseOJUsername.oj_username, func.sum(UserContest.rating)). \
        filter(CourseOJUsername.course_id == contest.course_id, CourseOJUsername.username == UserContest.username). \
        filter(UserContest.contest_id == id_). \
        group_by(CourseOJUsername.oj_username).all()
    for item in data:
        temp.setdefault(item[0], {
            'rating': 0,
            'accepted_problems': [],
            'members': []
        })
        temp[item[0]]['rating'] = item[1]
    data = db.session.query(CourseOJUsername.oj_username, CourseOJUsername.username, User.nickname). \
        filter(CourseOJUsername.username == User.username). \
        filter(CourseOJUsername.course_id == contest.course_id).all()
    for item in data:
        temp.setdefault(item[0], {
            'rating': 0,
            'accepted_problems': [],
            'members': []
        })
        temp[item[0]]['members'].append({
            'username': item[1],
            'nickname': item[2]
        })
    for item in temp.keys():
        rating = temp[item]['rating'] / len(temp[item]['members'])
        temp[item]['rating'] = round(rating, 3)
    res = []
    for name, info in temp.items():
        res.append({
            'team_name': name if len(info['members']) > 1 else info['members'][0]['nickname'],
            'accepted_problems': info['accepted_problems'],
            'members': info['members'],
            'rating': info['rating']
        })
    return jsonify({
        'code': 0,
        'data': {
            'all_problems': contest.problems,
            'user_state': res
        }
    })


@api.route('/refresh_all', methods=['POST'])
@login_required
@admin_only
def refresh_all_api():
    submit_crawl_course_info_task()
    raise CreateSuccess('Task has been created')
