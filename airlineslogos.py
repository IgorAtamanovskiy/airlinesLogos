# -*- coding: UTF-8 -*-

import json
import urllib.request
import os
import argparse
from urllib.parse import quote
import logging


def importLogos():
    # Set default values
    defWidth = 72
    defHeight = 24
    defStartFrom = 0
    defSaveToPath = "/airlines_logos/images"
    defLogName = "avialogos.log"

    # Init parameters
    parser = argparse.ArgumentParser(description="Airlines logos downloader")
    parser.add_argument("--w", default=defWidth, type=int, help="Width of the image")
    parser.add_argument("--h", default=defHeight, type=int, help="Height of the image")
    parser.add_argument(
        "--s",
        default=defStartFrom,
        type=int,
        help="Start from 'n' item in airlines list",
    )
    parser.add_argument(
        "--p", default=defSaveToPath, type=str, help="Path to save images"
    )
    parser.add_argument("--ln", default=defLogName, type=str, help="Path to save logs")
    parser.add_argument("--iata", default="", type=str, help="Single IATA code of airline to download")

    args = parser.parse_args()

    height = args.h if args.h > 0 else defHeight
    width = args.w if args.w > 0 else defWidth
    startFrom = args.s if args.s >= 0 else defStartFrom
    strLogosPath = args.p if args.p != "" else defSaveToPath
    strLogName = args.ln if args.ln != "" else defLogName
    strIATAcode = args.iata if len(args.iata)==2 else ""

    # Init logging
    logging.basicConfig(
        filename=strLogName,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
    logging.info("=== Application started ===")
    logging.info(
        f"Import start with parameters: ImageHeight:{height}, ImageWidth:{width}, IATA:{strIATAcode}, StartFromPosition:{startFrom}, SaveLogosTo:{strLogosPath}"
    )

    # Start processing
    if strIATAcode != "":
        logging.info(f"Saving single logo for {strIATAcode}")
        print(strIATAcode)
        saveAirlineLogo(strIATAcode, height, width, strLogosPath)

    else:
        counter = 0
        airlinesobj = getAirlines()

        logging.info(f"Found {len(airlinesobj)} airlines")
        logging.info(f"Starting import from {startFrom} position")

        for x in airlinesobj:
            if counter >= startFrom:
                print(x["code"])
                saveAirlineLogo(x["code"], height, width, strLogosPath)
                counter += 1
            else:
                counter += 1

    logging.info("=== Import complete successfully ===")


def getAirlines():
    data = urllib.request.urlopen(
        "https://api.travelpayouts.com/data/ru/airlines.json"
    ).read()
    output = json.loads(data)
    return output


def saveAirlineLogo(airlineIATACode, height, width, path):

    urlpng = (
        f"https://pics.avs.io/{width}/{height}/{format(quote(airlineIATACode))}.png"
    )

    imgFolder = f"{path}/{height}x{width}"

    if not os.path.exists(imgFolder):
        os.makedirs(imgFolder)

    filename = f"{imgFolder}/{airlineIATACode}.png"

    urllib.request.urlretrieve(urlpng, filename)


if __name__ == "__main__":
    importLogos()
