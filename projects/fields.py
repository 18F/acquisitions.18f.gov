from django.db.models.fields import TextField


class DocumentField(TextField):

    description = "A field for storing a document and marking it as public or "
    "private"

    def __init__(self, *args, **kwargs):
        public = kwargs.pop('public', None)
        public_after = kwargs.pop('public_after', None)
        if public_after is not None:
            self.public_after = public_after
            self.public = None
        elif public is not None:
            self.public_after = None
            self.public = public
        super(DocumentField, self).__init__(*args, **kwargs)
