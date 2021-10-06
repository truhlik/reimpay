from .base import *

ALLOW_ROBOTS = False
GOOGLE_MAPS_API_KEY = None

from model_bakery import baker
baker.generators.add('encrypted_fields.fields.EncryptedCharField', baker.generators.random_gen.gen_string)