from markettor.utils import get_instance_region
from markettor.cloud_utils import is_cloud


def get_ph_client():
    from markettoranalytics import Markettor

    if not is_cloud():
        return

    # send EU data to EU, US data to US
    api_key = None
    host = None
    region = get_instance_region()
    if region == "EU":
        api_key = "phc_dZ4GK1LRjhB97XozMSkEwPXx7OVANaJEwLErkY1phUF"
        host = "https://eu.i.markettor.com"
    elif region == "US":
        api_key = "sTMFPsFhdP1Ssg"
        host = "https://us.i.markettor.com"

    if not api_key:
        return

    ph_client = Markettor(api_key, host=host)

    return ph_client
