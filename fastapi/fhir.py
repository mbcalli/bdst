from dataclasses import dataclass
from datetime import datetime

@dataclass
class Identifier:
	# usual | official | temp | secondary (If known)
	use: str = None
	# The namespace for the identifier value
	system: str = None
	# The value that is unique
	value: str = None
	# The period during which the identifier is/was valid for use
	period: datetime = None
	# Organization that issued/manages the identifier
	assigner: str = None

@dataclass
class HumanName:
	# usual | official | temp | nickname | anonymous | old | maiden
	use: str = None
	# Text representation of the full name
	text: str = None
	# Family name (often called 'Surname')
	family: str = None
	# Given names (not always 'first'). Includes middle names
	given: str = None
	# Parts that come before the name
	prefix: str = None
	# Parts that come after the name
	suffix: str = None
	# Time period when name was/is in use
	period: datetime = datetime.today()


@dataclass
class ContactPoint:
	# phone | fax | email | pager | url | sms | other
	system: str = None
	# The actual contact point details
	value: str = None
	# home | work | temp | old - purpose of this contact point
	use: str = None
	# Specify preferred order of use (1 = highest)
	rank: int = 1
	# Time period when the contact point was/is in use
	period: datetime = datetime.today()

@dataclass
class Address:
	# home | work | temp | old - purpose of this address
	use: str = None
	# postal | physical | both
	type: str = None
	# Text representation of the address
	text: str = None
	# Street name, number, direction & P.O. Box etc.
	line: str = None
	# Name of city, town etc.
	city: str = None
	# District name (aka county)
	district: str = None
	# Sub-unit of country (abbreviations ok)
	state: str = None
	# Postal code for area
	postalCode: str = None
	# Country (can be ISO 3166 3 letter code)
	country: str = None
	# Time period when address was/is in use
	period: datetime = datetime.today()

@dataclass
class CodeableConcept:
	# Code defined by a terminology system
	coding: str = None
	# Plain text representation of the concept
	text: str = None

@dataclass
class Attachment:
	# Mime type of the content, with charset etc.
	contentType: str = None
	# Human language of the content (BCP-47)
	language: str = None
	# Data inline, base64ed
	data: str = None
	# Uri where the data can be found
	uri: str = None
	# Number of bytes of content (if url provided)
	size: int = None
	# Hash of the data (sha-1, base64ed)
	hash: str = None
	# Label to display in place of the data
	title: str = None
	# Date attachment was first created
	creation: datetime = datetime.today()

class Contact:

	def __init__(self, relationship: CodeableConcept = {}, name: HumanName = {}, telecom: ContactPoint = {}, address: Address = {}, gender: str = None, organization: str = None, period: datetime = datetime.today()):
		self.relationship = CodeableConcept(**relationship)
		self.name = HumanName(**name)
		self.telecom = ContactPoint(**telecom)
		self.address = Address(**address)
		self.gender = gender
		self.organization = organization
		self.period = period

@dataclass
class Communication:

	def __init__(self, language: CodeableConcept = {}, preferred: bool = True):
		self.language = CodeableConcept(**language)
		self.preferred = preferred


@dataclass
class Link:
	# The other patient resource that the link refers to
	other: str = None
	# replace | refer | seealso - type of link
	type: str = None

@dataclass
class Deceased:
	deceasedBoolean: bool = False
	deceasedDateTime: datetime = None

@dataclass
class MultipleBirth:
	multipleBirthBoolean: bool = False
	multipleBirthInteger: int = 0


class Patient:


	def __init__(self, identifier = {}, active = True, name = {}, telecom = {}, gender = None, birthDate = None, deceased = {}, address = {}, maritalStatus = {}, multipleBirth = {}, photo = {}, contact = {}, communication = {}, generalPractitioner = None, managingOrganization = None, link = {}):
		self.identifier = Identifier(**identifier)
		self.active = active
		self.name = HumanName(**name)
		self.telecom = ContactPoint(**telecom)
		self.gender = gender
		self.birthDate = birthDate
		self.deceased = Deceased(**deceased)
		self.address = Address(**address)
		self.maritalStatus = CodeableConcept(**maritalStatus)
		self.multipleBirth = MultipleBirth(**multipleBirth)
		self.photo = Attachment(**photo)
		self.contact = Contact(**contact)
		self.communication = Communication(**communication)
		self.generalPractitioner = generalPractitioner
		self.managingOrganization = managingOrganization
		self.link = Link(**link)

	
	def get_dictionary(self):
		return self.__dict__




class Condition:

	def __init__(self, identifier={}, clinicalStatus = {}, verificationStatus = {}, category = {}, severity = {}, code = {}, bodySite = {}, onsetDateTime = None, onsetAge = None, onsetPeriod = None, onsetRange = None, onsetString = None, abatementDateTime = None, abatementAge = None, abatementBoolean = None, abatementPeriod = None, abatementRange = None, abatementString = None, recordedDate = None, recorder = None, asserter = None):
		self.identifier = Identifier(**identifier)
		self.clinicalStatus = CodeableConcept(**clinicalStatus)
		self.verificationStatus = CodeableConcept(**verificationStatus)
		self.category = CodeableConcept(**category)
		self.severity = CodeableConcept(**severity)
		self.code = CodeableConcept(**code)
		self.bodySite = CodeableConcept(**bodySite)
		self.subject = None
		self.onsetDateTime = onsetDateTime
		self.onsetAge = onsetAge
		self.onsetPeriod = onsetPeriod
		self.onsetRange = onsetRange
		self.onsetString = onsetString
		self.abatementDateTime = abatementDateTime
		self.abatementAge = abatementAge
		self.abatementBoolean = abatementBoolean
		self.abatementPeriod = abatementPeriod
		self.abatementRange = abatementRange
		self.abatementString = abatementString
		self.recordedDate = recordedDate
		self.recorder = recorder
		self.asserter = asserter
  
class Observation:
        
        def __init__(self, identifier={}, basedOn = None, partOf = None, status = None, category = {}, code = {}, subject = None, focus = None, encounter = None, effectiveDateTime = None, effectivePeriod = None, effectiveTiming = None, effectiveInstant = None, issued = None, performer = None, valueQuantity = None, valueCodeableConcept = {}, valueString = None, valueBoolean = None, valueInteger = None, valueRange = None, valueRatio = None, valueSampledData = None, valueTime = None, valueDateTime = None, valuePeriod = None, dataAbsentReason = {}, interpretation = {}, note = None, bodySite = {}, method = {}, specimen = None, device = None, referenceRange=None, hasMember = None, derivedFrom = None, component = None):
                self.identifier = Identifier(**identifier)
                self.basedOn = basedOn
                self.partOf = partOf
                self.status = status
                self.category = CodeableConcept(**category)
                self.code = CodeableConcept(**code)
                self.subject = subject
                self.focus = focus
                self.encounter = encounter
                self.effectiveDateTime = effectiveDateTime
                self.effectivePeriod = effectivePeriod
                self.effectiveTiming = effectiveTiming
                self.effectiveInstant = effectiveInstant
                self.issued = issued
                self.performer = performer
                self.valueQuantity = valueQuantity
                self.valueCodeableConcept = CodeableConcept(**valueCodeableConcept)
                self.valueString = valueString
                self.valueBoolean = valueBoolean
                self.valueInteger = valueInteger
                self.valueRange = valueRange
                self.valueRatio = valueRatio
                self.valueSampledData = valueSampledData
                self.valueTime = valueTime
                self.valueDateTime = valueDateTime
                self.valuePeriod = valuePeriod
                self.dataAbsentReason = CodeableConcept(**dataAbsentReason)
                self.interpretation = CodeableConcept(**interpretation)
                self.note = note
                self.bodySite = CodeableConcept(**bodySite)
                self.method = CodeableConcept(**method)
                self.specimen = specimen
                self.device = device
                self.referenceRange = referenceRange
                self.hasMember = hasMember
                self.derivedFrom = derivedFrom
                self.component = component