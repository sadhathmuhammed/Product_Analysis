import requests
from typing import Any, Dict, List


def fetch_product_data(product_id: str) -> Dict[str, Any]:
    """
    Fetch product data from the Shopalyst Product Knowledge Graph API.
    """
    try:
        API_URL = f"https://dev.shopalyst.com/shopalyst-service/v1/products/{product_id}"
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Error fetching data for productId {product_id}: {error}")
        return {}


def extract_sku_details(product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract SKU details from `skuSet` key.
    """
    sku_set = product_data.get("skuSet", [])
    title = product_data.get("title", "N/A")
    sku_details = []

    for sku in sku_set:
        sku_id = sku.get("skuId", "N/A")
        offer_price = sku.get("offerPrice", "N/A")
        sale_price = sku.get("salePrice", "N/A")
        attributes = sku.get("attributes", {})
        shade = attributes.get("1", "N/A")  # "1" corresponds to shade

        sku_details.append({
            "skuId": sku_id,
            "shade": shade,
            "offerPrice": offer_price,
            "salePrice": sale_price,
            "title": f"{title} - {shade}"
        })

    return sku_details


def display_sku_details(sku_list: List[Dict[str, Any]]) -> None:
    """
    Display SKU details in the required output format.
    """
    for index, sku in enumerate(sku_list, start=1):
        print("--------------------------")
        print(f"Product {index}")
        print(f"skuId : {sku['skuId']}")
        print(f"shade : {sku['shade']}")
        print(f"offerPrice : {sku['offerPrice']}")
        print(f"title : {sku['title']}")
    print("--------------------------")


def main():
    product_id = input("Enter the productId: ").strip()
    product_data = fetch_product_data(product_id)
    if not product_data:
        print("No product data available.")
        return

    sku_list = extract_sku_details(product_data)
    if not sku_list:
        print("No SKUs found for the given product.")
        return

    display_sku_details(sku_list)


if __name__ == "__main__":
    main()
