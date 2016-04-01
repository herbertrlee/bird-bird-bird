import base64
import logging

import httplib2

from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


def get_vision_service():
    API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform']
    )

    credentials.authorize(http)

    return build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)


def is_it_a_bird(image_bytes):
    vision_service = get_vision_service()

    image_content = base64.b64encode(image_bytes)

    service_request = vision_service.images().annotate(
        body={
            'requests': [{
                'image': {
                    'content': image_content
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10,
                }]
            }]
        })

    response = service_request.execute()

    try:
        descriptions = [label_annotation["description"] for label_annotation in response["responses"][0]['labelAnnotations']]
        logging.info("descriptions: %s" % ", ".join(descriptions))

        return "bird" in descriptions
    except Exception:
        return False
