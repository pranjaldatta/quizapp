import pymongo
from src.views.main import MainView
from configparser import ConfigParser

import argparse


def get_args():

    arg = argparse.ArgumentParser()
    arg.add_argument("--path", "-p", help="path to config file", required=True)
    return arg.parse_args()


if __name__ == "__main__":

    args = get_args()

    cfg = ConfigParser()
    cfg.read(args.path)

    db_username = cfg.get("mongodb", "username")
    db_pass = cfg.get("mongodb", "password")
    project = cfg.get("mongodb", "project")

    client = pymongo.MongoClient(
        f"mongodb+srv://{db_username}:{db_pass}@cluster0.h20fw.mongodb.net/{project}?retryWrites=true&w=majority",
    ).dev

    mv = MainView(client)
    mv.run()
