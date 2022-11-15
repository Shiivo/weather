from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Result(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    us_p = db.Column(db.Text(), nullable=False)
    # us_c = db.Column(db.Text(), nullable=False)
    # us_e = db.Column(db.Text(), nullable=False)
    # us_m = db.Column(db.Text(), nullable=False)
    feels_like = db.Column(db.Float(), nullable=False)
    dt_obj = db.Column(db.DateTime(), nullable=False)
    temp = db.Column(db.Float(), nullable=False)
    weather = db.Column(db.Text(), nullable=False)
    location = db.Column(db.Text(), nullable=True)


    def to_dict(self):
        return{
            'us_p': self.us_p,
            # 'us_c': self.us_c,
            # 'us_e': self.us_e,
            # 'us_m': self.us_m,
            'feels_like': self.feels_like,
            'dt_obj': self.dt_obj,
            'temp': self.temp,
            'weather': self.weather,
            'location': self.temp,
        }
