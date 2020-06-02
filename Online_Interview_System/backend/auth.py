import datetime

from django.utils.translation import ugettext_lazy
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING

# request header message
def get_authorization_header(request):
	auth = request.META.get('HTTP_AUTHORIZATION', b'')
	if isinstance(auth, type('')):
		auth = auth.ecnode(HTTP_HEADER_ENCODING)
	return auth
# self-defined auth way
class ExpiringTokenAuthentication(BaseAuthentication):
	model = Token

	def authenticate(self, request):
		auth = get_authorization_header(request)
		if not auth:
			return None

		try:
			token = auth.decode()
		except UnicodeError:
			msg = ugettext_lazy("Invalid token, invalid characters included in token header")
			raise exceptions.AuthenticationFailed(msg)
		return self.authenticate_credentials(token)

	def authenticate_credentials(self, key):
		# get user msg from cache
		token_cache = 'token_' + key
		cache_user = cache.get(token_cache)
		if cache_user:
			return cache_user, cache_user

		try:
			token = self.model.objects.get(key=key)
		except self.model.DoesNotExist:
			raise exceptions.AuthenticationFailed("Authentication Failed")

		if not token.user.is_active:
			raise exceptions.AuthenticationFailed("User banned")

		if(datetime.datetime.now() - token.created) > datetime.timedelta(hours=0.3*1):
			raise exceptions.AuthenticationFailed("Auth-msg pass due")

		if token:
			token_cache = 'token_' + key
			cache.set(token_cache, token.user, 600)

		return token.user, token

	def authenticate_header(self, request):
		return 'Token'




