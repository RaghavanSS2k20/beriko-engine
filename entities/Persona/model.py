from mongoengine import Document, StringField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField
from ..Trait.model import Trait, Variable
class Persona(Document):
    user_id =  StringField(required=True)
    charecter_persona = StringField(required=True)
    traits = ListField(ReferenceField(Trait, reverse_delete_rule=2), required=True, min_length=3, max_length=3)
    intrests = ListField(EmbeddedDocumentField(Variable),default=list)
