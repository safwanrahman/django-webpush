

class ValidatePostData(object):


    errors = {}

    def __init__(self, data):
    	self.data = data

    def validate_fields(self):
    	data = self.data
    	all_keys = sorted(['url', 'subscription_info', 'status_type'])
        data_keys = sorted(data.keys())
    	if data_keys != all_keys:
    		for key in all_keys:
    			if key not in data_keys:
    				errors[key] = "This field is required."
    		return False