from mongoengine import Document, StringField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField

class Variable(EmbeddedDocument):
    slug = StringField(required=True)
    name = StringField(required=True)
    value = FloatField(required=True)

class Trait(Document):
    user_id = StringField(required=True)
    type = StringField(required=True, choices=('behavioral', 'psychological', 'demographic'))
    variables = ListField(EmbeddedDocumentField(Variable))

    meta = {
        'indexes': [
            {'fields': ['user_id', 'type'], 'unique': True}
        ]
    }