import os
import sys
from google_ads_helper import get_client
from google.ads.googleads.errors import GoogleAdsException

def main():
    try:
        client = get_client()
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID").replace("-", "")
        ga_service = client.get_service("GoogleAdsService")

        query = """
            SELECT
              campaign.id,
              campaign.name,
              campaign.status,
              metrics.impressions,
              metrics.clicks,
              metrics.cost_micros
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
            LIMIT 10
        """

        search_request = client.get_type("SearchGoogleAdsRequest")
        search_request.customer_id = customer_id
        search_request.query = query

        results = ga_service.search(request=search_request)

        print("| Campaign ID | Name | Status | Impressions | Clicks | Cost (USD) |")
        print("|---|---|---|---|---|---|")
        
        for row in results:
            cost = row.metrics.cost_micros / 1000000.0
            print(f"| {row.campaign.id} | {row.campaign.name} | {row.campaign.status.name} | {row.metrics.impressions} | {row.metrics.clicks} | ${cost:.2f} |")

    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
