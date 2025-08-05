# NCShare JSON MDQ provider

In order to support both InCommon participant institutions in North Carolina and institutions that are not InCommon participants, NCShare operates its own SAML discovery service.  Based on the "thiss.io" (THe Identity Selector Software) JavaScript discovery ervice that forms the basis for the RA21 / SeamlessAccess DS service, the discovery service integrates InCommon's aggregated metadata (referenced via the InCommon MDQ service) with bilateral metadata provdied by NCShare schools not participating in InCommon through its own JSON MDQ service.

To support schools inside North Carolina using commercial IDPs that present separate IDP metadata to each of their registered relying parties (eg., Okta), the NCShare SeamlessAccess discovery service needed a way to differentiate, in the aggregated metadata, between those schools' IDP presentations for the COmanage relying party and for the NCShare proxy IDP relying party.  To facilitate that, NCShare runs a patched version of the thiss.io MDQ server that handles "keyword" matching in its trustinfo rules slightly differently than the distribution version of the MDQ server. 

# thiss.io MDQ patch

The patch provided here (metadata.js.patch) is to be applied to the distribution version of "metadata.js" provided with the thiss.io MDQ server.  It adds a special case to the processing of the "keywords" tag to treat the value as a space separated list of tags, rather than as a single keyword.

This allows the discovery service trust policy to restrict users to selecting one of their school's IDP presentations for accessing COmanage and another for accessing the NCShare proxy IDP, avoiding users' having to choose which of their IDP instances to use based on which service they're accessing.  Users are always presented with their school's name (alone) in the discovery service, and the DS chooses which of their school's IDP's metadata objects to reference based on tags added to the IDP metadata when converting it to JSON.

# convert.py script

The "convert.py" script included here is run hourly in the NCShare environment to update a file (incommon.json) that's mounted into the MDQ container as "/etc/metadata.json" to populate the JSON MDQ service. 

The script imports metadata from the InCommon MDQ service and converts it to the JSON format required by the thiss.io MDQ provider, then adds bilaterally-federated JSON metadata for non-InCommon NCShare participants' IDPs.  It adds "keywords" tags to each entry in the metadata to indicate whether a given IDP should be available for users' logging in to COmanage (comonly), the proxy IDP (idponly), or both (comonly idponly).  

Other sites will, of course, need to modify this script for their purposes.  Note that the MDQ service depends on published SAML (XML) metadat being available at some well-known URL for each IDP -- in the NCShare case, bilaterally federated IDPs have their metadata cached inside NCShare and presented via the web interface fronting the NCShare proxy IDP.  Any mechanism that allows a specific URL to be used to retrieve the original XML metadata for each federated IDP will work, however.

# 
