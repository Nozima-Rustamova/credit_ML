from django.db import models

class SoliqRecord(models.Model):
    '''
    Mocked soliq record for individeuals or any comany identified by inn
    Storing raw json returned plus some indexed fields for easy querying
    '''
    inn=models.CharField(max_length=64, db_index=True)
    name=models.CharField(max_length=255, null=True, blank=True)
    data=models.JSONField(null=True, blank=True)
    fetched_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Soliq Record"
        verbose_name_plural = "Soliq Records"
        ordering = ['-fetched_at']

    def __str__(self):
        return f"SoliqRecord({self.inn})"
    

class KadastrRecord(models.Model):
    '''
    Mocked kadastr (land registery) record for parcel id
    '''

    parcel_id=models.CharField(max_length=128, db_index=True)
    owner_name=models.CharField(max_length=255, null=True, blank=True)
    address=models.CharField(max_length=512, null=True, blank=True)
    data=models.JSONField(null=True, blank=True)
    fetched_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kadastr Record"
        verbose_name_plural = "Kadastr Records"
        ordering = ['-fetched_at']

    def __str__(self):
        return f"KadastrRecord({self.parcel_id})"