import os
import json
import argparse
import datetime
import sys
import sh
import logging
import time

POLL_COUNT = 10
INTERVAL = 10  # seconds


# ---------------- LOGGING ----------------
def setup_logging():
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - line %(lineno)d - %(message)s",
        handlers=[
            logging.FileHandler(f"ec2_operations_{timestamp}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ---------------- AUTH ----------------
def authentication(params):
    logging.info("Starting AWS authentication")

    for key in ["key_id", "access_key", "region"]:
        if not params.get(key):
            raise ValueError(f"Missing parameter: {key}")

    os.environ["AWS_ACCESS_KEY_ID"] = params["key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = params["access_key"]
    os.environ["AWS_DEFAULT_REGION"] = params["region"]
    os.environ["AWS_PAGER"] = ""

    logging.info("AWS authentication successful")


# ---------------- TAG HELPER ----------------
def get_instance_name(tags):
    if not tags:
        return "N/A"
    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value", "N/A")
    return "N/A"


# ---------------- STATE CHECK ----------------
def describe_instance_states(instance_ids):
    logging.info(f"Checking state for instances: {instance_ids}")

    result = sh.aws(
        "ec2", "describe-instances",
        "--instance-ids", *instance_ids
    )

    data = json.loads(str(result))
    states = {}

    for reservation in data.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            states[instance["InstanceId"]] = instance["State"]["Name"]

    logging.info(f"Current states: {states}")
    return states


# ---------------- MONITOR ----------------
def monitor(instance_ids, out, desired_state):
    for _ in range(POLL_COUNT):
        states = describe_instance_states(instance_ids)

        if states and all(
            state.lower() == desired_state.lower()
            for state in states.values()
        ):
            logging.info(f"All instances reached state: {desired_state}")
            describe_instances(instance_ids, out)
            return True

        logging.info(f"Waiting... current={states}, target={desired_state}")
        time.sleep(INTERVAL)

    logging.warning("Timeout waiting for desired state")
    return False


# ---------------- OPERATIONS ----------------
def operate_instances(operation, instance_ids, out, desired_state):
    logging.info(f"Performing '{operation}' on instances: {instance_ids}")

    sh.aws(
        "ec2",
        f"{operation}-instances",
        "--instance-ids", *instance_ids
    )

    return monitor(instance_ids, out, desired_state)


# ---------------- DESCRIBE ----------------
def describe_instances(instance_ids, out):
    logging.info("Fetching EC2 instance details")

    result = sh.aws(
        "ec2", "describe-instances",
        "--instance-ids", *instance_ids
    )

    data = json.loads(str(result))

    for reservation in data.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            out.append({
                "InstanceId": instance.get("InstanceId", "N/A"),
                "Name": get_instance_name(instance.get("Tags")),
                "State": instance.get("State", {}).get("Name", "N/A"),
                "Private IP": instance.get("PrivateIpAddress", "N/A"),
                "Public IP": instance.get("PublicIpAddress", "N/A"),
            })


# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser(description="EC2 operations using AWS CLI")

    parser.add_argument("--key_id", required=True)
    parser.add_argument("--access_key", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--all", action="store_true")
    parser.add_argument(
        "--operation",
        required=True,
        choices=["start", "stop", "reboot", "terminate"],
    )
    parser.add_argument(
        "--instance_id",
        nargs="+",
        default=[],
        help="One or more EC2 instance IDs",
    )

    params = vars(parser.parse_args())
    out = []

    setup_logging()
    logging.info("Script started")

    authentication(params)

    STATE_MAP = {
        "start": "running",
        "stop": "stopped",
        "reboot": "running",
        "terminate": "terminated",
    }

    desired_state = STATE_MAP[params["operation"]]

    if params["all"]:
        result = sh.aws("ec2", "describe-instances")
        data = json.loads(str(result))
        instance_ids = [
            inst["InstanceId"]
            for res in data.get("Reservations", [])
            for inst in res.get("Instances", [])
        ]
    else:
        instance_ids = params["instance_id"]

    if not instance_ids:
        raise ValueError("No instance IDs provided")

    operate_instances(params["operation"], instance_ids, out, desired_state)

    logging.info("Execution completed")
    print(json.dumps(out, indent=4))


if __name__ == "__main__":
    main()
