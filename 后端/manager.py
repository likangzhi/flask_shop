from flask_shop import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

app = create_app('develop')
CORS(app, supports_credentials=True)


manager = Manager(app) 
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()
    # manager.run()























