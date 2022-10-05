# app.py
from __future__ import print_function
from flask import Flask, jsonify, request
import json
import os
import requests
import logging
import sys
from qualtrics_api_base import QualtricsAPIBase
from mailing_lists import MailingLists

from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["POST"])
def updateContact():
    print (os.environ.get('Q_USERNAME'))
    contactId = request.json.get('contactId')
    panelId = request.json.get('panelId')
    surveyId = request.json.get('surveyId')
    responseId = request.json.get('responseId')
    # if not contactId or not panelId or not surveyId or not responseId:
    #     return jsonify({'error': 'Mandatory Field Missing'}), 400
    
    input = ['contactId','panelId','surveyId','responseId']
    for item in input:
        if item in request.json:
            pass
        else: 
            return jsonify({'error': "mandatory field "+item+" missing"}), 400
    res_survey=get_response(surveyId,responseId) 
    # https://co1.qualtrics.com/API/v3/mailinglists/ML_3eApjotf3POCy9v/contacts/MLRP_2sLR9oTNp08rBvD
    # https://co1.qualtrics.com/API/v3/mailinglists/ML_3eApjotf3POCy9v/contacts/MLRP_2sLR9oTNp08rBvD
    if 'Error' in res_survey:
        return jsonify({'error': "Get survey failed, please check API Token and Survey details"}), 400
    else:
        embedded_data=res_survey
        mailing_lists_client = MailingLists(os.environ.get('Q_API_TOKEN'), os.environ.get('DATA_CENTER'))
        contact=mailing_lists_client.update_contact(panelId,contactId,embedded_data)
    return jsonify(contact)

def get_response(surveyId,responseId):
    base_url = ''
    payload = {'Request': 'getLegacyResponseData',
                'User': os.environ.get('Q_USERNAME'),
                'Token': os.environ.get('Q_API_TOKEN'),
                'Format': 'JSON',
                'Version': '2.3',
                'SurveyID': surveyId,
                'Labels': '1',
                'ResponseID': responseId

             }
    r = requests.post(base_url, data = payload)
    if r.ok:
        http_response = r.json()
        responses = {}
        for response_id, response in http_response.items():
            # replace # with _ and ~ with _
            reps = {'#':'_', '~':'_'}
            for k, value in response.items():
                if k.startswith('Q'):
                    key = replace_all(k, reps)
                    value=str(value)
                    responses[key] = response.pop(k)
                    responses[key] = value 
        dictionaryToJson = json.dumps(responses)
        survey_response=json.loads(dictionaryToJson)
    else:
        survey_response={"Error":"failed"}
    return survey_response

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


