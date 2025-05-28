import pykis
from django.conf import settings


key_info = {
	"appkey": settings.KIS_APP_KEY,
	"appsecret": settings.KIS_APP_SECRET
}
account_info = {
	"account_code": settings.KIS_ACCOUNT_CODE,
	"product_code": settings.KIS_ACCOUNT_PRODUCT_CODE
}

domain = pykis.DomainInfo(kind="virtual")

kis = pykis.Api(key_info=key_info, account_info=account_info, domain_info=domain)