from app import app
from models import User, Note
import views

if __name__ == '__main__':
    User.create_table()
    Note.create_table()
    app.run(host='localhost', port=5000, debug=True)