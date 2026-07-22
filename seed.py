from app import create_app
from extensions import db
from models.category import Category
from models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    if Category.query.count() == 0:
        cats = [
            ('Programming',      'ti-code'),
            ('Design',           'ti-palette'),
            ('Languages',        'ti-language'),
            ('Data & Analytics', 'ti-chart-bar'),
            ('Music',            'ti-music'),
            ('Photography',      'ti-camera'),
            ('Mathematics',      'ti-math'),
            ('Writing',          'ti-pencil'),
            ('Other',            'ti-dots'),
        ]
        for name, icon in cats:
            db.session.add(Category(name=name, icon=icon))
        db.session.commit()
        print(f"Seeded {len(cats)} categories.")
    else:
        print("Categories already seeded.")

    if not User.query.filter_by(email='admin@skillswap.com').first():
        admin = User(
            full_name='Admin User',
            email='admin@skillswap.com',
            university='SkillSwap HQ',
            department='Admin',
            year_of_study=1,
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@skillswap.com / admin123")
    else:
        print("Admin already exists.")

    print("Done!")


