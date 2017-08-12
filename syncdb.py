from app.db import DB, Settings

db = DB()
db.create_all()

if db.session.query(Settings).count() == 0:
    settings = Settings(
        chain='external',
        token_address='',
        library_address=''
    )
    db.session.add(settings)
    db.session.commit()
