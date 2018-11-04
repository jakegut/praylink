import os
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from praylink import app, db

manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command('runserver', Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000))
    )
)
    
if __name__ == "__main__":
    manager.run()