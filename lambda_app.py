from backend.app import app
from mangum import Mangum
handler = Mangum(app)
