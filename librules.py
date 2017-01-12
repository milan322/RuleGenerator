import os
from os.path import join
import json

rulesDir = "/opt/vedavaapi_grammar/data/settings/"
rulesfpath = join(rulesDir,"rules.json")

def getrules():
    #rules.json file path
    ruleslist={}
    if os.path.exists(rulesfpath):
        with open(rulesfpath) as f:
            ruleslist = json.load(f)
    return json.dumps(ruleslist)

def createfile(rulesfpath):
    if not os.path.exists(rulesfpath):
        try:
            print "Creating file:"+rulesfpath
            with open(rulesfpath,"w") as f:
                f.write(json.dumps({"rules":[]},indent=4))
        except Exception as e:
            print "Not able to create file: ",e


class RuleManager():
    def __init__(self):
        self.rule_names=[]
        self.json_load_output=[]
    def load_rulesjson(self,rule_file):
        #ruleslist={}
        if os.path.exists(rule_file):
            with open(rule_file) as f:
                #ruleslist = json.load(f)
                self.json_load_output=json.load(f)
        return self.json_load_output

    def save_rule(self, rule_file):
        try:
            print "Load_out_put=",self.json_load_output
            with open(rule_file,"w") as outfile:
                outfile.write(json.dumps(self.json_load_output,indent=4))
        except Exception as e:
            print "Error=",e
            return False
        return True
        
    def update_rule(self, rulesdict):
        allrules = self.json_load_output['rules']
        print "allrules=",allrules 
        entry = dict((key, value) for key, value in rulesdict.items() if key != 'id') 
        idx = allrules.index(filter(lambda n: n.get('name') == rulesdict['name'],\
        allrules)[0])
        allrules[idx] = entry

