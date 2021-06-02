import os.path
import glob

from pywhat.magic_numbers import FileSignatures
from pywhat.nameThatHash import Nth
from pywhat.regex_identifier import RegexIdentifier


class Identifier:
    def __init__(self):
        self.regex_id = RegexIdentifier()
        self.file_sig = FileSignatures()
        self.name_that_hash = Nth()

    def identify(self, input: str, api=False) -> dict:
        identify_obj = {}
        identify_obj["File Signatures"] = {}
        identify_obj["Regexes"] = {}

        if os.path.isdir(input):
            # if input is a directory, recursively search for all of the files
            for myfile in glob.iglob(input + "**/**", recursive=True):
                if os.path.isfile(myfile):
                    magic_numbers = self.file_sig.open_binary_scan_magic_nums(myfile)
                    text = self.file_sig.open_file_loc(myfile)

                    if not magic_numbers:
                        magic_numbers = self.file_sig.check_magic_nums(myfile)

                    short_name = os.path.basename(myfile)
                    identify_obj["File Signatures"][short_name] = magic_numbers
                    identify_obj["Regexes"][short_name] = self.regex_id.check(text)


        elif os.path.isfile(input):
            short_name = os.path.basename(input)
            magic_numbers = self.file_sig.open_binary_scan_magic_nums(input)
            text = self.file_sig.open_file_loc(input)

            # if file doesn't exist, check to see if the inputted text is
            # a file in hex format
            if not magic_numbers:
                magic_numbers = self.file_sig.check_magic_nums(text)

            short_name = os.path.basename(input)
            identify_obj["File Signatures"][short_name] = magic_numbers
            identify_obj["Regexes"][short_name] = self.regex_id.check(text)

        else:
            text = [input]
            identify_obj["Regexes"]["text"] = self.regex_id.check(text)


        for key, value in list(identify_obj.items()):
            for filename, result in list(identify_obj[key].items()):
                # if there are zero matches for this file/text, remove it from the dictionary
                if result == [] or not result:
                    del identify_obj[key][filename]

            # if there are zero regex or file signature matches, set it to None
            if len(identify_obj[key]) == 0:
                identify_obj[key] = None

        return identify_obj
