from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    price_sold = db.Column(db.Float, nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Sale(company_id='{self.company_id}', client_id='{self.client_id}', product_id='{self.product_id}', price_sold={self.price_sold}, quantity_sold={self.quantity_sold})"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    total_stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product(product_id='{self.product_id}', name='{self.name}', total_stock={self.total_stock})"

admin = Admin(app, name="Aditya's Database" , template_mode='bootstrap4')
admin.add_view(ModelView(Sale, db.session))
admin.add_view(ModelView(Product, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    company_id = request.form.get('company_id')
    client_id = request.form.get('client_id')
    product_id = request.form.get('product_id')
    price_sold = request.form.get('price_sold')
    quantity_sold = request.form.get('quantity_sold')
    
    if not (company_id and client_id and product_id and price_sold and quantity_sold):
        return "Please fill in all fields", 400
    
    try:
        price_sold = float(price_sold)
        quantity_sold = int(quantity_sold)
    except ValueError:
        return "Invalid price or quantity", 400

    
    # Fetch the product from the database
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return f"Product with ID {product_id} not found", 404
    
    # Check if enough stock is available
    if quantity_sold > product.total_stock:
        return f"Not enough stock available for {product.name}. Available stock: {product.total_stock}", 400
    
    # Update remaining stock
    remaining_stock = product.total_stock - quantity_sold
    product.total_stock = remaining_stock
    
    # Create new sale entry
    new_sale = Sale(
        company_id=company_id,
        client_id=client_id,
        product_id=product_id,
        price_sold=price_sold,
        quantity_sold=quantity_sold
    )
    
    try:
        db.session.add(new_sale)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error submitting sale: {str(e)}", 500
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)