

class Config:
    SECRET_KEY = '73e3aeed807e5f61cab1da58dec24829'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS= True
    MAIL_USERNAME= "chordograph@gmail.com"
    MAIL_PASSWORD= "fhbomvhlpsjzdmzo"
    # app.config['SECRET_KEY'] = '73e3aeed807e5f61cab1da58dec24829'
    # app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
    # app.config['MAIL_SERVER']='smtp.gmail.com'
    # app.config['MAIL_PORT']= 587
    # app.config['MAIL_USE_TLS']= True
    # # app.config['MAIL_USERNAME']= os.environ.get('EMAIL_USER')
    # # app.config['MAIL_PASSWORD']= os.environ.get('EMAIL_PASS')
    # app.config['MAIL_USERNAME']= "chordograph@gmail.com"
    # app.config['MAIL_PASSWORD']= "fhbomvhlpsjzdmzo"