# barbaric-electron

## Setup

```bash
mkvirtualenv --python=/usr/bin/python3 derp
pip install -r requirements.txt
cp config.py.skeleton config.py
vim config.py  # Edit SECRET_KEY, SECURITY_PASSWORD_SALT, BARBARIC_PORT and BARBARIC_HOST
python manage.py db upgrade
python manage.py add_admin <email>
```

Add directories by editing `electron.db:directory` in your favorite sqlite editing software.

```bash
python run.py
```

