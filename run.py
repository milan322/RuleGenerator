#!/usr/bin/python -u
import os
import sys, getopt
import re
import glob
from sys import argv
from flask import *
from json import dumps
from werkzeug import secure_filename
from flask import Flask, redirect, url_for, render_template
from flask import render_template, flash, redirect, session, url_for, request, g
import requests
import datetime
from librules import *
from config import *

app = Flask(__name__)

@app.route('/')
def index():
    #return render_template('index.html', title='Login')
    return render_template('rule.html')

@app.route('/ruleslist', methods=['GET','POST'])
def ruleslist():
    print "getting all rules from json-----\n"
    pattern = request.args.get('pattern')
    print "pattern=",pattern,"\n"
    createfile(rulesfpath)
    ruleMgr = RuleManager()
    rules = ruleMgr.load_rulesjson(rulesfpath)
    #print json.dumps(rules,indent=4)
    rules_json = {}
    rules_list=[]
    for item in rules['rules']:
        if pattern and not re.search(pattern, item['name'],re.IGNORECASE):
            continue
        rules_list.append(item)
    rules_json['rules'] = rules_list
    print json.dumps(rules_json, indent=4)
    return json.dumps(rules_json)

@app.route('/saverule', methods=['GET','POST'])
def saverule():
    print "saving new rule to Json-----\n"
    rule_name = request.args.get('rule_name');
    word = request.args.get('word')
    ruleid = request.args.get('rule_id')
    desc = request.args.get('rule_desc')
    createfile(rulesfpath)
    ruleMgr = RuleManager()
    data = ruleMgr.load_rulesjson(rulesfpath)
    """if not data["rules"]:
        pass
    else:    
        for item in data['rules']:
            if item['name'] == rule_name:
                print "ERROR-rule name already exists!!\n"
                return myerror('Rule name already exists!!!')"""
    if ruleid=="-1":
        data['rules'].append({"name":rule_name,"word":word,"desc":desc})
    else:
        data['rules'][int(ruleid)] = {"name":rule_name,"word":word,"desc":desc}
        
    #with open(rule_file,"w") as outfile:
            #outfile.write(json.dumps(data,indent=4))
    ruleMgr.json_load_output = data
    ruleMgr.save_rule(rulesfpath)
    return myresult()

@app.route('/delrules', methods=['GET','POST'])
def rmrules():
    rulesjson = request.json
    names = [x['rulename'] for x in rulesjson['rules']]
    print "names=",names,"\n\n"
    ruleMgr = RuleManager()
    data = ruleMgr.load_rulesjson(rulesfpath)
    finaldict = {}
    res = list(filter(lambda x: not x['name'] in names, data['rules']))
    finaldict["rules"] = res
    with open(rulesfpath,"w") as outfile:
        outfile.write(json.dumps(finaldict,indent=4))
    return myresult()



def main(args):
    createdir(rulesDir)
    print "Available on the following URLs:"
    for line in mycheck_output(["/sbin/ifconfig"]).split("\n"):
        m = re.match('\s*inet addr:(.*?) .*', line)
        if m:
            print "    http://" + m.group(1) + ":" + str(9000) + "/"
    app.run(
      host ="0.0.0.0",
      port = 9000,
      debug = True,
      use_reloader=False
     )

if __name__ == "__main__":
   main(sys.argv[1:])
