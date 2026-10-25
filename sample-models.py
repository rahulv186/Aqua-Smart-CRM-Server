# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adminrefreshtoken(models.Model):
    id = models.UUIDField(primary_key=True)
    adminid = models.ForeignKey('Platformadmin', models.DO_NOTHING, db_column='adminId')  # Field name made lowercase.
    familyid = models.UUIDField(db_column='familyId')  # Field name made lowercase.
    tokenhash = models.TextField(db_column='tokenHash', unique=True)  # Field name made lowercase.
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    revokedat = models.DateTimeField(db_column='revokedAt', blank=True, null=True)  # Field name made lowercase.
    replacedbytokenid = models.UUIDField(db_column='replacedByTokenId', blank=True, null=True)  # Field name made lowercase.
    lastusedat = models.DateTimeField(db_column='lastUsedAt', blank=True, null=True)  # Field name made lowercase.
    useragent = models.TextField(db_column='userAgent', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.TextField(db_column='ipAddress', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AdminRefreshToken'


class Amccontract(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    assetid = models.ForeignKey('Asset', models.DO_NOTHING, db_column='assetId', blank=True, null=True)  # Field name made lowercase.
    contractnumber = models.TextField(db_column='contractNumber')  # Field name made lowercase.
    title = models.TextField()
    status = models.TextField()  # This field type is a guess.
    startsat = models.DateTimeField(db_column='startsAt')  # Field name made lowercase.
    endsat = models.DateTimeField(db_column='endsAt')  # Field name made lowercase.
    visitcount = models.IntegerField(db_column='visitCount')  # Field name made lowercase.
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.TextField()
    terms = models.TextField(blank=True, null=True)
    renewedfromid = models.ForeignKey('self', models.DO_NOTHING, db_column='renewedFromId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AmcContract'
        unique_together = (('companyid', 'contractnumber'),)


class Amcvisit(models.Model):
    id = models.UUIDField(primary_key=True)
    contractid = models.ForeignKey(Amccontract, models.DO_NOTHING, db_column='contractId')  # Field name made lowercase.
    jobid = models.OneToOneField('Servicejob', models.DO_NOTHING, db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    dueat = models.DateTimeField(db_column='dueAt')  # Field name made lowercase.
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AmcVisit'


class Asset(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    assetcode = models.TextField(db_column='assetCode', blank=True, null=True)  # Field name made lowercase.
    brand = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    serialnumber = models.TextField(db_column='serialNumber', blank=True, null=True)  # Field name made lowercase.
    producttype = models.TextField(db_column='productType', blank=True, null=True)  # Field name made lowercase.
    installedat = models.DateTimeField(db_column='installedAt', blank=True, null=True)  # Field name made lowercase.
    warrantyendsat = models.DateTimeField(db_column='warrantyEndsAt', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    notes = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Asset'
        unique_together = (('companyid', 'assetcode'),)


class Auditlog(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId', blank=True, null=True)  # Field name made lowercase.
    actorid = models.ForeignKey('User', models.DO_NOTHING, db_column='actorId', blank=True, null=True)  # Field name made lowercase.
    actoradminid = models.ForeignKey('Platformadmin', models.DO_NOTHING, db_column='actorAdminId', blank=True, null=True)  # Field name made lowercase.
    action = models.TextField()
    entitytype = models.TextField(db_column='entityType')  # Field name made lowercase.
    entityid = models.TextField(db_column='entityId', blank=True, null=True)  # Field name made lowercase.
    metadata = models.JSONField(blank=True, null=True)
    ipaddress = models.TextField(db_column='ipAddress', blank=True, null=True)  # Field name made lowercase.
    useragent = models.TextField(db_column='userAgent', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AuditLog'


class Complaint(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    assetid = models.ForeignKey(Asset, models.DO_NOTHING, db_column='assetId', blank=True, null=True)  # Field name made lowercase.
    linkedjobid = models.ForeignKey('Servicejob', models.DO_NOTHING, db_column='linkedJobId', blank=True, null=True)  # Field name made lowercase.
    managerid = models.ForeignKey('Manager', models.DO_NOTHING, db_column='managerId', blank=True, null=True)  # Field name made lowercase.
    complaintnumber = models.TextField(db_column='complaintNumber')  # Field name made lowercase.
    title = models.TextField()
    description = models.TextField()
    priority = models.TextField()  # This field type is a guess.
    status = models.TextField()  # This field type is a guess.
    resolution = models.TextField(blank=True, null=True)
    createdbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    resolvedat = models.DateTimeField(db_column='resolvedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Complaint'
        unique_together = (('companyid', 'complaintnumber'),)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    customercode = models.TextField(db_column='customerCode', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField()
    phone = models.TextField()
    alternatephone = models.TextField(db_column='alternatePhone', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(blank=True, null=True)
    addressline1 = models.TextField(db_column='addressLine1', blank=True, null=True)  # Field name made lowercase.
    addressline2 = models.TextField(db_column='addressLine2', blank=True, null=True)  # Field name made lowercase.
    area = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    postalcode = models.TextField(db_column='postalCode', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    archivedat = models.DateTimeField(db_column='archivedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Customer'
        unique_together = (('companyid', 'customercode'),)


class Fileobject(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerId', blank=True, null=True)  # Field name made lowercase.
    assetid = models.ForeignKey(Asset, models.DO_NOTHING, db_column='assetId', blank=True, null=True)  # Field name made lowercase.
    jobid = models.ForeignKey('Servicejob', models.DO_NOTHING, db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    uploadedbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='uploadedById', blank=True, null=True)  # Field name made lowercase.
    category = models.TextField()  # This field type is a guess.
    storagebucket = models.TextField(db_column='storageBucket')  # Field name made lowercase.
    storagepath = models.TextField(db_column='storagePath')  # Field name made lowercase.
    originalname = models.TextField(db_column='originalName')  # Field name made lowercase.
    mimetype = models.TextField(db_column='mimeType')  # Field name made lowercase.
    sizebytes = models.BigIntegerField(db_column='sizeBytes')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FileObject'
        unique_together = (('storagebucket', 'storagepath'),)


class Inventoryitem(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    sku = models.TextField(blank=True, null=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    unit = models.TextField()
    reorderlevel = models.DecimalField(db_column='reorderLevel', max_digits=12, decimal_places=3)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InventoryItem'
        unique_together = (('companyid', 'sku'),)


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    role = models.TextField()  # This field type is a guess.
    tokenhash = models.TextField(db_column='tokenHash', unique=True)  # Field name made lowercase.
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    acceptedat = models.DateTimeField(db_column='acceptedAt', blank=True, null=True)  # Field name made lowercase.
    revokedat = models.DateTimeField(db_column='revokedAt', blank=True, null=True)  # Field name made lowercase.
    invitedbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='invitedById', related_name='invitation_invitedbyid_set', blank=True, null=True)  # Field name made lowercase.
    invitedbyadminid = models.ForeignKey('Platformadmin', models.DO_NOTHING, db_column='invitedByAdminId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Invitation'


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    servicejobid = models.ForeignKey('Servicejob', models.DO_NOTHING, db_column='serviceJobId', blank=True, null=True)  # Field name made lowercase.
    invoicenumber = models.TextField(db_column='invoiceNumber')  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    issuedate = models.DateTimeField(db_column='issuedAt', blank=True, null=True)  # Field name made lowercase.
    dueat = models.DateTimeField(db_column='dueAt', blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    taxamount = models.DecimalField(db_column='taxAmount', max_digits=12, decimal_places=2)  # Field name made lowercase.
    discountamount = models.DecimalField(db_column='discountAmount', max_digits=12, decimal_places=2)  # Field name made lowercase.
    totalamount = models.DecimalField(db_column='totalAmount', max_digits=12, decimal_places=2)  # Field name made lowercase.
    currency = models.TextField()
    notes = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Invoice'
        unique_together = (('companyid', 'invoicenumber'),)


class Invoiceline(models.Model):
    id = models.UUIDField(primary_key=True)
    invoiceid = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='invoiceId')  # Field name made lowercase.
    itemid = models.ForeignKey(Inventoryitem, models.DO_NOTHING, db_column='itemId', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField()
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unitprice = models.DecimalField(db_column='unitPrice', max_digits=12, decimal_places=2)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='taxRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    linetotal = models.DecimalField(db_column='lineTotal', max_digits=12, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InvoiceLine'


class Jobassignment(models.Model):
    id = models.UUIDField(primary_key=True)
    jobid = models.ForeignKey('Servicejob', models.DO_NOTHING, db_column='jobId')  # Field name made lowercase.
    technicianid = models.ForeignKey('Technician', models.DO_NOTHING, db_column='technicianId')  # Field name made lowercase.
    assignedbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='assignedById', blank=True, null=True)  # Field name made lowercase.
    assignedat = models.DateTimeField(db_column='assignedAt')  # Field name made lowercase.
    unassignedat = models.DateTimeField(db_column='unassignedAt', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'JobAssignment'


class Jobcard(models.Model):
    id = models.UUIDField(primary_key=True)
    jobid = models.OneToOneField('Servicejob', models.DO_NOTHING, db_column='jobId')  # Field name made lowercase.
    workperformed = models.TextField(db_column='workPerformed', blank=True, null=True)  # Field name made lowercase.
    techniciannotes = models.TextField(db_column='technicianNotes', blank=True, null=True)  # Field name made lowercase.
    checklist = models.JSONField(blank=True, null=True)
    customerfeedback = models.TextField(db_column='customerFeedback', blank=True, null=True)  # Field name made lowercase.
    customerrating = models.IntegerField(db_column='customerRating', blank=True, null=True)  # Field name made lowercase.
    signaturefileid = models.TextField(db_column='signatureFileId', blank=True, null=True)  # Field name made lowercase.
    customersignedat = models.DateTimeField(db_column='customerSignedAt', blank=True, null=True)  # Field name made lowercase.
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JobCard'


class Jobstatusevent(models.Model):
    id = models.UUIDField(primary_key=True)
    jobid = models.ForeignKey('Servicejob', models.DO_NOTHING, db_column='jobId')  # Field name made lowercase.
    fromstatus = models.TextField(db_column='fromStatus', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tostatus = models.TextField(db_column='toStatus')  # Field name made lowercase. This field type is a guess.
    note = models.TextField(blank=True, null=True)
    changedbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='changedById', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JobStatusEvent'


class Manager(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    employeecode = models.TextField(db_column='employeeCode', blank=True, null=True)  # Field name made lowercase.
    department = models.TextField(blank=True, null=True)
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Manager'
        unique_together = (('companyid', 'employeecode'),)


class Company(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    slug = models.TextField(unique=True)
    phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    gstin = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    postalcode = models.TextField(db_column='postalCode', blank=True, null=True)  # Field name made lowercase.
    timezone = models.TextField()
    currency = models.TextField()
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    joincode = models.TextField(db_column='joinCode', unique=True, blank=True, null=True)  # Field name made lowercase.
    allowcustomerselfregistration = models.BooleanField(db_column='allowCustomerSelfRegistration')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Company'


class Companyowner(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.OneToOneField(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CompanyOwner'


class Otpchallenge(models.Model):
    id = models.UUIDField(primary_key=True)
    phone = models.TextField()
    purpose = models.TextField()  # This field type is a guess.
    codehash = models.TextField(db_column='codeHash')  # Field name made lowercase.
    attempts = models.IntegerField()
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    consumedat = models.DateTimeField(db_column='consumedAt', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.TextField(db_column='ipAddress', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OtpChallenge'


class Passwordresettoken(models.Model):
    id = models.UUIDField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    tokenhash = models.TextField(db_column='tokenHash', unique=True)  # Field name made lowercase.
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    usedat = models.DateTimeField(db_column='usedAt', blank=True, null=True)  # Field name made lowercase.
    requestedip = models.TextField(db_column='requestedIp', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PasswordResetToken'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerId', blank=True, null=True)  # Field name made lowercase.
    invoiceid = models.ForeignKey(Invoice, models.DO_NOTHING, db_column='invoiceId', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.TextField()  # This field type is a guess.
    reference = models.TextField(blank=True, null=True)
    receivedat = models.DateTimeField(db_column='receivedAt')  # Field name made lowercase.
    notes = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Payment'


class Platformadmin(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(unique=True)
    passwordhash = models.TextField(db_column='passwordHash')  # Field name made lowercase.
    fullname = models.TextField(db_column='fullName', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    mfasecretencrypted = models.TextField(db_column='mfaSecretEncrypted', blank=True, null=True)  # Field name made lowercase.
    mfaenabledat = models.DateTimeField(db_column='mfaEnabledAt', blank=True, null=True)  # Field name made lowercase.
    failedloginattempts = models.IntegerField(db_column='failedLoginAttempts')  # Field name made lowercase.
    lockeduntil = models.DateTimeField(db_column='lockedUntil', blank=True, null=True)  # Field name made lowercase.
    lastloginat = models.DateTimeField(db_column='lastLoginAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PlatformAdmin'


class Refreshtoken(models.Model):
    id = models.UUIDField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    familyid = models.UUIDField(db_column='familyId')  # Field name made lowercase.
    tokenhash = models.TextField(db_column='tokenHash', unique=True)  # Field name made lowercase.
    expiresat = models.DateTimeField(db_column='expiresAt')  # Field name made lowercase.
    revokedat = models.DateTimeField(db_column='revokedAt', blank=True, null=True)  # Field name made lowercase.
    replacedbytokenid = models.UUIDField(db_column='replacedByTokenId', blank=True, null=True)  # Field name made lowercase.
    lastusedat = models.DateTimeField(db_column='lastUsedAt', blank=True, null=True)  # Field name made lowercase.
    useragent = models.TextField(db_column='userAgent', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.TextField(db_column='ipAddress', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RefreshToken'


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    entitytype = models.TextField(db_column='entityType')  # Field name made lowercase.
    entityid = models.TextField(db_column='entityId')  # Field name made lowercase.
    dueat = models.DateTimeField(db_column='dueAt')  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    sentat = models.DateTimeField(db_column='sentAt', blank=True, null=True)  # Field name made lowercase.
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reminder'


class Servicejob(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    assetid = models.ForeignKey(Asset, models.DO_NOTHING, db_column='assetId', blank=True, null=True)  # Field name made lowercase.
    jobnumber = models.TextField(db_column='jobNumber')  # Field name made lowercase.
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    servicetype = models.TextField(db_column='serviceType')  # Field name made lowercase.
    priority = models.TextField()  # This field type is a guess.
    status = models.TextField()  # This field type is a guess.
    scheduledat = models.DateTimeField(db_column='scheduledAt', blank=True, null=True)  # Field name made lowercase.
    startedat = models.DateTimeField(db_column='startedAt', blank=True, null=True)  # Field name made lowercase.
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)  # Field name made lowercase.
    reportedissue = models.TextField(db_column='reportedIssue', blank=True, null=True)  # Field name made lowercase.
    resolution = models.TextField(blank=True, null=True)
    createdbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServiceJob'
        unique_together = (('companyid', 'jobnumber'),)


class Stockmovement(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    itemid = models.ForeignKey(Inventoryitem, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    jobid = models.ForeignKey(Servicejob, models.DO_NOTHING, db_column='jobId', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.ForeignKey('User', models.DO_NOTHING, db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    movementtype = models.TextField(db_column='movementType')  # Field name made lowercase. This field type is a guess.
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unitcost = models.DecimalField(db_column='unitCost', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StockMovement'


class Technician(models.Model):
    id = models.UUIDField(primary_key=True)
    companyid = models.ForeignKey(Company, models.DO_NOTHING, db_column='companyId')  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    employeecode = models.TextField(db_column='employeeCode', blank=True, null=True)  # Field name made lowercase.
    emergencycontact = models.TextField(db_column='emergencyContact', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    alternatephone = models.TextField(db_column='alternatePhone', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(blank=True, null=True)
    designation = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # This field type is a guess.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    hiredat = models.DateTimeField(db_column='hiredAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Technician'
        unique_together = (('companyid', 'employeecode'),)


class User(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.TextField(unique=True, blank=True, null=True)
    phone = models.TextField(unique=True, blank=True, null=True)
    passwordhash = models.TextField(db_column='passwordHash', blank=True, null=True)  # Field name made lowercase.
    fullname = models.TextField(db_column='fullName', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    emailverifiedat = models.DateTimeField(db_column='emailVerifiedAt', blank=True, null=True)  # Field name made lowercase.
    phoneverifiedat = models.DateTimeField(db_column='phoneVerifiedAt', blank=True, null=True)  # Field name made lowercase.
    failedloginattempts = models.IntegerField(db_column='failedLoginAttempts')  # Field name made lowercase.
    lockeduntil = models.DateTimeField(db_column='lockedUntil', blank=True, null=True)  # Field name made lowercase.
    passwordchangedat = models.DateTimeField(db_column='passwordChangedAt', blank=True, null=True)  # Field name made lowercase.
    mustchangepassword = models.BooleanField(db_column='mustChangePassword')  # Field name made lowercase.
    lastloginat = models.DateTimeField(db_column='lastLoginAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'