# UNITED LIFTS MRS BASE MODEL
from django.db import models
from mrsauth.models import User


class ServiceTarget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    key_name = models.CharField(db_column='keyName', max_length=50)

    class Meta:
        managed = True
        db_table = 'services_targets'
        app_label = 'mrs'


class ServiceArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(db_column='description', max_length=250)

    class Meta:
        managed = True
        db_table = 'services_areas'
        app_label = 'mrs'


class Month(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'months'
        app_label = 'mrs'

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    currency_code = models.CharField(max_length=3)
    unlocode = models.CharField(max_length=2)

    class Meta:
        managed = True
        db_table = 'countries'


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, db_column='isActive')
    description = models.CharField(max_length=255, blank=True, null=True)
    key_name = models.CharField(db_column='keyName', max_length=8)

    class Meta:
        managed = True
        db_table = 'projects'

    def __str__(self):
        return self.name

class ProcessType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    initial_status = models.IntegerField(db_column='initialStatus')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'process_types'


class ProcessTypeStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_active = models.IntegerField(db_column='isActive')
    is_final = models.IntegerField(db_column='isFinal')
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'process_types_status'


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'titles'


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='profiles', on_delete=models.DO_NOTHING, db_column='userId')
    fullname = models.CharField(db_column='fullName', max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    email_verified = models.IntegerField(db_column='emailVerified', blank=True, null=True)
    title = models.ForeignKey(Title, on_delete=models.DO_NOTHING, db_column='titleId', blank=True, null=True)
    street_address = models.CharField(db_column='streetAddress', max_length=255, blank=True, null=True)
    postcode = models.CharField(db_column='postCode', max_length=12, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, db_column='countryId', blank=True, null=True)
    phone_verified = models.IntegerField(db_column='phoneVerified', blank=True, null=True)
    status = models.IntegerField(db_column='statusId', blank=True, null=True)
    last_position = models.TextField(db_column='lastPosition', blank=True, null=True)
    localization_code = models.CharField(db_column='localizationCode', max_length=8, blank=True, null=True)
    currency_code = models.CharField(db_column='currencyCode', max_length=3, blank=True, null=True)
    projects = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId', blank=True, null=True)
    is_active = models.BooleanField(default=True, db_column='isActive', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'profile'

    def __str__(self):
        return self.fullname


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=250)

    class Meta:
        managed = True
        db_table = 'contacts'

    def __str__(self):
        return self.first_name + " " + self.last_name

class Attachment(models.Model):
    id = models.AutoField(primary_key=True)
    conceptid = models.IntegerField(db_column='conceptId', unique=True)
    valueconcept = models.IntegerField(db_column='valueConcept')
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=512)

    class Meta:
        managed = True
        db_table = 'attachments'


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'brands'


class Technician(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING, db_column='profileId')
    notes = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'technicians'

    def __str__(self):
        return self.profile.fullname


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'suppliers'


class Part(models.Model):
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


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, db_column='partId', blank=True, null=True)
    reorder_details = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(db_column='quantity')
    warning_quantity = models.IntegerField(db_column='warning_quantity')
    shelf_number = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'inventory'


class ContractFrequency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'contracts_frequencies'

    def __str__(self):
        return self.name


class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.IntegerField(db_column='isActive')
    start_datetime = models.DateTimeField(db_column='startDatetime', blank=True, null=True)
    end_datetime = models.DateTimeField(db_column='endDatetime', blank=True, null=True)
    stand_by_datetime = models.DateTimeField(db_column='standByDatetime', blank=True, null=True)
    reactive_datetime = models.DateTimeField(db_column='reactiveDatetime', blank=True, null=True)
    cancel_datetime = models.CharField(db_column='cancelDatetime', max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    frequency_mtn_id = models.IntegerField(db_column='frequencyMtnId', unique=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    contract_frequency = models.OneToOneField(ContractFrequency, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contracts'

    def __str__(self):
        return self.name


class Correction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    service_target_id = models.IntegerField(db_column='serviceTargetId')

    class Meta:
        managed = True
        db_table = 'corrections'


class Fault(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'faults'


class JhaItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(db_column='isActive')
    is_ticked_default = models.IntegerField(db_column='isTickedDefault', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jha_items'


class Round(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(db_column='isActive')
    colour = models.CharField(max_length=30, blank=True, null=True)
    polygon = models.TextField(blank=True, null=True)
    technicians = models.ManyToManyField(Technician)

    class Meta:
        managed = True
        db_table = 'rounds'

    def __str__(self):
        return self.name


class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'agents'

    def __str__(self):
        return self.name + " - " + self.contact.first_name + " " + self.contact.last_name


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    contact = models.OneToOneField(Contact, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    agent = models.OneToOneField(Agent, on_delete=models.DO_NOTHING)
    round = models.ForeignKey(Round, on_delete=models.DO_NOTHING, db_column='roundId')
    service_type_id = models.IntegerField(db_column='serviceTypeId')
    floors = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(db_column='postCode', max_length=12, blank=True, null=True)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    key_access_details = models.CharField(db_column='keyAccessDetails', max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=4000, blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    address = models.CharField(db_column='address', max_length=100, blank=True, null=True)
    suburb = models.CharField(db_column='suburb', max_length=50, blank=True, null=True)
    lifts = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'jobs'

    def __str__(self):
        return self.name


class Lift(models.Model):
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
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')

    class Meta:
        managed = True
        db_table = 'lifts'


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    default_month = models.ForeignKey(Month, on_delete=models.DO_NOTHING, db_column='defaultMonth')
    service_target = models.ForeignKey(ServiceTarget, on_delete=models.DO_NOTHING, db_column='serviceTargetId')
    service_area = models.ForeignKey(ServiceArea, on_delete=models.DO_NOTHING, db_column='serviceAreaId')

    class Meta:
        managed = True
        db_table = 'tasks'


class LiftTask(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, db_column='taskId')
    is_completed = models.IntegerField(db_column='isCompleted')
    completed_Datetime = models.DateTimeField(db_column='completedDatetime')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'lifts_tasks'


class Priority(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'priority'


class ServicesTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    key_name = models.CharField(db_column='keyName', max_length=10)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'services_types'


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
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


class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    process_type = models.ForeignKey(ProcessType, on_delete=models.DO_NOTHING, db_column='processTypeId')
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255)
    status = models.ForeignKey(ProcessTypeStatus, related_name='wo_current_status', on_delete=models.DO_NOTHING,
                               db_column='statusId')
    next_status = models.ForeignKey(ProcessTypeStatus, related_name='wo_next_status', on_delete=models.DO_NOTHING,
                                    db_column='nextStatus')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workflows'


class WorkflowEvent(models.Model):
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


class WorkorderLift(models.Model):
    id = models.AutoField(primary_key=True)
    lift = models.ForeignKey(Lift, on_delete=models.DO_NOTHING, db_column='liftId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, db_column='taskId')
    notes = models.CharField(max_length=255, blank=True, null=True)
    started_datetime = models.DateTimeField(db_column='startedDatetime', blank=True, null=True)
    completed_datetime = models.DateTimeField(db_column='completedDatetime', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workorders_lifts'


class Workorder(models.Model):
    id = models.AutoField(primary_key=True)
    workorder_lifts = models.ManyToManyField(WorkorderLift)
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
    is_closed = models.BooleanField(default=False, db_column='isClosed')
    jha_items = models.ManyToManyField(JhaItem)

    class Meta:
        managed = True
        db_table = 'workorders'


class ClosedWorkorder(models.Model):
    id = models.AutoField(primary_key=True)
    workorder_lifts = models.ManyToManyField(WorkorderLift)
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


class Callout(models.Model):
    id = models.AutoField(primary_key=True)
    is_printed = models.IntegerField(db_column='isPrinted', blank=True, null=True)
    technician_fault = models.ForeignKey(Fault, on_delete=models.DO_NOTHING, db_column='technicianFaultId', blank=True,
                                         null=True)
    priority = models.ForeignKey(Priority, on_delete=models.DO_NOTHING, db_column='priorityId', blank=True, null=True)
    florNumber = models.CharField(db_column='floorNo', max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    part_description = models.CharField(db_column='partDescription', max_length=255, blank=True, null=True)
    correction = models.ForeignKey(Correction, models.DO_NOTHING, db_column='correctionId')
    attributable_id = models.IntegerField(db_column='attributableId', blank=True, null=True)
    tech_description = models.CharField(db_column='techDescription', max_length=255, blank=True, null=True)
    workorder = models.OneToOneField(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId', blank=True,
                                     null=True)
    docket_number = models.CharField(db_column='docketNumber', max_length=255, blank=True, null=True)
    callout_time = models.DateTimeField(db_column='calloutTime', blank=True, null=True)
    time_arrival = models.DateTimeField(db_column='timeArrival', blank=True, null=True)
    rectification_time = models.DateTimeField(db_column='rectificationTime', blank=True, null=True)
    time_departure = models.DateTimeField(db_column='timeDeparture', blank=True, null=True)
    chargeable_id = models.IntegerField(db_column='chargeableId', blank=True, null=True)
    technician_signature = models.CharField(db_column='technicianSignature', max_length=255, blank=True, null=True)
    customer_signature = models.CharField(db_column='customerSignature', max_length=255, blank=True, null=True)
    accepted_id = models.IntegerField(db_column='acceptedId', blank=True, null=True)
    notify_email = models.CharField(db_column='notifyEmail', max_length=50, blank=True, null=True)
    verify = models.CharField(max_length=255, blank=True, null=True)
    reported_customer = models.CharField(db_column='reportedCustomer', max_length=255, blank=True, null=True)
    photo_name = models.CharField(db_column='photoName', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'callouts'


class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=8000)

    class Meta:
        managed = True
        db_table = 'notes'


class WorkordersHistory(models.Model):
    id = models.AutoField(primary_key=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    change_type_id = models.IntegerField(db_column='changeTypeId')
    value = models.CharField(max_length=4000)
    user_id = models.IntegerField(db_column='userId', unique=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column='projectId')

    class Meta:
        managed = True
        db_table = 'workorders_history'


class PartRequest(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(db_column='quantity')
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, db_column='partId')
    description = models.CharField(max_length=4000, blank=True, null=True)
    reason_chargeable = models.CharField(db_column='reasonChargeable', max_length=4000, blank=True, null=True)
    workorder = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING, db_column='workorderId')
    remark = models.CharField(max_length=512, blank=True, null=True)
    project = models.IntegerField(db_column='projectId')
    status = models.ForeignKey(ProcessTypeStatus, on_delete=models.DO_NOTHING, db_column='statusId')

    class Meta:
        managed = True
        db_table = 'parts_requests'


class WorkorderPosition(models.Model):
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
