import flask
import datetime as _datetime

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def datetime(value):
    dt = _datetime.datetime.utcfromtimestamp(value)
    return dt.strftime("%Y-%m-%d %H:%m:%S ")