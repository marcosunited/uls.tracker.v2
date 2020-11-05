import os
import time

from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import FileField

from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView


class StorageSetting(models.Model):
    id = models.AutoField(primary_key=True)


def get_upload_path(instance, filename):
    return os.path.join("content_type_%d" % instance.document_type.id, str(time.time_ns())
                        + '_' + instance.document_id
                        + '_' + instance.file_sequence
                        + '_' + filename)


class FileDocument(models.Model):
    id = models.AutoField(primary_key=True)
    document_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, db_column='contentTypeId', blank=True,
                                      null=True)
    document_id = models.IntegerField(blank=True, null=True)
    file_sequence = models.IntegerField(blank=True, null=True)
    file_path = models.FilePathField(path=None)
    is_upload = models.BooleanField(blank=True, null=True)
    file = FileField(upload_to=get_upload_path, storage=FileSystemStorage(location='c:\\upload'))


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDocument
        fields = ('id',
                  'document_type',
                  'document_id',
                  'file_sequence',
                  'file_path',
                  'file',
                  'is_upload')


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
