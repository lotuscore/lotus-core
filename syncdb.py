from db import DB, Settings

db = DB()
db.create_all()

settings = Settings(
    chain='external',
    token_address='',
    library_address=''
)

db.session.add(settings)
db.session.commit()
