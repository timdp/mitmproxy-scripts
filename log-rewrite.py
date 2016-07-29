from lib.log import log_combined
from lib.rewrite import rewrite

def request(flow):
	log_combined(flow)
	rewrite(flow)
