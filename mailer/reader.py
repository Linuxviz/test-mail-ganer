# -*- coding: utf-8 -*-

import json
import magic

from core.settings import ALLOWED_FILE_EXTANTIONS_FOR_SUBSCRIBERS_UPLOAD


class FileReader:
    # TODO try ecxept
    """
    Read document different extantions and return python list[dict].
    Reader must have a read function for every allowed mime type
    """

    @staticmethod
    def is_allowed_extantion(extantion):
        if extantion in ALLOWED_FILE_EXTANTIONS_FOR_SUBSCRIBERS_UPLOAD:
            return True
        return False

    @staticmethod
    def get_extantion(file_obj):
        try:
            extantion = magic.Magic(mime=True).from_file(file_obj.path)
        # TODO log
        except:
            extantion = None
        return extantion

    def read(self, file_obj):
        extantion = self.get_extantion(file_obj)
        if not extantion:
            raise Exception("Error in reading extantions")

        if not self.is_allowed_extantion(extantion):
            # TODO Сделать exaptions
            raise Exception("This is not a allowed extantion")

        if extantion == 'application/json':
            return self.read_json(file_obj)

        # if extantion == 'mime-type':
        # return self.current_reader(file_obj)
        raise Exception("The mem-type is allowed but havent an any reder")

    @staticmethod
    def read_json(file_obj):
        res = json.load(file_obj, encoding='utf-8')
        return res
