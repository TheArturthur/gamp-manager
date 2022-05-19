from . import db


class Exporters(db.Model):
    __tablename__ = 'Exporters'
    idExporter = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    Name = db.Column(db.String(45), nullable=True, default=None)
    URL = db.Column(db.String(100), nullable=True, default=None, unique=True)
    Latest_version = db.Column(db.String(45), nullable=True, default=None)

    targets = db.relationship('Targets', backref='exporter', lazy=True)


class Projects(db.Model):
    __tablename__ = 'Projects'
    idProject = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    Name = db.Column(db.String(45), nullable=False, default="")
    Datacenter = db.Column(db.String(45), nullable=False, default=None)

    targets = db.relationship('Targets', backref='project', lazy=True)


class Targets(db.Model):
    __tablename__ = 'Targets'
    idTarget = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    Name = db.Column(db.String(45), nullable=True, default=None)
    OS = db.Column(db.String(45), nullable=True, default=None)
    Prometheus = db.Column(db.String(45), nullable=True, default=None)
    Environment = db.Column(db.String(45), nullable=True, default=None)
    Monitoring = db.Column(db.String(45), nullable=True, default=None)
    Alerting = db.Column(db.String(45), nullable=True, default=None)
    Port = db.Column(db.Integer, nullable=True, default=None)
    Project_id = db.Column(db.Integer, db.ForeignKey('Projects.idProject'), nullable=False)
    Exporter_id = db.Column(db.Integer, db.ForeignKey('Exporters.idExporter'), nullable=False)
