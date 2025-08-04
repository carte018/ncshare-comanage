# NCShare COManage extensions Docker build

This directory contains the files required to build the NCShare version of the CoManage Registry Docker container from the standard build of the CoManage Registry.

To use it, first build the default CoManage registry container according to the instructions in the main README.md file in this directory's parent directory.  Then rename the default CoManage registry container:

* comanage-registry:4.3.2-internet2-tier-1

built by the standard build process to:

* comanage-registry:4.3.2-internet2-tier-1-orig

and then use this directory to build a new comanage-registry:4.3.2-internet2-tier-1 container image based on he comanage-registry:4.3.2-internet2-tier-1-orig container image.

The build makes a number of adjustments to the default CoManage container installation:

* Disables weak TLS versions supported in the default Apache config
* Modifies the ClustersController.php code to grant $self access to view (but still not manage) Cluster provisioning so that end-users don't receive confusing errors when they attempt to click through the "Cluster" link in their COManage profile.  This was construed as problematic for the UX by users in NCShare.
* Modifies the CoLdapProvisionerTarget.php code to better handle provisioning of LDAP group memberships in the event that the target LDAP is using posixGroup objectclassed group objects with user uid values (rather than uidnumber values) in the memberUid group attribute (as is the case in the NCShare LDAP)
* Modifies the CoPetition subsystem to:
  * Eliminate requirement for email validation user email addresses (since NCShare only supports "official" addresses reported by users' home IDPs
  * Automatically log user out of COManage once the petition process has completed.  This avoids an error condition users encountered when trying to log in to COManage immediately after going through registration due to persistent petition state in their browsers.
  * Trigger an additional group provisioning operation after cluster provisioning is completed, since in the NCShare case, LDAP provisioning cannot be completed successfully until cluster identifiers are assigned to users.
* Installs postfix and reated depedencies in support of CoManage sending email notifications using authenticated SMTP (since NCShare does not support originating email from the domain otherwise)
* Installs an "mgr.php" application for managing expiration / renewal of CoManage identities.  This is a totally optional add-in to the COManage environment, and is dependent upon configuration of the COManage instance to set up expiration dates for user identities at registration time.
* Installs updated HTTP config to enforce authentication for "mgr.php" application (also optional)
* Installs a cron task to run the CoreJob.Expire Comanage job daily to trigger processing of identity expiration policies (also optional)
* Installs a modified version of the UnixCluster plugin lang.php library which eliminates spaces in the CN values for user-specific groups created during enrollment (to avoid Linux "ls -l" parsing issues when group names present with embedded spaces)
* Modifies the group membership management code to support an idiosyncratic group nesting behavior.  In NCShare, there are a collection of groups (one site-wide ncshare_support group, with project admin staff as members, and one $school_contacts group for each school with local IT staff from the school as members) to which management of special $school_h200 groups needs to be delegated.  In order to simplify automation of this delegated administrative model, the modifications cause members added to $school_h200 groups by virtue of being in nested groups named either "ncshare_support" or $school_contacts to be added to the $school_h200 groups as both members and owners, allowing them to manage the group without being added to it individually by project admins.  The default COManage code restricts group nesting to conferring member (never owner) rights in the containing group.
