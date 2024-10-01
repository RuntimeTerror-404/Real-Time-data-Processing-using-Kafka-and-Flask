from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'status': self.status,
            'organization': self.organization
        }
