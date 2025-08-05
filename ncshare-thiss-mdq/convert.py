#!/usr/bin/python3

# For the moment, we list *all* InCommon IDPs -- that can be changed by applying filtering
# to the input XML here by entityID.  Unfortunately the metadata doesn't provide a reliable 
# means of geolocating IDPs to identify those "inside North Carolina".
#
# The JSON converted metadata produced here is read by the RA21 MDQ provider, which in turn is 
# consulted by the SeamlessAccess discovery service.
#
# As non-InCommon IDPs are added for trust, they need to have their JSON-converted metadata 
# appended to the JSON aggregate created here in or to make them available for discovery.
#
# The MDQ provider will need to be restarted each time this JSON aggregate is regenerated.

import sys
import json
import urllib.parse
import xml.etree.ElementTree as ET
import subprocess

subp = subprocess.Popen(['/usr/bin/curl','https://mdq.incommon.org/entities/'],stdout=subprocess.PIPE)
sout = subp.stdout
tree = ET.parse(sout)

root = tree.getroot()

print('[')

first=True
for c1 in root:
    isidp = False
    emit = {}
    eid = ""
    displayname = ""
    scope = ""
    if c1.tag.count('EntityDescriptor') >= 1:
        eid = c1.attrib['entityID']
        for sub1 in c1:
            if sub1.tag.count('IDPSSODescriptor') >= 1:
                isidp = True
                for sub2 in sub1:
                    if sub2.tag.count('Extensions') >= 1:
                        for sub3 in sub2:
                            if sub3.tag.count('Scope') >= 1:
                                scope = sub3.text
                            if sub3.tag.count('UIInfo') >= 1:
                                for sub4 in sub3:
                                    if sub4.tag.count('DisplayName') >= 1:
                                        displayname=sub4.text
    if isidp and 'nccu.edu' not in eid and 'meredith.edu' not in eid:
        emit['title'] = displayname
        emit['descr'] = displayname
        emit['auth'] = 'saml'
        emit['entity_id'] = eid
        emit['entityID'] = eid
        emit['scope'] = scope
        # InCommon IDPs are available to both comanage and the proxy IDP
        # Some bilateral IDPs (Okta) use different entity ids for each RP
        # so in some bilateral cases, an IDP may be 'comonly' or 'idponly'
        emit['keywords'] = 'comonly idponly'
        emit['type'] = 'idp'
        quoted = urllib.parse.quote(eid,safe="")
        emit['md_source'] = ('https://mdq.incommon.org/entities/' + quoted)
        if first:
            first=False
        else:
            print(',')
        print(json.dumps(emit))

# We load only IDPs from the InCommon metadata into the local MDQ JSON aggregate,
# so in order to provide vanity naming in RA21/SeamlessAccess for the NCShare Comanage
# instance, we load JSON metadata for it explicitly here.

addx={}
addx['title'] = 'NCShare Comanage'
addx['descr'] = 'NCShare Comanage'
addx['auth'] = 'saml'
addx['entity_id'] = 'https://ncshare-com-01.ncshare.org/shibboleth'
addx['entityID'] = 'https://ncshare-com-01.ncshare.org/shibboleth'
addx['type'] = 'sp'
print(',')
print(json.dumps(addx))

# The NCSHare Proxy IDP is not loaded as an IDP in the InCommon metadata.
# If that changes, this will become redundant, but until then, we add
# JSON metadata for it explicitly here and reference a local copy of its 
# full XML metadata.

addy={}
addy['title'] = 'NCShare proxy IDP'
addy['descr'] = 'NCShare proxy IDP'
addy['auth'] = 'saml'
addy['entity_id'] = 'https://ncshare-idp-01.ncshare.org/idp/shibboleth'
addy['entityID'] = 'https://ncshare-idp-01.ncshare.org/idp/shibboleth'
addy['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/idp-metadata.xml'
addy['type'] = 'idp'
print(',')
print(json.dumps(addy))


# We inject metadata references for the Google IDP instance for NCSSM here
#
# NCSSM is not an InCommon member, but we need their IDP to be available in the SA
#

addz={}
addz['title'] = 'NC School of Science and Math (NCSSM)'
addz['descr'] = 'NCSSM Google IDP'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://accounts.google.com/o/saml2?idpid=C049bhyqw'
addz['entityID'] = 'https://accounts.google.com/o/saml2?idpid=C049bhyqw'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/ncssm-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'ncssm.edu'
addz['scope'] = 'ncssm.edu'
addz['name_tag'] = 'NCSSM - North Carolina School of Science and Math'
addz['keywords'] = 'North Carolina School of Science and Math S&M comonly idponly'
print(',')
print(json.dumps(addz))

#
# And Meredith College
#

addz={}
addz['title'] = 'Meredith College (meredith.edu)'
addz['descr'] = 'Meredith College'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/b736a805-659f-4f7e-933b-131f734133d1/'
addz['entityID'] = 'https://sts.windows.net/b736a805-659f-4f7e-933b-131f734133d1/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/meredith-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'meredith.edu'
addz['scope'] = 'meredith.edu'
addz['name_tag'] = 'Meredith College - North Carolina'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# NCAT
#

addz={}
addz['title'] = 'NCAT (NC Agricultural and Technical State University)'
addz['descr'] = 'NC Agricultural and Technical State University (NCAT)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/d844dd75-a4d7-4b1f-bd33-bc0b1c796c38/'
addz['entityID'] = 'https://sts.windows.net/d844dd75-a4d7-4b1f-bd33-bc0b1c796c38/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/ncat-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'ncat.edu'
addz['scope'] = 'ncat.edu'
addz['name_tag'] = 'North Carolina Agricultural and Technical State University (NCAT)'
addz['keywords'] = 'North Carolina Agricultural and Technical State University ncat.edu aggies.ncat.edu comonly idponly'
print(',')
print(json.dumps(addz))

#
# NCCU recently (in 2024) had to decomission their InCommon IDP and move to 
# EntraID.
#

addz={}
addz['title'] = 'NCCU (NC Central University)'
addz['descr'] = 'NC Central University (NCCU)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/e86ab769-1eab-4e00-b79e-28ba7a8dbdf6/'
addz['entityID'] = 'https://sts.windows.net/e86ab769-1eab-4e00-b79e-28ba7a8dbdf6/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/nccu-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'nccu.edu'
addz['scope'] = 'nccu.edu'
addz['name_tag'] = 'North Carolina Central University (NCCU)'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# FSU
#

addz={}
addz['title'] = 'UNCFSU (Fayetteville State University)'
addz['descr'] = 'UNC-Fayetteville State University (UNCFSU)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/b2e1e6f4-64f1-4872-9da1-ca8a9a7c41f7/'
addz['entityID'] = 'https://sts.windows.net/b2e1e6f4-64f1-4872-9da1-ca8a9a7c41f7/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/uncfsu-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'uncfsu.edu'
addz['scope'] = 'uncfsu.edu'
addz['name_tag'] = 'Fayetteville State University (UNCFSU)'
addz['keywords'] = 'Fayetteville State University fsu comonly idponly'
print(',')
print(json.dumps(addz))

#
# UNC-W
#

addz={}
addz['title'] = 'UNCW - UNC Wilmington (uncw.edu)'
addz['descr'] = 'UNC-Wilmington (UNCW)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/22136781-9753-4c75-af28-68a078871ebf/'
addz['entityID'] = 'https://sts.windows.net/22136781-9753-4c75-af28-68a078871ebf/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/uncw-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'uncw.edu'
addz['scope'] = 'uncw.edu'
addz['name_tag'] = 'UNC Wilmington (UNCW)'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# Catawba College
#

addz={}
addz['title'] = 'Catawba College (catawba.edu)'
addz['descr'] = 'Catawba College (Catawba)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/73226585-c0ae-4f97-8b2a-625fcc3030a2/'
addz['entityID'] = 'https://sts.windows.net/73226585-c0ae-4f97-8b2a-625fcc3030a2/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/catawba-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'catawba.edu'
addz['scope'] = 'catawba.edu'
addz['name_tag'] = 'Catawba College (Catawba)'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# Chowan U
#

addz={}
addz['title'] = 'Chowan University (chowan.edu)'
addz['descr'] = 'Chowan University (Chowan)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/e083b159-b0b9-4a51-b5f8-eb9b61718231/'
addz['entityID'] = 'https://sts.windows.net/e083b159-b0b9-4a51-b5f8-eb9b61718231/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/chowan-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'chowan.edu'
addz['scope'] = 'chowan.edu'
addz['name_tag'] = 'Chowan University (Chowan)'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# UNC-P
#

addz={}
addz['title'] = 'UNC Pembroke (uncp.edu)'
addz['descr'] = 'UNC Pembroke (Pembroke)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/1aa2e328-7d0f-4fd1-9216-c479a1c14f9d/'
addz['entityID'] = 'https://sts.windows.net/1aa2e328-7d0f-4fd1-9216-c479a1c14f9d/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/uncp-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'uncp.edu'
addz['scope'] = 'uncp.edu'
addz['name_tag'] = 'University of North Carolina at Pembroke (Pembroke)'
addz['keywords'] = 'UNC Pembroke uncp.edu University of North Carolina at Pembroke comonly idponly'
print(',')
print(json.dumps(addz))

#
# Campbell U
#

addz={}
addz['title'] = 'Campbell University (campbell.edu)'
addz['descr'] = 'Campbell University (Campbell)'
addz['auth'] = 'saml'
addz['entity_id'] = 'https://sts.windows.net/98c4a3c2-24c3-40d9-b18f-4177190a1b5a/'
addz['entityID'] = 'https://sts.windows.net/98c4a3c2-24c3-40d9-b18f-4177190a1b5a/'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/campbell-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'campbell.edu'
addz['scope'] = 'campbell.edu'
addz['name_tag'] = 'Campbell University (Campbell)'
addz['keywords'] = 'comonly idponly'
print(',')
print(json.dumps(addz))

#
# Guilford College - Okta IDP presentation for COmanage
#

addz={}
addz['title'] = 'Guilford College (guilford.edu) [comanage]'
addz['descr'] = 'Guilford College (Guilford) [comanage]'
addz['auth'] = 'saml'
addz['entity_id'] = 'http://www.okta.com/exknd2ahqxQkE5Uri697'
addz['entityID'] = 'http://www.okta.com/exknd2ahqxQkE5Uri697'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/guilford-for-com-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'guilford.edu'
addz['scope'] = 'guilford.edu'
addz['name_tag'] = 'Guilford College (Guilford)'
addz['keywords'] = 'comonly'
print(',')
print(json.dumps(addz))

#
# Guilford College - Okta IDP presentation for proxy IDP
#

addz={}
addz['title'] = 'Guilford College (guilford.edu) [compsvcs]'
addz['descr'] = 'Guilford College (Guilford) [compsvcs]'
addz['auth'] = 'saml'
addz['entity_id'] = 'http://www.okta.com/exknd3q84ems1za6B697'
addz['entityID'] = 'http://www.okta.com/exknd3q84ems1za6B697'
addz['md_source'] = 'https://ncshare-idp-01.ncshare.org/metadata/guilford-for-idp-metadata.xml'
addz['type'] = 'idp'
addz['domain'] = 'guilford.edu'
addz['scope'] = 'guilford.edu'
addz['name_tag'] = 'Guilford College (Guilford)'
addz['keywords'] = 'idponly'
print(',')
print(json.dumps(addz))

print(']')
