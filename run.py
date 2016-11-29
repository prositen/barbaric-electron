from app import app

__author__ = 'Anna Holmgren'

app.run(host=app.config['BARBARIC_HOST'],
        port=app.config['BARBARIC_PORT'], debug=app.config['DEBUG'])
