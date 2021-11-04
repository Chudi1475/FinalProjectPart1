# Chukwudi Duru
# 1784955

import os
import datetime

SKIP_HEADER = True


def createCSVLine(header, data):
    # creates a comma sepperated line with the elements from data with order from header
    return ','.join([data[h] for h in header])


def createTable(data, cols, path):
    # create csv with given data and order of coloumns and save it at path
    saveData = []
    if not SKIP_HEADER:
        # add an header
        saveData = [','.join(cols)]
    saveData.extend([createCSVLine(cols, dataRow) for dataRow in data])
    with open(path, "w") as f:
        # save in file
        f.write('\n'.join(saveData))


def parseCSVLine(header, row):
    # parse row of csv as a dict
    result = dict()
    for h, r in zip(header, row.split(',')):
        result[h] = r.strip()
    return result


def parseTable(path, cols):
    # parse csv as a list of dictionaries for each row
    with open(path, "r") as f:
        return [parseCSVLine(cols, line) for line in f]


def main(mP, pP, sP):
    # get all the data with given headers or element names
    manufacturerList = parseTable(
        mP, ["item ID", "manufacturer name", "item type", "damaged indicator"])
    priceList = parseTable(pP, ["item ID", "price"])
    serviceList = parseTable(sP, ["item ID", "service date"])
    allItems = dict()
    # join all the data in the allItems dict, which maps from id to the item dict
    for m in manufacturerList:
        allItems[m["item ID"]] = m
    # created base data, add price and service date to the list
    for p in priceList:
        allItems[p["item ID"]]["price"] = p["price"]
    for s in serviceList:
        allItems[s["item ID"]]["service date"] = s["service date"]
    # create fullInventory csv
    createTable(sorted(list(allItems.values()), key=lambda x: x["manufacturer name"]), [
        "item ID", "manufacturer name", "item type", "price", "service date", "damaged indicator"], "FullInventory.csv")

    # create for each other result csv a list (or dict with lists for each item)
    damagedItems = []
    itemTypes = dict()
    pastService = []
    now = datetime.datetime.now().date()
    for item in allItems.values():
        # loop over all items and add to needed list
        if item["item type"] not in itemTypes:
            # add list, if there wasn't this item type
            itemTypes[item["item type"]] = []
        itemTypes[item["item type"]].append(item)
        # add to damaged list
        if item["damaged indicator"] != "":
            damagedItems.append(item)
        # create date from service date string
        dateParts = item["service date"].split('/')
        date = datetime.date(int(dateParts[2]), int(
            dateParts[0]), int(dateParts[1]))
        item["date"] = date
        if date < now:
            pastService.append(item)

    for t, items in itemTypes.items():
        # loop over each item type and create csv with all items
        createTable(sorted(items, key=lambda x: x["item ID"]), [
            "item ID", "manufacturer name", "item type", "price", "service date", "damaged indicator"], "{}Inventory.csv".format(t))

    # create past service data csv
    createTable(sorted(pastService, key=lambda x: x["date"]), [
        "item ID", "manufacturer name", "item type", "price", "service date"], "PastServiceDateInventory.csv")

    # create damaged csv
    createTable(sorted(damagedItems, key=lambda x: x["price"], reverse=True), [
        "item ID", "manufacturer name", "item type", "price", "service date"], "DamagedInventory.csv")


if __name__ == '__main__':
    # get all the correct paths
    manufacturerPath = "ManufacturerList.csv"
    while not os.path.exists(manufacturerPath):
        manufacturerPath = input('Path to the manufacturer list: ')
    pricePath = "PriceList.csv"
    while not os.path.exists(pricePath):
        pricePath = input('Path to the Price list: ')
    servicePath = "ServiceDatesList.csv"
    while not os.path.exists(servicePath):
        servicePath = input('Path to the service dates list: ')
    # call main function
    main(manufacturerPath, pricePath, servicePath)
