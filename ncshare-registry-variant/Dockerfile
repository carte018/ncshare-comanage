FROM comanage-registry:4.3.2-internet2-tier-1-orig
COPY updatedClustersController.php /srv/comanage-registry/app/Controller/ClustersController.php
COPY updatedCoLdapProvisionerTarget.php /srv/comanage-registry/app/Plugin/LdapProvisioner/Model/CoLdapProvisionerTarget.php
COPY apache-include-virtual-host-port443-base /etc/httpd/apache-include-virtual-host-port443-base
RUN yum -y install postfix cyrus-sasl cyrus-sasl-plain
COPY main.cf /etc/postfix/main.cf
COPY supervisord.conf /usr/local/etc/supervisord.conf
COPY mgr.php /srv/comanage-registry/app/webroot/mgr.php
COPY mgr.css /srv/comanage-registry/app/webroot/css/mgr.css
COPY 000-comanage.conf /etc/httpd/conf.d/000-comanage.conf
COPY runexpire /etc/cron.d/runexpire
COPY uclang.php /srv/comanage-registry/app/AvailablePlugin/UnixCluster/Lib/lang.php
COPY updatedCoPetitionsController.php /srv/comanage-registry/app/Controller/CoPetitionsController.php
COPY updatedCoInvite.php /srv/comanage-registry/app/Model/CoInvite.php
COPY updatedCoPetition.php /srv/comanage-registry/app/Model/CoPetition.php
COPY updatedCoGroupMember.php /srv/comanage-registry/app/Model/CoGroupMember.php

RUN yum -y update shibboleth
