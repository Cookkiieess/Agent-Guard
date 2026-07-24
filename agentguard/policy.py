import yaml

def load_policy(file_path):

    config = yaml.safe_load(open(file_path, 'r'))
    def_val = config.pop("default")
    return config,def_val

def get_action(policy_data, label):
    if label in policy_data[0]:
        return policy_data[0][label]
    else:
        return policy_data[1]
    