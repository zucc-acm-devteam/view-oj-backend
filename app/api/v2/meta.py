from flask import jsonify

from app.libs.global_varible import g
from app.libs.red_print import RedPrint

api = RedPrint('meta')


@api.route('/version', methods=['GET'])
def get_version_api():
    return jsonify({
        'code': 0,
        'version': g.run_start_time
    })
