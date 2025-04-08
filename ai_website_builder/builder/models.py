# builder/models.py
import uuid
from django.db import models
import json

class Website(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    generated_content = models.TextField(default="{}", blank=True)
    custom_content = models.TextField(default="{}", blank=True)
    preview_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_generated_content(self, content):
        if isinstance(content, dict):
            self.generated_content = json.dumps(content)
        elif isinstance(content, str):
            self.generated_content = content

    def get_generated_content(self):
        try:
            return json.loads(self.generated_content)
        except:
            return {"error": "Invalid JSON format"}

    def set_custom_content(self, content):
        if isinstance(content, dict):
            self.custom_content = json.dumps(content)
        elif isinstance(content, str):
            self.custom_content = content

    def get_custom_content(self):
        try:
            return json.loads(self.custom_content)
        except:
            return {"error": "Invalid JSON format"}

    def __str__(self):
        return self.name
    def get_preview_url(self):
        return f"/preview/{self.preview_token}/"
