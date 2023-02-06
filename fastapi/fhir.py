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
	# The language
	language: CodeableConcept = CodeableConcept()
	# Language preference indicator
	preferred: bool = True

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

	def update(self,  **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	def get_dictionary(self):
		return self.__dict__