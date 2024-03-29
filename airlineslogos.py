# -*- coding: UTF-8 -*-

import json
import urllib.request
import os
import argparse
from urllib.parse import quote
import logging
import socket
from socket import timeout
import ssl


def importLogos():
    # Set default values
    defWidth = 72
    defHeight = 24
    defStartFrom = 0
    defSaveToPath = "/airlines_logos/images"
    defLogName = "app_logs.log"
    defGetRetina = 0

    # Init parameters
    parser = argparse.ArgumentParser(description="Airlines logos downloader")
    parser.add_argument("--w", default=defWidth, type=int, help="Width of the image")
    parser.add_argument("--h", default=defHeight, type=int, help="Height of the image")
    parser.add_argument(
        "--rtn", default=defGetRetina, type=int, help="Get image for retina display"
    )
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
    parser.add_argument(
        "--iata", default="", type=str, help="Single IATA code of airline to download"
    )

    args = parser.parse_args()

    height = args.h if args.h > 0 else defHeight
    width = args.w if args.w > 0 else defWidth
    retinaImage = args.rtn if args.rtn > 0 else defGetRetina
    startFrom = args.s if args.s >= 0 else defStartFrom
    strLogosPath = args.p if args.p != "" else defSaveToPath
    strLogName = args.ln if args.ln != "" else defLogName
    strIATAcode = args.iata if len(args.iata) == 2 else ""

    # Init logging
    logging.basicConfig(
        filename=strLogName,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
    logging.info("=== Application started ===")
    logging.info(
        f"Import start with parameters: ImageHeight:{height}, ImageWidth:{width}, IATA:{strIATAcode}, StartFromPosition:{startFrom}, GetRetinaImage:{retinaImage}, SaveLogosTo:{strLogosPath}"
    )

    # Start processing
    if strIATAcode != "":
        logging.info(f"Saving single logo for {strIATAcode}")
        print(strIATAcode)
        saveAirlineLogo(strIATAcode, height, width, strLogosPath, retinaImage)
    else:
        counter = 0
        airlinesobj = getAirlines()

        logging.info(f"Found {len(airlinesobj)} airlines")
        logging.info(f"Starting import from {startFrom} position")

        for x in airlinesobj:
            if counter >= startFrom:
                print(x["code"])
                saveAirlineLogo(x["code"], height, width, strLogosPath, retinaImage)
                counter += 1
            else:
                counter += 1
    logging.info("=== Import complete ===")


def getAirlines():
    data = urllib.request.urlopen(
        "https://api.travelpayouts.com/data/ru/airlines.json"
    ).read()
    output = json.loads(data)
    return output


def saveAirlineLogo(airlineIATACode, height, width, path, retina):
    if retina == 0:
        urlpng = (
            f"https://pics.avs.io/{width}/{height}/{format(quote(airlineIATACode))}.png"
        )
    else:
        urlpng = f"https://pics.avs.io/{width}/{height}/{format(quote(airlineIATACode))}@2x.png"

    imgFolder = f"{path}/{height}x{width}"

    if not os.path.exists(imgFolder):
        os.makedirs(imgFolder)

    filename = f"{imgFolder}/{airlineIATACode}.png"

    socket.setdefaulttimeout(15)
    ssl._create_default_https_context = ssl._create_unverified_context

    remaining_download_tries = 3

    while remaining_download_tries > 0:
        try:
            urllib.request.urlretrieve(urlpng, filename)

        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            remaining_download_tries = remaining_download_tries - 1
            logging.error(
                f"Data of {airlineIATACode} not retrieved because {error} URL: {urlpng}"
            )
            continue
        except timeout:
            remaining_download_tries = remaining_download_tries - 1
            logging.error(f"Socket timed out - URL {urlpng}")
            continue
        else:
            logging.info(f"Succeed download: {urlpng}")
            break


if __name__ == "__main__":
    importLogos()
