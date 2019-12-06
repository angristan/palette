from app import app, db
from app.models import Color

# Will make these objects available when running "flask shell"
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Color': Color}
