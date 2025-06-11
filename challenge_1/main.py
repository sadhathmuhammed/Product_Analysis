import csv
from collections import defaultdict
from typing import Dict


def parse_csv_file(file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Reads the CSV and returns a nested dictionary of parent_org -> brand -> cumulative view count
    """
    parent_brand_views = defaultdict(lambda: defaultdict(int))
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent_org = row.get("Parent org", "").strip().lower()
            brand = row.get("Brand", "").strip().lower()
            try:
                view_count = int(row.get("Product View Count", "0"))
            except ValueError as error:
                print(error)

            parent_brand_views[parent_org][brand] += view_count
    return parent_brand_views

def compute_totals(data: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Computes total product views for each parent org
    """
    return {parent: sum(brands.values()) for parent, brands in data.items()}


def display_results(parent_brand_views: Dict[str, Dict[str, int]], parent_totals: Dict[str, int]) -> None:
    """
    Displays the output in the required format
    """
    sorted_parents = sorted(parent_totals.items(), key=lambda x: x[1], reverse=True)
    for parent, total in sorted_parents:
        print(f"{parent} : {total}")
        sorted_brands = sorted(parent_brand_views[parent].items(), key=lambda x: x[1], reverse=True)
        for brand, count in sorted_brands:
            print(f"  {brand} : {count}")


def main():
    csv_path = "product_views.csv"
    parent_brand_views = parse_csv_file(csv_path)
    parent_totals = compute_totals(parent_brand_views)
    display_results(parent_brand_views, parent_totals)


if __name__ == "__main__":
    main()

