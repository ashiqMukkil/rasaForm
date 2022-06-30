import yaml

class YmlParser:
    """
        create/update nlu.yml,domain.yml,stories.yml,rules.yml
    """
    def __init__(self, json_body, is_create=True):
        self.load_config_file()
        (self.existing_nlu_yml,self.existing_domain_yml,
        self.existing_stories_yml,self.existing_rules_yml) = self.load_existing_yml_files()
        self.new_utterance,self.new_intents,self.new_rules = {},[],[]
        self.intent_names_fetched = set(self.existing_domain_yml['intents'])
        self.json_to_yml_parser(json_body)
        self.update_yml_files()

    def load_config_file(self):
        with open(r'config.yml') as config:
            self.config = yaml.full_load(config)
        
    def load_existing_yml_files(self):
        print(self.config['RASA']['DOMAIN_PATH'])
        try:
            with open(self.config['RASA']['DOMAIN_PATH']) as old_domain_yml:
                old_domain_yml = yaml.full_load(old_domain_yml)

            with open(self.config['RASA']['NLU_PATH']) as old_nlu_yml:
                old_nlu_yml = yaml.full_load(old_nlu_yml)

            with open(self.config['RASA']['STORIES_PATH']) as old_stories_yml:
                old_stories_yml = yaml.full_load(old_stories_yml)

            with open(self.config['RASA']['RULES_PATH']) as old_rules_yml:
                old_rules_yml = yaml.full_load(old_rules_yml)  
        except OSError as e:
            print(f"{type(e)}: {e}")

        return (old_nlu_yml,old_domain_yml,old_stories_yml,old_rules_yml)

    def utter_type_redirect(self,response,intent):
        if response['Type'] == 'Button':
            buttons =[]
            for buttonIntent in response['Buttons']:
                self.json_to_yml_parser(buttonIntent['Intent'])
                buttons.append({'title':buttonIntent['ButtonText'],
                                'payload':'/'+buttonIntent['Intent']['IntentName']})
            self.new_utterance.update({
                'utter_'+intent :{
                    'text':response['ButtonHead'],
                    'buttons':buttons
                }
            }) 
            self.new_rules.append({
                'rule':'rule '+intent,
                'steps':{
                    'intent':intent,
                    'action':'utter_'+intent
                }
            }) 
        elif response['Type'] == 'Text':
            self.new_utterance.update({
                'utter_'+intent:{
                    'text':response['Response']
                }
            })  
            self.new_rules.append({
                'rule':'rule '+intent,
                'steps':{
                    'intent':intent,
                    'action':'utter_'+intent
                }
            })                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

    def json_to_yml_parser(self,json_body):
        try:
            self.intent_names_fetched.add(json_body['IntentName'])
            self.new_intents.append({
                'intent':json_body['IntentName'],
                'examples':'- ' + ('\n- '.join(json_body['Examples']))
            })
            self.utter_type_redirect(json_body['Response'],json_body['IntentName'])
            return self.new_intents
        except Exception as e:
            print(e)

    def update_yml_files(self):
        self.existing_domain_yml['intents'] = self.intent_names_fetched
        self.existing_domain_yml['responses'].update(self.new_utterance)
        self.existing_nlu_yml['nlu'].extend(self.new_intents)
        self.existing_rules_yml['rules'].extend(self.new_rules)


    
"""
test data
"""
d = {
    "IntentName":'company details',
    "Examples":[
        'company',
        'about company',
        'details about company'
    ],
    "Response":{
        "Type":"Button",
        "Buttons":[
            {
                "ButtonText":'Career',
                "Intent":{
                    "IntentName":'career',
                    "Examples":[
                        'career'
                    ],
                    "Response":{
                        "Type":"Button",
                        "Buttons":[
                            {
                                "ButtonText":"opening",
                                "Intent":{
                                    "IntentName":'opening',
                                    "Examples":[
                                        'opening'
                                    ],
                                    "Response":{
                                        "Type":"Text",
                                        "Response":"You can contact hr department at hr@domain.com"
                                    }
                                },
                            },
                            {
                                "ButtonText":"details",
                                "Intent":{
                                    "IntentName":'details',
                                    "Examples":[
                                        'opening'
                                    ],
                                    "Response":{
                                        "Type":"Text",
                                        "Response":"You can contact hr department at details@domain.com"
                                    }
                                },
                            }
                        ],
                        "ButtonHead":"Click Any career options below"
                    }
                }
            },
            {
                "ButtonText":'Team',
                "Intent":{
                    "IntentName":'team',
                    "Examples":[
                        'team'
                    ],
                    "Response":{
                        "Type":"Text",
                        "Response":"check team@domain.com"
                    }
                }
            },
            {
                "ButtonText":'About',
                "Intent":{
                    "IntentName":'about',
                    "Examples":[
                        'about'
                    ],
                    "Response":{
                        "Type":"Text",
                        "Response":"check about@domain.com"
                    }
                }
            }
        ],
        "ButtonHead":"Hey! click button bellow"
    }
}

d = YmlParser(d)