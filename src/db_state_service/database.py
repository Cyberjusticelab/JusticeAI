from flask_sqlalchemy import SQLAlchemy


def connect(app, user, password, db, host='postgresql_db'):
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{user}:{password}@{host}/{db}'.format(user=user, password=password, host=host, db=db)

    app.config['SQLALCHEMY_DATABASE_URI'] = url

    db = SQLAlchemy(app)

    return db
