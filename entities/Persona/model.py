from mongoengine import Document, StringField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField
from ..Trait.model import Trait, Variable
class Persona(Document):
    user_id =  StringField(required=True)
    charecter_persona = StringField(required=True)
    traits = ListField(EmbeddedDocumentField(Trait), required=True, min_length=3, max_length=3)
    intrests = ListField(EmbeddedDocument(Variable),default=list)
