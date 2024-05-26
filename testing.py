from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


cities = storage.get(City, "521a55f4-7d82-47d9-b54c-a76916479545")
print(cities.to_dict())

