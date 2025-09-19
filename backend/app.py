from flask import Flask
from blueprints import routes
from models import User,db
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS



app=Flask(__name__)
CORS(app)


app.config.from_object(Config)
db.init_app(app)

migrate=Migrate(app,db)

jst=JWTManager(app)




app.register_blueprint(routes)






if __name__=='__main__':
    app.run(debug=True)