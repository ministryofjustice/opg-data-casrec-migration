import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
sys.path.append(str(current_path) + "/../shared")

# logging
environment = os.environ.get("ENVIRONMENT")
# Update to DEBUG for extra logging whilst developing
from api_test import ApiTests


def main():
    csvs = [
        "clients",
        "orders",
        "bonds",
        "deputies",
        "deputy_fee_payer",
        "deputy_orders",
        "deputy_clients_count",
        "supervision_level",
        "client_death_notifications",
        "deputy_death_notifications",
        "warnings",
        "crec",
        "visits",
        "reports",
        "invoice",
    ]

    api_tests = ApiTests()
    api_tests.enhance_api_user_permissions()

    for csv in csvs:
        api_tests.create_a_session()
        api_tests.csv = csv
        api_tests.run_response_tests()
    api_tests.upload_log_file()

    if api_tests.failed:
        print("Tests Failed")
        # Changing this whilst we are doing first part of deduplication as expecting failures on pre
        if environment in ["local", "development"]:
            exit(1)
    else:
        print("Tests Passed")


if __name__ == "__main__":
    main()
