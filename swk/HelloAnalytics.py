"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/home/ubuntu/myenv/SWKV2/swk/swk-new.json'
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
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()
  #           body={
  #         'reportRequests': [
  #             {
  #                 'viewId': VIEW_ID,
  #                 'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
  #                 'metrics': [
  #                     {'expression': 'ga:pageviews'},
  #                     {'expression': 'ga:uniquePageviews'},
  #                     {'expression': 'ga:timeOnPage'},
  #                     {'expression': 'ga:bounces'},
  #                     {'expression': 'ga:entrances'},
  #                     {'expression': 'ga:exits'}
  #                 ],
  #                 "dimensions": [
  #                     {"name": "ga:pagePath"}
  #                 ],
  #                 "orderBys": [
  #                     {"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"}
  #                 ]
  #             }
  #         ]
  #     }
  # ).execute() 




def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response"""

    for report in response.get('reports', []):

        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
          dimensions = row.get('dimensions', [])
          dateRangeValues = row.get('metrics', [])

        # for header, dimension in zip(dimensionHeaders, dimensions):
          # print(header + ': ' + dimension)
          # print(dimension)

        for i, values in enumerate(dateRangeValues):

          for metricHeader, value in zip(metricHeaders, values.get('values')):
            # print(metricHeader.get('name') + ': ' + value)
            return(value)

def main():
  # print("Hello")
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  # print(response)
  print_response(response)
  

if __name__ == '__main__':
  main()

