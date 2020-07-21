from flask import jsonify
from flask_login import login_required, current_user

from app.libs.auth import admin_only
from app.libs.error_code import CreateSuccess, NotFound, Success, AuthFailed
from app.libs.red_print import RedPrint
from app.models.camp_models.camp import Camp
from app.models.camp_models.camp_oj import CampOJ
from app.models.camp_models.course import Course
from app.models.camp_models.course_oj_username import CourseOJUsername
from app.models.camp_models.course_contest import CourseContest
from app.models.camp_models.user_contest import UserContest
from app.validators.camp import (AppendContestForm, CreateCampForm,
                                 CreateCourseForm, ModifyCampNameForm,
                                 ModifyCourseForm, ModifyCourseUsernameForm)
from app.libs.spider_service import task_crawl_course_info
from app.models.user import User

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
    camps = Camp.search(page_size=-1)['data']
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
    users = User.search(status=1, page_size=-1)['data']
    res = []
    for user in users:
        rating = 0
        found = False
        for course in camp.courses:
            course_oj_username = CourseOJUsername.get_by_username_and_course_id(
                user.username,
                course.id
            )
            if course_oj_username is None:
                continue
            found = True
            rating += course_oj_username.rating
        if found:
            res.append({
                'username': user.username,
                'nickname': user.nickname,
                'status': user.status,
                'rating': rating
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


@api.route('/course/<int:id_>', methods=['PATCH'])
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
    users = User.search(status=1, page_size=-1)['data']
    res = []
    for user in users:
        course_oj_username = CourseOJUsername.get_by_username_and_course_id(
            user.username,
            id_
        )
        if course_oj_username is None:
            continue
        res.append({
            'username': user.username,
            'nickname': user.nickname,
            'status': user.status,
            'rating': course_oj_username.rating
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
    if form['oj_username'] == '':
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
    users = User.search(status=1, page_size=-1)['data']
    res = []
    for user in users:
        user_contest = UserContest.get_by_username_and_contest_id(
            user.username,
            id_
        )
        res.append({
            'user': user,
            'accepted_problems': user_contest.accepted_problems,
            'rating': user_contest.rating
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
    task_crawl_course_info()
    raise CreateSuccess('Task has been created')
