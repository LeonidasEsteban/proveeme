from django import template

register = template.Library()

@register.simple_tag
def active(req, pattern):
	import re
	if pattern == req.path:
		return 'active'

	return ''
