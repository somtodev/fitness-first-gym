# Author: Somtochukwu Nnalue
# Description: For Clean Code The App Was Modularized Into A Package(App)
from app import app, db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)