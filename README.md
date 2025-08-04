# NCShare Overview

NCShare is a project involving a broad coalition of North Carolina educational institutions (both private and public).  The project aims to build a state-wide cyberinfrastructure that combines high-speed networking, shared computational resources, and state-of-the-art GPU resources to facilitate research and education at schools of all sizes across the state.  

The project is a collaboration across several different NSF grants:

* “NCShare Science DMZ,” which is under the direction of Tracy Futhey (Duke), Joel Faison (North Carolina Central), Kevin Davis (Davidson), Tracy Doaks (MCNC) and Jon Gant (North Carolina Central) (NSF OAC – 2201525 PI: Tracy Futhey)
* “NCShare Compute as a Service,” which is under the direction of Charley Kneifel (Duke), Tracy Futhey (Duke), Joel Faison (North Carolina Central), Mohammad Ahmed (North Carolina Central) and Kevin Davis (Davidson) (NSF OAC – 2201105 PI: Charley Kneifel) 
* “NCShare Accelerating Impact – GPU-as-a-Service,” which is under the direction of Tracy Futhey (Duke), J. Michael Baker (UNC-CH), Kaushik Roy (NCA&T), Charley Kneifel (Duke) and Tracy Doaks (MCNC) (NSF OAC – 2430141 PI: Tracy Futhey)

The work documented here was undertaken in order to facilitate management of user identities associated with the NCShare project, particularly as the project extends its reach under the third grant above (NSF OAC - 2430141 PI: Tracy Futhey) to include providing GPU-as-a-Service capabilities to North Carolina institutions.

# NCShare Facilities and IAM

Early in the project, there was no first-class identity and access management facility deployed inside NCShare.  As the project grew to engage a wider range of participant institutions, management of bilateral federation relationships with multiple different IDP providers at different schools became problematic, and manual maintenance of an LDAP registry for users of the compute cluster facility became unwieldy.  Outsourcing of some of the identity management infrastructure to gitlab.com, while functional, also came to be seen as a hindrance to widespread use of NCShare facilities.

The customizations offered here were developed as NCShare expanded its services to include a first-class "VO" IAM facility built around the COmanage system distributed as part of the InCommon Trusted Access Platform (TAP) effort.  COmanage provides an identity registry that allows users to use their home institutions' SSO facilities as their primary authentication service and primary identity provider, while affording NCShare the ability to manage project-specific identity attributes (including group memberships) without forcing participating institutions to expand their own local IAM infrastructures to accomodate additional information. 

NCShare's IAM facilities now comprise a single COmanage Registry installation that manages linked federated identities from participating schools and provisions NCShare-specific user identities into an OpenLDAP installation that in turn acts as the attribute store for a SAML-to-SAML/SAML-to-OIDC proxy (built around an instance of the Shibboleth IDP).  Users go through a one-time web-based automated registration process to establish NCShare identities linked to their institutional identities, and then use their institutional SSO systems to authenticate to the proxy IDP for access to NCShare web servcies.  Access to specialty resources (such as clustered GPU computing resources) is controlled through groups managed in COmanage and provisioned to the NCShare LDAP.  SSH access to Linux hosts in the computing cluster is provided using SSH keys distributed via the NCShare LDAP and managed by users via the COmanage Registry.

# NCShare Customizations to COmanage

The ncshare-registry-variant directory herein contains instructions for building a customized COmanage Docker image based on a pre-existing image built using the Internet2 TAP build of the COmanage Registry.  Details of the customizations may be found in the README.md in that directory.  In broad overview the changes affect:

* The default web flow for end-user sign-up in COmanage.  The changes remove some restrictions and eliminate some unnecessary steps from the registration process to make it faster and less complicated for end-users.

* The LDAP provisioning plugin distributed with COmanage.  The NCShare LDAP schema is tuned to support both the proxy IDP and Linux hosts in the NCShare cluster computing environment.  The default LDAP provisioning mechanism in COmanage is adjusted to accommodate the particular schema used inside NCShare.

* The identity lifecycle for COmanage-managed identities.  NCShare implements a policy requiring users at participating institutions to re-attest to their use of NCShare resources on an annual basis, and there are custom code additions to support automating the process of notifying users prior to their identities expiring and providing self-service re-attestation facilities for end-users.

 
