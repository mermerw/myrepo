# www.entry.com

## Local dev setup steps

### 1. Pre-reqzzz
Make sure native Docker is installed, and the following ports are available
- 11211 (Memcached)
- 6606  (MySQL)
- 18000 (When served in Django runserver, mainly for dev of API)

### 2. Pick a version of `command`
Review the `dev-compose.yml` file. Two `command` options are available for two different purposes
- `python maange.py runserver` for working with backend code
- WSGI (Gunicorn / uWSGI) + Nginx for working with backend code, but remember to bind your IP and domain name in host file

Both should run without error, just leave the one for your development stage and comment the other

### 3. Run!
- Start the world by `docker-compose -f dev-compose.yml up` and after the initial build everything should just run, and the environment is now ready
- Before first request, execute `docker exec web bash -c 'cd /code && python manage.py makemigrations && python manage.py migrate'`
- Inside your favorite browser, go to `localhost:18000` if `runserver` is used or `www.entry.com` if Nginx is used

If you are in API dev phase and uses `runserver` command, a **FRIENDLY** 404 page should give you enough idea where to get started :P

### 4. Migration Steps
When doing migration, take note of the migrate sequence:
- auth
- contenttypes
- sessions
- admin
- social\_django

To support UTF8 encoding:
```
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import MySQLdb
from contextlib import closing
from django_www.settings import DATABASES

db_conf = DATABASES['default']
with closing(MySQLdb.connect(**{
    'host': db_conf['HOST'],
    'port': int(db_conf['PORT']),
    'user': db_conf['USER'],
    'passwd': db_conf['PASSWORD'],
    'db': db_conf['NAME'],
})) as conn:
    with closing(conn.cursor()) as cursor:
        cursor.execute('''ALTER TABLE auth_user CHANGE first_name first_name
            VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL''')
        cursor.execute('''ALTER TABLE auth_user CHANGE last_name last_name
            VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL''')
        cursor.execute('ALTER DATABASE %s CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci' % db_conf['NAME'])
        conn.commit()
```

Then migrate the API app. Note that explicit `makemigrations $app\_name` seems to be
a compulsary step in the new version of Django, before `migrate` detects the changes in
the API app.
