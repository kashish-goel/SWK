"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os
script_dir = os.path.dirname(__file__)
rel_path = 'swk-new.json'
abs_file_path = os.path.join(script_dir,rel_path)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = abs_file_path
VIEW_ID = '243710477'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    print("in initialise")
    return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
          "reportRequests": [
            {
              "viewId": "243710477",
              "dateRanges": [
                {
                  "startDate": "2020-09-15",
                  "endDate": "yesterday"
                }
              ]
            }
          ]
        }
  ).execute()


def print_response(response):
    totalvalue =0
    """Parses and prints the Analytics Reporting API V4 response.

     Args:
       response: An Analytics Reporting API V4 response.
     """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        totalvalue ="0"

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ', dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range:', str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    totalvalue = int(value) + int(totalvalue)
                    print(metricHeader.get('name') + ':', value)
                    return(totalvalue)
                # print(totalvalue)
                    


def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    print_response(response)


if __name__ == '__main__':
    main()


