from flask_sqlalchemy import SQLAlchemy


def connect(app, user, password, db, host='postgresql_db'):
    # We connect with the help of the PostgreSQL URL
    url = f'postgresql://{user}:{password}@{host}/{db}'

    app.config['SQLALCHEMY_DATABASE_URI'] = url

    db = SQLAlchemy(app)

    return db
