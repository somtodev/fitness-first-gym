from app import db


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('packages', lazy='dynamic'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    trainer = db.relationship('Trainer', backref=db.backref('package', lazy='dynamic'))
    current_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Colum(db.Integer, default=10)

