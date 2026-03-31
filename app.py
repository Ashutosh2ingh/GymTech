from flask import Flask, render_template, request, redirect, flash, url_for, session
from models import db, User, Plan, PlanFeature, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os, uuid
from datetime import datetime, timedelta
from flask_migrate import Migrate

app = Flask(__name__)

# 🔗 Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'dev-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)

FEATURE_LIST = [
    "Gym Access",
    "Cardio Equipment",
    "Personal Trainer",
    "Diet Plan",
    "Group Classes"
]

# 👇 Registerpage now renders HTML
@app.route('/register', methods=['GET','POST'])
def register():

    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('User with this email already exist!', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)

        user = User(name=name,email=email,password=hashed_password,created_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        
        flash('Registration Successfull! Please Login','success')
        return redirect(url_for('login'))
    return render_template('register.html')


# 👇 Loginpage now renders HTML
@app.route('/login', methods=['GET','POST'])
def login():

    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email=request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id 
            session['user_type'] = (user.profile.user_type if user.profile else 'Member')
            session['user_image'] = (user.profile.image if user.profile and user.profile.image else 'about.png')
            flash('Login Successfull!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Email or Password!', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')


# 👇 Logout 
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# 👇 Homepage now renders HTML
@app.route('/')
def home():

    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('home.html')


# 👇 Profile renders HTML
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])

    return render_template('profile.html', user=user)


# 👇 Update Profile
@app.route('/update-profile', methods=['POST'])
def update_profile():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('login'))

    phone = request.form.get('phone')
    address = request.form.get('address')
    user_type = request.form.get('user_type')
    image = request.files.get('image') 

    # If profile does not exist, create it
    if not user.profile:
        profile = Profile(
            user_id=user.id,
            phone=phone,
            address=address,
            user_type=user_type if user_type in ['Admin', 'Member'] else 'Member'
        )
        db.session.add(profile)
    else:
        user.profile.phone = phone
        user.profile.address = address

        if session.get('user_type') == 'Admin':
            if user_type in ['Admin', 'Member']:
                user.profile.user_type = user_type
        else:
            user.profile.user_type = 'Member'

    # 👇 IMAGE UPLOAD LOGIC
    if image and image.filename != "":
        filename = secure_filename(image.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            unique_name
        )

        image.save(image_path)

        user.profile.image = unique_name
        session['user_image'] = unique_name

    db.session.commit()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


# 👇 Members renders HTML
@app.route('/members')
def members():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('user_type') != 'Admin':
        flash('Access Denied!', 'error')
        return redirect(url_for('home'))
    
    users = User.query.all()
    plans = Plan.query.all()

    return render_template('members.html', members=users, plans=plans)


# 👇 Add Members
@app.route('/admin/add-member', methods=['POST'])
def add_member():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('user_type') != 'Admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    address = request.form.get('address')
    user_type = request.form.get('user_type')
    plan_id = request.form.get('plan_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        flash('User already exists!', 'error')
        return redirect(url_for('members'))

    hashed_password = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        created_at=datetime.utcnow()
    )

    db.session.add(user)
    db.session.commit()

    profile = Profile(
        user_id=user.id,
        phone=phone,
        address=address,
        user_type=user_type if user_type in ['Admin', 'Member'] else 'Member',
        plan_id=plan_id if plan_id else None,
        start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date else None,
        end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    )

    db.session.add(profile)
    db.session.commit()

    flash('Member created successfully!', 'success')
    return redirect(url_for('members'))


# 👇 Update Members
@app.route('/admin/update-user', methods=['POST'])
def update_user():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('user_type') != 'Admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))

    user_id = request.form.get('user_id')
    phone = request.form.get('phone')
    plan_id = request.form.get('plan_id')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    user = User.query.get(user_id)

    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('members'))

    # create profile if not exists
    if not user.profile:
        user.profile = Profile(user_id=user.id)

    user.profile.phone = phone

    # plan handling
    user.profile.plan_id = plan_id if plan_id else None

    # date handling
    user.profile.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    user.profile.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

    db.session.commit()

    flash('Members detail updated successfully!', 'success')
    return redirect(url_for('members'))


# 👇 Delete Member (Admin only)
@app.route('/delete-member', methods=['POST'])
def delete_member():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('user_type') != 'Admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))

    user_id = request.form.get('user_id')

    user = User.query.get(user_id)

    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('members'))

    # Prevent admin from deleting himself
    if str(user.id) == str(session.get('user_id')):
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('members'))

    # Delete profile image if exists
    if user.profile and user.profile.image:
        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            user.profile.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete profile first
    if user.profile:
        db.session.delete(user.profile)

    # Delete user
    db.session.delete(user)
    db.session.commit()

    flash('Member deleted successfully!', 'success')
    return redirect(url_for('members'))


# 👇 Plan renders HTML
@app.route('/plan')
def plan():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    plans = Plan.query.all()

    return render_template('plans.html', plans=plans, feature_list=FEATURE_LIST)


# 👇 Add Plan renders HTML
@app.route('/admin/add-plan', methods=['POST'])
def add_plan():

    if 'user_id' not in session or session.get('user_type') != 'Admin':
        flash('Unauthorized!', 'error')
        return redirect(url_for('plan'))

    name = request.form.get('name')
    price = request.form.get('price')
    selected_features = request.form.getlist('features')

    new_plan = Plan(name=name, price=price)

    db.session.add(new_plan)
    db.session.commit()

    for feature_name in FEATURE_LIST:
        feature = PlanFeature(
            plan_id=new_plan.id,
            feature_name=feature_name,
            is_available=(feature_name in selected_features)
        )
        db.session.add(feature)
    db.session.commit()

    flash('Plan added successfully!', 'success')
    return redirect(url_for('plan'))


# 👇 Update Plan renders HTML
@app.route('/admin/update-plan', methods=['POST'])
def update_plan():

    if 'user_id' not in session or session.get('user_type') != 'Admin':
        flash('Unauthorized!', 'error')
        return redirect(url_for('plan'))

    plan_id = request.form.get('plan_id')
    name = request.form.get('name')
    price = request.form.get('price')
    selected_features = request.form.getlist('features')

    plan = Plan.query.get(plan_id)

    if not plan:
        flash('Plan not found!', 'error')
        return redirect(url_for('plan'))

    plan.name = name
    plan.price = price
    PlanFeature.query.filter_by(plan_id=plan.id).delete()

    for feature_name in FEATURE_LIST:
        feature = PlanFeature(
            plan_id=plan.id,
            feature_name=feature_name,
            is_available=(feature_name in selected_features)
        )
        db.session.add(feature)
    db.session.commit()

    flash('Plan updated successfully!', 'success')
    return redirect(url_for('plan'))


# 👇 Delete Plan (Admin only)
@app.route('/admin/delete-plan', methods=['POST'])
def delete_plan():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session.get('user_type') != 'Admin':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))

    plan_id = request.form.get('plan_id')

    plan = Plan.query.get(plan_id)

    if not plan:
        flash('Plan not found!', 'error')
        return redirect(url_for('plan'))

    db.session.delete(plan)
    db.session.commit()

    flash('Plan deleted successfully!', 'success')
    return redirect(url_for('plan'))


# 👇 Contact now renders HTML
@app.route('/contact')
def contact():

    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)