

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = Path(__file__).parent / "pink_morsels_sales.csv"


def iter_input_files() -> Iterable[Path]:
	"""Yield input CSV files sorted by name for stable processing."""

	return sorted(DATA_DIR.glob("daily_sales_data_*.csv"))


def parse_sales(row: dict[str, str]) -> float:
	price = float(row["price"].replace("$", ""))
	quantity = int(row["quantity"])
	return price * quantity


def is_pink_morsel(row: dict[str, str]) -> bool:
	return row.get("product", "").strip().lower() == "pink morsel"


def build_output_rows() -> Iterable[list[str]]:
	for path in iter_input_files():
		with path.open(newline="", encoding="utf-8") as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
				if not is_pink_morsel(row):
					continue
				sales = parse_sales(row)
				yield [f"{sales:.2f}", row["date"], row["region"]]


def write_output() -> None:
	OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
	with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["Sales", "Date", "Region"])
		writer.writerows(build_output_rows())


if __name__ == "__main__":
	write_output()
