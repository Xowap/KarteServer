# -*- coding: utf-8 -*-
from django.db import models

#
# Data types
#

class BlobField(models.Field):
	description = "Blob"

	def db_type(self):
		return 'oid'

#
# Security fields
#

class CryptKey(models.Model):
	email = models.EmailField()
	keyid = models.CharField(max_length = 16)

class SingleCheckRow(models.Model):
	class Meta:
		abstract = True

	key = models.ForeignKey("CryptKey")
	chk_self = models.CharField(max_length = 50) # TODO define this data type

class DoubleCheckRow(SingleCheckRow):
	class Meta:
		abstract = True

	chk_prev = models.CharField(max_length = 50) # TODO define this data type

class Deletable(models.Model):
	class Meta:
		abstract = True

	deleted = models.BooleanField()
#
# Base classes
#

# Définit simplement une promotion
class BaseTl1Promotion(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length = 50)

class BaseTl1Domain(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length = 50)

class BaseUser(models.Model):
	class Meta:
		abstract = True

	firstname = models.CharField(max_length = 50)
	lastname = models.CharField(max_length = 50)
	created_at = models.DateTimeField(auto_now = True)
	email = models.EmailField()
	roles = models.ManyToManyField("Role")
	picture = BlobField()
	tl1_domain = models.ForeignKey("Tl1Domain")
	tl1_user = models.CharField(max_length = 50)
	tl1_promotion = models.ForeignKey("Tl1Promotion")
	adhesion_type = models.IntegerField() # TODO passer en enum
	adhesion_amount = models.FloatField()
	adhesion_date = models.DateTimeField()

class BaseAuthFactor(models.Model):
	class Meta:
		abstract = True

	medium = models.IntegerField() # TODO make this an enum
	account = models.ForeignKey('Account')
	data = models.TextField()

class BaseRole(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length = 50)
	actions = models.ManyToManyField("Action", related_name = '%(class)s_actions')
	checkouts = models.ManyToManyField("Checkout")

# Représente une caisse
class BaseCheckout(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length = 50)
	tls_pubkey = models.TextField() # TODO se renseigner sur les données à vraiment stocker
	ipv4 = models.IPAddressField() # TODO passer en champ générique ipv4/ipv6
	products = models.ManyToManyField('Product')

class BaseAccount(models.Model):
	class Meta:
		abstract = True

	user = models.ForeignKey("User")
	amount = models.IntegerField()
	active = models.BooleanField()

class BaseProduct(models.Model):
	class Meta:
		abstract = True

	name = models.CharField(max_length = 50)
	price = models.IntegerField()
	picture = BlobField(null = True)
	script = models.TextField(null = True)

#
# Real classes
#

class Tl1Promotion(BaseTl1Promotion, Deletable):
	class Meta:
		db_table = 'karte_tl1_promotion'

class Tl1Domain(BaseTl1Domain, Deletable):
	class Meta:
		db_table = 'karte_tl1_domain'

class Role(BaseRole, Deletable):
	pass

class User(BaseUser, Deletable):
	pass

class AuthFactor(BaseAuthFactor, Deletable):
	class Meta:
		db_table = 'karte_auth_factor'

class Account(BaseAccount, Deletable):
	pass

class Checkout(BaseCheckout, Deletable):
	pass

class Product(BaseProduct, Deletable):
	pass

class Action(SingleCheckRow):
	name = models.CharField(max_length = 50)
	slug = models.SlugField()
	description = models.TextField()

class Operation(DoubleCheckRow):
	account = models.ForeignKey(Account)
	checkout = models.ForeignKey(Checkout)
	operator = models.ForeignKey(User)
	date = models.DateTimeField(auto_now = True)
	product = models.ForeignKey('Product', null = True)
	debit = models.IntegerField(null = True)
	credit = models.IntegerField(null = True)

#
# Log Classes
#

class BaseLog(DoubleCheckRow):
	class Meta:
		abstract = True

	operator = models.ForeignKey('User', related_name = '%(class)s_operator')
	date = models.DateTimeField(auto_now = True)
	action = models.ForeignKey(Action)

class UserLog(BaseLog, BaseUser):
	class Meta:
		db_table = 'karte_user_log'
	user_ptr = models.ForeignKey('User', related_name = 'user_ptr')

class AccountLog(BaseLog, BaseAccount):
	class Meta:
		db_table = 'karte_account_log'
	account_ptr = models.ForeignKey('Account', related_name = 'account_ptr')

class AuthFactorLog(BaseLog, BaseAuthFactor):
	class Meta:
		db_table = 'karte_auth_factor_log'
	auth_factor_ptr = models.ForeignKey('AuthFactor', related_name = 'auth_factor_ptr')

class Tl1PromotionLog(BaseLog, BaseTl1Promotion):
	class Meta:
		db_table = 'karte_tl1_promotion_log'
	tl1_promotion_ptr = models.ForeignKey('Tl1Promotion', related_name = 'tl1_promotion_ptr')

class Tl1DomainLog(BaseLog, BaseTl1Domain):
	class Meta:
		db_table = 'karte_tl1_domain_log'
	tl1_domain_ptr = models.ForeignKey('Tl1Domain', related_name = 'tl1_domain_ptr')

class RoleLog(BaseLog, BaseRole):
	class Meta:
		db_table = 'karte_role_log'
	role_ptr = models.ForeignKey('Role', related_name = 'role_ptr')

class CheckoutLog(BaseLog, BaseCheckout):
	class Meta:
		db_table = 'karte_checkout_log'
	checkout_ptr = models.ForeignKey('Checkout', related_name = 'checkout_ptr')

class ProductLog(BaseLog, BaseProduct):
	class Meta:
		db_table = 'karte_product_log'
	product_ptr = models.ForeignKey('Product', related_name = 'product_ptr')
