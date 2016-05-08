from .logger import *


class ImportOpRegistry:
    _ops = {}

    @staticmethod
    def register(realm, typ, op):
        if realm not in ImportOpRegistry._ops:
            ImportOpRegistry._ops[realm] = {}

        ImportOpRegistry._ops[realm][typ] = op

    @staticmethod
    def get(realm, typ):
        return ImportOpRegistry._ops[realm.lower()][typ.lower()]


class ImportOpValidationRegistry(ImportOpRegistry):
    _ops = {}

    @staticmethod
    def register(realm, typ, op):
        if realm not in ImportOpValidationRegistry._ops:
            ImportOpValidationRegistry._ops[realm] = {}

        ImportOpValidationRegistry._ops[realm][typ] = op

    @staticmethod
    def get(realm, typ):
        if typ.lower() in ImportOpValidationRegistry._ops[realm.lower()]:
            return ImportOpValidationRegistry._ops[realm.lower()][typ.lower()]
        else:
            return None


class ImportOpCleanRegistry(ImportOpRegistry):
    _ops = {}

    @staticmethod
    def register(realm, typ, op):
        if realm not in ImportOpCleanRegistry._ops:
            ImportOpCleanRegistry._ops[realm] = {}

        ImportOpCleanRegistry._ops[realm][typ] = op

    @staticmethod
    def get(realm, typ):
        print(realm + "/" + typ)
        return ImportOpCleanRegistry._ops[realm.lower()][typ.lower()]



