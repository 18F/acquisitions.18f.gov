from django.db.models.fields import TextField


class DocumentField(TextField):

    description = "A field for storing a document and marking it as public or "
    "private"

    def __init__(self, *args, **kwargs):
        public = kwargs.pop('public', False)
        self.public = public
        super(DocumentField, self).__init__(*args, **kwargs)
