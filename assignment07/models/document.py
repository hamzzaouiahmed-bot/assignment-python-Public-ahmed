from __future__ import annotations

from mongoengine import Document, EmbeddedDocument, fields


class AuthorDoc(EmbeddedDocument):
    full_name = fields.StringField(required=True)
    title = fields.StringField(required=True)


class ScientificArticleDoc(Document):
    title = fields.StringField(required=True)
    summary = fields.StringField()
    text = fields.StringField() 
    arxiv_id = fields.StringField(required=True)
    author = fields.EmbeddedDocumentField(AuthorDoc, required=True)

    meta = {
        "collection": "scientific_articles",
        "indexes": [
            {
                "fields": ["$text"],  
                "default_language": "english",
            }
        ],
    }
