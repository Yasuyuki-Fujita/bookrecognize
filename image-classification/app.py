import boto3
import base64
import json
import numpy as np
import logging
import traceback,sys
from chalice import Chalice
 
app = Chalice(app_name='image-classification')
app.debug = True
 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
 
@app.route('/classification', methods=['POST'], content_types=['application/octet-stream'], cors=True)
def classification():
 
    try:
        body_data = app.current_request.raw_body
        body_data = body_data.split(b'base64,')
 
        image = base64.b64decode(body_data[1])
 
        sagemaker_client = boto3.client(service_name='sagemaker-runtime', region_name='xxxxxxxx')
 
        logger.info('Invoke Endpoint')
        res = sagemaker_client.invoke_endpoint(
                        EndpointName='sagemaker-imageclassification-notebook-ep-xxxxxxxxxxx',
                        ContentType='application/x-image',
                        Body = image
                    )
 
        result = res['Body'].read()
        result = json.loads(result)
 
        # the result will output the probabilities for all classes
        object_categories = ['ISBN479804573X', 'ISBN4537256109', 'ISBN4839964564']
 
        out = ''
        index = np.argsort(result)
        for i in index[::-1]:
            out += '{} / [probability] {:.2%},'.format(object_categories[i], result[i])
            if result[i] < 0.1:
                break
 
        return out[:-1]
 
    except Exception as e:
        tb = sys.exc_info()[2]
        return 'error:{0}'.format(e.with_traceback(tb))
 
@app.route('/rekognition', methods=['POST'], content_types=['application/octet-stream'], cors=True)
def rekognition():
 
    try:
        body_data = app.current_request.raw_body
        body_data = body_data.split(b'base64,')
 
        image = base64.b64decode(body_data[1])
 
        rekognition_client = boto3.client(service_name='rekognition', region_name='xxxxxx')
 
        logger.info('Invoke Rekognition')
        res = rekognition_client.detect_labels(
                        Image = { 'Bytes': image },
                        MaxLabels=5,
                        MinConfidence=10
                    )
 
        translate_client = boto3.client(service_name='translate', region_name='xxxxx')
        out = ''
        for label in res['Labels'] :
            trans = translate_client.translate_text(Text=label['Name'], 
                        SourceLanguageCode='en', TargetLanguageCode='ja')
 
            out += '[en] {} / [ja] {} / [Confidence] {:.2f}%,'.format(
                        label['Name'], trans.get('TranslatedText'), label['Confidence']
                    )
 
        return out[:-1]
 
    except Exception as e:
        tb = sys.exc_info()[2]
        return 'error:{0}'.format(e.with_traceback(tb))