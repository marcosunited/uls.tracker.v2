# MRS BASE MODEL

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import IntegerField, DateTimeField, FileField
from django.utils import timezone

from mrs.rules.Actions import JobActions
from mrs.rules.Variables import JobVariables
from mrs.utils.storage import FileDocument
from mrsauth.models import User


class MrsModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_column='isDeleted')

    class Meta:
        abstract = True


class MetadataType(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'metadata_types'

    def __str__(self):
        return self.name


class MetadataValue(MrsModel):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(MetadataType, on_delete=models.CASCADE)
    value = models.CharField(max_length=70)

    class Meta:
        managed = True
        db_table = 'metadata_values'

    def __str__(self):
        return self.value


class Note(MrsModel):
    id = models.AutoField(primary_key=True)
    document_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,
                                      db_column='contentTypeId', blank=True, null=True)
    document_id = models.PositiveIntegerField()
    document = GenericForeignKey('document_type', 'document_id')
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=8000)

    class Meta:
        managed = True
        db_table = 'notes'

    def __str__(self):
        return self.title


class ServiceArea(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'service_area'
        app_label = 'mrs'

    def __str__(self):
        return self.name


class ServiceType(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'service_type'
        app_label = 'mrs'

    def __str__(self):
        return self.name


class ServiceTarget(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    key_name = models.CharField(db_column='keyName', max_length=50)

    class Meta:
        managed = True
        db_table = 'services_targets'
        app_label = 'mrs'

    def __str__(self):
        return self.name

class Task(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasks'

    def __str__(self):
        return self.name


class Procedure(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    tasks = models.ManyToManyField(Task)
    service_target = models.ForeignKey(ServiceTarget, on_delete=models.DO_NOTHING, db_column='serviceTargetId')

    class Meta:
        managed = True
        db_table = 'procedures'

    def __str__(self):
        return self.name


class Month(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'months'
        app_label = 'mrs'

    def __str__(self):
        return self.name


class Country(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    currency_code = models.CharField(max_length=3)
    unlocode = models.CharField(max_length=2)

    class Meta:
        managed = True
        db_table = 'countries'

    def __str__(self):
        return self.name


class Project(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, db_column='isActive')
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'projects'

    def __str__(self):
        return self.name


class ProcessType(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    initial_status = models.IntegerField(db_column='initialStatus')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'process_types'

    def __str__(self):
        return self.name + " (" + self.project.name + ")"


class ProcessTypeStatus(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_active = models.IntegerField(db_column='isActive')
    is_final = models.IntegerField(db_column='isFinal')
    sequence_number = models.PositiveSmallIntegerField(default=1)
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'process_types_status'

    def __str__(self):
        return self.name + " (" + self.process_type.name + " - " +  self.project.name + ")"


class Title(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'titles'

    def __str__(self):
        return self.name


class Profile(MrsModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, db_column='userId')
    fullname = models.CharField(db_column='fullName', max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    email_verified = models.BooleanField(db_column='emailVerified', blank=True, null=True)
    alternative_email = models.EmailField(max_length=200, blank=True, null=True)
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING, db_column='titleId', blank=True, null=True)
    street_address = models.CharField(db_column='streetAddress', max_length=255, blank=True, null=True)
    postcode = models.CharField(db_column='postCode', max_length=12, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, db_column='countryId', blank=True, null=True)
    phone_verified = models.IntegerField(db_column='phoneVerified', blank=True, null=True)
    status = models.IntegerField(db_column='statusId', blank=True, null=True)
    last_position = models.TextField(db_column='lastPosition', blank=True, null=True)
    localization_code = models.CharField(db_column='localizationCode', max_length=8, blank=True, null=True)
    currency_code = models.CharField(db_column='currencyCode', max_length=3, blank=True, null=True)
    default_project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='default_project')
    projects = models.ManyToManyField(Project, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_column='isActive', blank=True, null=True)
    avatar = models.ImageField(upload_to='images/avatar', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'profile'

    def __str__(self):
        return self.fullname


class Contact(MrsModel):
    id = models.AutoField(primary_key=True)
    title = models.PositiveIntegerField()
    position = models.PositiveIntegerField()
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=250)

    class Meta:
        managed = True
        db_table = 'contacts'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Attachment(MrsModel):
    id = models.AutoField(primary_key=True)
    conceptid = models.IntegerField(db_column='conceptId', unique=True)
    valueconcept = models.IntegerField(db_column='valueConcept')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=512)

    class Meta:
        managed = True
        db_table = 'attachments'

    def __str__(self):
        return self.name


class Brand(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'brands'

    def __str__(self):
        return self.name


class Technician(MrsModel):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING, db_column='profileId')
    notes = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'technicians'

    def __str__(self):
        return self.profile.fullname


class Supplier(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'suppliers'

    def __str__(self):
        return self.name


class Part(MrsModel):
    id = models.AutoField(primary_key=True)
    part_number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=500)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, db_column='brandId', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, db_column='supplierId', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'parts'

    def __str__(self):
        return self.name


class Inventory(MrsModel):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, db_column='partId', blank=True, null=True)
    reorder_details = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(db_column='quantity')
    warning_quantity = models.IntegerField(db_column='warning_quantity')
    shelf_number = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'inventory'

    def __str__(self):
        return self.part.name + " (" + self.quantity + ")"


class ContractFrequency(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    days_frequency = IntegerField(default=7)

    class Meta:
        managed = True
        db_table = 'contracts_frequencies'

    def __str__(self):
        return self.name


class Contract(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(db_column='isActive', blank=True, null=True)
    start_datetime = models.DateTimeField(db_column='startDatetime', blank=True, null=True)
    end_datetime = models.DateTimeField(db_column='endDatetime', blank=True, null=True)
    stand_by_datetime = models.DateTimeField(db_column='standByDatetime', blank=True, null=True)
    reactive_datetime = models.DateTimeField(db_column='reactiveDatetime', blank=True, null=True)
    cancel_datetime = models.CharField(db_column='cancelDatetime', max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    frequency_mtn_id = models.IntegerField(db_column='frequencyMtnId', unique=True, blank=True, null=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, blank=True, null=True)
    contract_frequency = models.OneToOneField(ContractFrequency, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId', default='1')

    class Meta:
        managed = True
        db_table = 'contracts'

    def __str__(self):
        return self.name


class Correction(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    service_target_id = models.IntegerField(db_column='serviceTargetId')

    class Meta:
        managed = True
        db_table = 'corrections'

    def __str__(self):
        return self.name


class Fault(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'faults'

    def __str__(self):
        return self.name


class JhaItem(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(db_column='isActive')
    is_ticked_default = models.IntegerField(db_column='isTickedDefault', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jha_items'

    def __str__(self):
        return self.name


class Round(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(db_column='isActive')
    colour = models.CharField(max_length=30, blank=True, null=True)
    polygon = models.TextField(blank=True, null=True)
    technicians = models.ManyToManyField(Technician, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'rounds'

    def __str__(self):
        return self.name


class Agent(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'agents'

    def __str__(self):
        return self.name + " - " + self.contact.first_name + " " + self.contact.last_name


class Job(MrsModel):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name='Number')
    name = models.CharField(max_length=50, verbose_name='Name')
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, verbose_name='Contact', db_column='contactId')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, db_column='contractId')
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, db_column='agentId')
    round = models.ForeignKey(Round, on_delete=models.DO_NOTHING, db_column='roundId')
    floors = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(db_column='postCode', max_length=12, blank=True, null=True)
    key_access_details = models.CharField(db_column='keyAccessDetails', max_length=255, blank=True, null=True)
    notes = models.TextField(max_length=2048, blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    address = models.CharField(db_column='address', max_length=100, blank=True, null=True)
    suburb = models.CharField(db_column='suburb', max_length=100, blank=True, null=True)
    group = models.CharField(db_column='group', max_length=100, blank=True, null=True)
    owner_details = models.CharField(db_column='ownerDetails', max_length=250, blank=True, null=True)
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId', default='1')
    documents = models.ManyToManyField(FileDocument)

    class Meta:
        managed = True
        db_table = 'jobs'

    class RulesConf:
        variables = JobVariables
        actions = JobActions

    def __str__(self):
        return self.name


class Lift(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, db_column='jobId')
    model = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(db_column='isActive')
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, db_column='brandId')
    registration_number = models.CharField(db_column='registrationNumber', max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    drive = models.CharField(max_length=255, blank=True, null=True)
    has_light_trays = models.IntegerField(db_column='hasLightRays')
    speed = models.IntegerField(blank=True, null=True)
    installed_date = models.DateTimeField(db_column='installedDate', blank=True, null=True)
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId', blank=True,
                               null=True)

    class Meta:
        managed = True
        db_table = 'lifts'

    def __str__(self):
        return self.name


class ServicesTypes(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    key_name = models.CharField(db_column='keyName', max_length=10)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'services_types'

    def __str__(self):
        return self.name


class Settings(MrsModel):
    id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=20)
    key = models.CharField(max_length=3)
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255)
    value1 = models.CharField(max_length=255, blank=True, null=True)
    value2 = models.CharField(max_length=255, blank=True, null=True)
    value3 = models.CharField(max_length=255, blank=True, null=True)
    value4 = models.CharField(max_length=255, blank=True, null=True)
    value5 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'settings'

    def __str__(self):
        return self.module + "(" + self.code + ")"


class Workflow(MrsModel):
    id = models.AutoField(primary_key=True)
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255)
    status = models.ForeignKey(ProcessTypeStatus, related_name='wf_current_status', on_delete=models.DO_NOTHING,
                               db_column='statusId')
    next_status = models.ForeignKey(ProcessTypeStatus, related_name='wf_next_status', on_delete=models.DO_NOTHING,
                                    db_column='nextStatus')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workflows'

    def __str__(self):
        return self.name


class WorkflowEvent(MrsModel):
    id = models.AutoField(primary_key=True)
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    previous_status = models.ForeignKey(ProcessTypeStatus, related_name='event_previous_status',
                                        on_delete=models.DO_NOTHING, db_column='previousStatus')
    new_status = models.ForeignKey(ProcessTypeStatus, related_name='wo_new_status', on_delete=models.DO_NOTHING,
                                   db_column='newStatus')
    workflow = models.ForeignKey(Workflow, on_delete=models.DO_NOTHING, db_column='workflowId')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workflow_event'

    def __str__(self):
        return self.process_type.name + " (" + self.previous_status.name + " -> " + self.new_status.name + ")"


class Priority(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'priority'

    def __str__(self):
        return self.name


class WorkorderLift(MrsModel):
    id = models.AutoField(primary_key=True)
    lift = models.ForeignKey(Lift, on_delete=models.DO_NOTHING, db_column='liftId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')
    notes = models.CharField(max_length=255, blank=True, null=True)
    started_datetime = models.DateTimeField(db_column='startedDatetime', blank=True, null=True)
    completed_datetime = models.DateTimeField(db_column='completedDatetime', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workorders_lifts'




class Workorder(MrsModel):
    id = models.AutoField(primary_key=True)
    id_by_project = models.IntegerField(db_column='idByProject')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, db_column='jobId')
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    priority = models.ForeignKey(Priority, on_delete=models.DO_NOTHING, db_column='priorityId')
    technician = models.ForeignKey(Technician, on_delete=models.DO_NOTHING, db_column='technicianId')
    customer_id = models.IntegerField(db_column='customerId')
    accepted_datetime = models.DateTimeField(db_column='acceptedDatetime', blank=True, null=True)
    started_datetime = models.DateTimeField(db_column='startedDatetime', blank=True, null=True)
    scheduled_datetime = models.DateTimeField(db_column='scheduledDatetime', blank=True, null=True)
    completed_datetime = models.DateTimeField(db_column='completedDatetime', blank=True, null=True)
    reported_fault = models.ForeignKey(Fault, on_delete=models.DO_NOTHING, db_column='reportedFaultId', blank=True,
                                       null=True)
    detected_fault = models.IntegerField(db_column='detectedFaultId', blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=32000, blank=True, null=True)
    notes = models.ManyToManyField(Note)
    correction = models.ForeignKey(Correction, models.DO_NOTHING, db_column='correctionId')
    solution = models.TextField(max_length=32000, blank=True, null=True)
    signature = models.IntegerField(db_column='signatureId', blank=True, null=True)
    attention_time = models.IntegerField(db_column='attentionTime', blank=True, null=True)
    solution_time = models.IntegerField(db_column='solutionTime', blank=True, null=True)
    expected_time = models.IntegerField(db_column='expectedTime', blank=True, null=True)
    is_chargeable = models.BooleanField(default='False', db_column='isChargeable')
    part_required = models.IntegerField(db_column='partRequired')
    is_closed = models.BooleanField(default=False, db_column='isClosed')
    jha_items = models.ManyToManyField(JhaItem)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workorders'


class ClosedWorkorder(MrsModel):
    id = models.AutoField(primary_key=True)
    workorder_lifts = models.ManyToManyField(WorkorderLift)
    id_by_project = models.IntegerField(db_column='idByProject')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, db_column='jobId')
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    priority = models.ForeignKey(Priority, on_delete=models.DO_NOTHING, db_column='priorityId')
    technician = models.ForeignKey(Technician, on_delete=models.DO_NOTHING, db_column='technicianId')
    notes = models.ManyToManyField(Note)
    customer_id = models.IntegerField(db_column='customerId')
    accepted_datetime = models.DateTimeField(db_column='acceptedDatetime', blank=True, null=True)
    started_datetime = models.DateTimeField(db_column='startedDatetime', blank=True, null=True)
    scheduled_datetime = models.DateTimeField(db_column='scheduledDatetime', blank=True, null=True)
    completed_datetime = models.DateTimeField(db_column='completedDatetime', blank=True, null=True)
    reported_fault = models.ForeignKey(Fault, related_name='wo_reported_fault', on_delete=models.DO_NOTHING,
                                       db_column='reportedFaultId', blank=True, null=True)
    detected_fault = models.ForeignKey(Fault, related_name='wo_detected_fault', on_delete=models.DO_NOTHING,
                                       db_column='detectedFaultId', blank=True, null=True)
    lift = models.ForeignKey(Lift, on_delete=models.DO_NOTHING, db_column='liftId')
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=32000, blank=True, null=True)
    correction = models.ForeignKey(Correction, models.DO_NOTHING, db_column='correctionId')
    solution = models.CharField(max_length=32000, blank=True, null=True)
    signature = models.IntegerField(db_column='signatureId', blank=True, null=True)
    attention_time = models.IntegerField(db_column='attentionTime', blank=True, null=True)
    solution_time = models.IntegerField(db_column='solutionTime', blank=True, null=True)
    expected_time = models.IntegerField(db_column='expectedTime', blank=True, null=True)
    is_chargeable = models.BooleanField(default='False', db_column='isChargeable')
    part_required = models.IntegerField(db_column='partRequired')

    class Meta:
        managed = True
        db_table = 'closed_workorders'


class WorkordersHistory(MrsModel):
    id = models.AutoField(primary_key=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    change_type_id = models.IntegerField(db_column='changeTypeId')
    value = models.CharField(max_length=4000)
    user_id = models.IntegerField(db_column='userId', unique=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')
    timestamp = models.DateTimeField(default=timezone.now())

    class Meta:
        managed = True
        db_table = 'workorders_history'


class PartRequest(MrsModel):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(db_column='quantity')
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, db_column='partId')
    description = models.CharField(max_length=4000, blank=True, null=True)
    reason_chargeable = models.CharField(db_column='reasonChargeable', max_length=4000, blank=True, null=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    remark = models.CharField(max_length=512, blank=True, null=True)
    project = models.IntegerField(db_column='projectId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId', default='1')

    class Meta:
        managed = True
        db_table = 'parts_requests'


class WorkorderLocation(MrsModel):
    id = models.AutoField(primary_key=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')
    latitude = models.DecimalField(max_digits=4, decimal_places=4, blank=True, null=True)
    longitude = models.DecimalField(max_digits=4, decimal_places=4, blank=True, null=True)
    position = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workorders_positions'


class MaintenancePlan(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    lift = models.ForeignKey(Lift, on_delete=models.DO_NOTHING, db_column='liftId')
    procedures = models.ManyToManyField(Procedure)

    class Meta:
        managed = True
        db_table = 'maintenance_plans'


class ScheduleEntry(MrsModel):
    id = models.AutoField(primary_key=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    lift = models.ForeignKey(Lift, on_delete=models.DO_NOTHING, db_column='liftId')
    procedure = models.ForeignKey(Procedure, on_delete=models.DO_NOTHING, db_column='taskId')
    schedule_date = models.DateField(db_column='scheduleDate')
    workorder = models.OneToOneField(Workorder, on_delete=models.CASCADE, primary_key=False)

    class Meta:
        managed = True
        db_table = 'schedule_entries'


"""
SYSTEM MODELS
"""


class MrsOperator(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    django_lookup = models.CharField(max_length=50)
    rules_operator = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mrs_mrsoperator'

    def __str__(self):
        return self.name


class MrsField(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    operators = models.ManyToManyField(MrsOperator)
    isList = models.BooleanField(default=False)
    list_source_model = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mrs_fields'

    def __str__(self):
        return self.name


class Report(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    report_processor = models.CharField(max_length=150)
    report_template = models.TextField()

    class Meta:
        managed = True
        db_table = 'reports'

    def __str__(self):
        return self.name


class ReportHistory(MrsModel):
    id = models.AutoField(primary_key=True)
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING, db_column='reportId')
    finish_timestamp = models.DateTimeField(default=timezone.now())
    output_file = FileField(storage=FileSystemStorage(location='c:\\reports'))
    result = models.CharField(max_length=30, blank=True, null=True)


class Rule(MrsModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, db_column='contentTypeId', null=True)
    description = models.TextField(blank=True, null=True)
    conditions = models.JSONField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'business_rules'

    def __str__(self):
        return self.name


class ActionsHistory(MrsModel):
    id = models.AutoField(primary_key=True)
    rule = models.JSONField()
    variables = models.CharField(max_length=250, blank=True)
    actions = models.CharField(max_length=250, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, db_column='contentTypeId', null=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    model_state = models.JSONField()
    timestamp = DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    hash = models.CharField(max_length=250, blank=True)
    executed = models.BooleanField(blank=True, null=True)


# init models event receivers to enable rules engine
from mrs.rules.JobReceivers import *
