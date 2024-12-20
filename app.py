from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database model
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    expiry_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Medicine {self.name}>"

@app.route('/')
def index():
    medicines = Medicine.query.all()
    return render_template('index.html', medicines=medicines)

@app.route('/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        expiry_date = request.form['expiry_date']
        try:
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            new_medicine = Medicine(name=name, stock=int(stock), expiry_date=expiry_date)
            db.session.add(new_medicine)
            db.session.commit()
            flash("Medicine added successfully!", "success")
            return redirect(url_for('index'))
        except ValueError:
            flash("Invalid input!", "danger")
            return redirect(url_for('add_medicine'))
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
