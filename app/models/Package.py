from app import db


class PackageType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(100))
    premium = db.Column(db.Boolean, default=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package_type.id'))
    package_type = db.relationship('PackageType', backref=db.backref('package', lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('packages', lazy='dynamic'))