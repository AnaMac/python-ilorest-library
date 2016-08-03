# Copyright 2016 Hewlett Packard Enterprise Development, LP.
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.

import sys
from _redfishobject import RedfishObject
from ilorest.rest.v1_helper import ServerDownOrUnreachableError

def ex46_get_ahs_data(redfishobj):
    sys.stdout.write("\nEXAMPLE 46: Get AHS Data\n")
    instances = redfishobj.search_for_type("Manager.")

    for instance in instances:
        tmp = redfishobj.redfish_get(instance["@odata.id"])
        response = redfishobj.redfish_get(tmp.dict["Oem"]["Hp"]["Links"]\
                                          ["ActiveHealthSystem"]["@odata.id"])

        sys.stdout.write("Fetching AHS Data, this may take minutes to hours\n")
        ahslink = redfishobj.redfish_get(response.dict["Links"]["AHSLocation"]\
                                         ["extref"])

        with open("data.ahs", 'wb') as ahsoutput:
            ahsoutput.write(ahslink.read)
            ahsoutput.close()

        sys.stdout.write("AHS Data saved successfully as data.ahs\n")
        redfishobj.error_handler(response)

if __name__ == "__main__":
    # When running on the server locally use the following commented values
    # iLO_https_host = "blobstore://."
    # iLO_account = "None"
    # iLO_password = "None"

    # When running remotely connect using the iLO address, iLO account name,
    # and password to send https requests
    iLO_https_host = "https://10.0.0.100"
    iLO_account = "admin"
    iLO_password = "password"

    # Create a REDFISH object
    try:
        REDFISH_OBJ = RedfishObject(iLO_https_host, iLO_account, iLO_password)
    except ServerDownOrUnreachableError, excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support " \
                                                                "RedFish.\n")
        sys.exit()
    except Exception, excp:
        raise excp

    ex46_get_ahs_data(REDFISH_OBJ)

