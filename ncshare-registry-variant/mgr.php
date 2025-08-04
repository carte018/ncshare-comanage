<html>
<head>
<title>Manage Identity Status</title>
<!--<link rel="stylesheet" href="css/co-base.css">-->
<link rel="stylesheet" href="css/mgr.css">
</head>
<body>
<?php

    // Context retrieval from environment -- who are we?  $my_id becomes ePPN of user.
    $my_id = $_SERVER['REMOTE_USER'];
    $co_name = file_get_contents('/run/secrets/co_name');
    $core_user = file_get_contents('/run/secrets/core_user');
    $core_pwd = file_get_contents('/run/secrets/core_pwd');
    $core_url = file_get_contents('/run/secrets/core_url');
    $co_user_title = file_get_contents('/run/secrets/co_user_title');


    // Relevant operations

    // Function to find the index of an object in an array of objects by property value
    // Returns the first (leftmost) matching object index in array (if more than one)
    function find_index_in_array($array,$prop,$value) {
        for ($i = 0; $i < count($array); $i++) {
                if ($array[$i]->$prop === $value) {
                        return $i;
                }
        }
    }

    // Same, but return the object rather than the index
    function find_in_array($array,$prop,$value) {
        for ($i = 0; $i < count($array); $i++) {
                if ($array[$i]->$prop === $value) {
                        return $array[$i];
                }
        }
    }

    // Get current user's co_person object from the core API

    function get_co_person_by_eppn($eppn) {
        $curl = curl_init();
        curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);  // grab result instead of printing
        curl_setopt($curl,CURLOPT_SSL_VERIFYPEER,0);  // don't verify peer - SSL cert ignore
        curl_setopt($curl,CURLOPT_HTTPAUTH,CURLAUTH_BASIC);  // http basic-auth
        curl_setopt($curl,CURLOPT_CUSTOMREQUEST,"GET");  // unnecessarily set GET request
        curl_setopt($curl,CURLOPT_USERPWD,$GLOBALS['core_user'].":".$GLOBALS['core_pwd']);  // creds
        $url = $GLOBALS['core_url'].$eppn;
        curl_setopt($curl,CURLOPT_URL,$url);
        $headers = ["Content-Type: application/json"];
        curl_setopt($curl,CURLOPT_HTTPHEADER,$headers);

        $res = curl_exec($curl);

        $coperson = json_decode($res);

        if (isset($coperson->error)) {
                return null;
        } else {
                return $coperson;
        }
    }

    // PUT co_person replacement to the core API
    // Requires the new person object to PUT and the eppn of the user to PUT it to

    function update_co_person($newperson,$eppn) {
	$curl = curl_init();
	curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
	curl_setopt($curl,CURLOPT_SSL_VERIFYPEER,0);
	curl_setopt($curl,CURLOPT_HTTPAUTH,CURLAUTH_BASIC);
	curl_setopt($curl,CURLOPT_CUSTOMREQUEST,"PUT");
	curl_setopt($curl,CURLOPT_USERPWD,$GLOBALS['core_user'].":".$GLOBALS['core_pwd']);
	$url = $GLOBALS['core_url'].$eppn;
	curl_setopt($curl,CURLOPT_URL,$url);
	curl_setopt($curl,CURLOPT_POSTFIELDS,json_encode($newperson));
	$headers = ["Content-Type: application/json"];
	curl_setopt($curl,CURLOPT_HTTPHEADER,$headers);
	
	curl_exec($curl);
    }


    // Handle POSTed responses so that updates get processed before retrieving the display
    // portion of the page.  This way, performing a "renew" results in seeing the renewed 
    // identify information rather than the stale info appearing until another reload.
    //
    // Check for authentication is redundant usually, but worth the effort for the 
    // odd case where a session expiration leads to a secondary SSO trip and the user 
    // has a new or missing identifier on the return trip.
    //
   
    if (isset($_POST['operation'])) {
	// This is a posted operation request
	if (isset($my_id)) {
		// And this is an authenticated request so we can proceed
		$cur_person = get_co_person_by_eppn($my_id);
		if (isset($cur_person) && isset($cur_person->CoPersonRole)) {
			// Person is registered (regardless of state)
			// Acquire role if possible
			$rolei = find_index_in_array($cur_person->CoPersonRole,"title",$co_user_title);
			if ($_POST['operation'] === 'renewnow' || $_POST['operation'] === 'reopen') {
				// Same operation for renew and reopen -- make active
				$cur_person->CoPersonRole[$rolei]->status = 'A';
				$newexp = date('Y-m-d H:i:s',time()+31536000);
				$cur_person->CoPersonRole[$rolei]->valid_through = $newexp;
			} else if ($_POST['operation'] === 'expirenow') {
				$cur_person->CoPersonRole[$rolei]->status = 'PC';
				$newexp = date('Y-m-d H:i:s',time());
				$cur_person->CoPersonRole[$rolei]->valid_through = $newexp;
			}
			update_co_person($cur_person,$my_id);
		}
	}
    }
		
?>
<div class="header">
<h1>Manage Your <?php echo $co_name; ?> Identity</h1>
</div>
<div class="intro">
<p>
This page allows you to manage your <?php echo $co_name; ?> identity.  Depending on the current status of your identity, you may be able to renew, revoke, or re-enable your identity here.
</p>
</div>
<?php
    if (! isset($my_id) || empty($my_id)) {
	// No user identity to use
?>
<div class="noid">
<p>
It appears that you do not have a current or expired <?php echo $co_name ?> identity to manage.  This could happen because your home IDP failed to send us your unique identifier (eduPersonPrincipalName), because your identifier has changed since you registered your <?php echo $co_name; ?>  identity, or becasue you have not yet registered as an <?php echo $co_name; ?>  user.  If you believe you have a registered identity in <?php echo $co_name; ?>, contact your local site administrators for assistance.
</p>
</div>
</body>
</html>
<?php
	return;
    } else {    

    $current_coperson = get_co_person_by_eppn($my_id);

    if (! isset($current_coperson) || empty($current_coperson)) {
?>
<div class="nocoperson">
<p>
You successfully authenticated at your home institution as <em><?php echo $my_id; ?></em>.  We are unable to match that institutional identifier with a current <?php echo $co_name; ?> identity.  this can happen if you have not yet registered as a <?php echo $co_name; ?> user, or if your institutional identifier has changed since you originally registered.  
</p>
<p>If you have not yet registered, contact your local IT support staff for instructions on registering with <?php echo $co_name; ?>.  
</p>
<p>If you believe you have a registered identity, contact the <?php echo $co_name; ?> administration for assistance ensuring that your identity registration is correct.
</p>
</div>
<?php 
    } else {
	// CoName-Member below needs to be replaced with the title value for your CO's active users
	$copr = find_in_array($current_coperson->CoPersonRole,"title","CoName-Member");

	$status = $copr->status;
	$expiration = $copr->valid_through;
	$coid = find_in_array($current_coperson->Identifier,"type","uid");
	$uid = $coid->identifier;
	$state_string = $status;
	if ($status === "GP") {
		$state_string = "Expiration Grace Period";
	} else if ($status === "PC") {
		$state_string = "Expired";
	} else if ($status === "A") {
		$state_string = "Active";
	}

?>
<div class="status">
<p>
The table below lists your <?php echo $co_name; ?> identity's current status:
</p>
<div class="tablediv">
<table class="statustable">
  <tr>
     <td>Institutional Identifier</td>
     <td><?php echo $my_id; ?></td>
  </tr>
  <tr>
    <td><?php echo $co_name; ?> ID</td>
    <td><?php echo $uid; ?></td>
  </tr>
  <tr>
    <td>Identity Status</td>
    <td><?php echo $state_string; ?></td>
  </tr>
  <tr>
    <td>Expiration Date</td>
    <td><?php echo $expiration; ?></td>
  </tr>
</table>
</div>
</div>
<div class="instructions">
<?php
  if ($status === "GP") {
?>

<p>
Our records indicate that your <?php echo $co_name; ?> identity expires in less than 30 days.  If you do nothing, on or just after the expiration date listed above, your <?php echo $co_name; ?> identity will be expired, and your access to <?php echo $co_name; ?> resources will be removed.  This will include both data storage and other services you may have previously used from <?php echo $co_name; ?>.  If you do not wish to continue to use <?php echo $co_name; ?> resources, do nothing, and your identity will expire automatically.
</p>
<p>
If you would like to continue using <?php echo $co_name; ?> resources after the expiration date listed above, you may click the "Renew Now" button below to immediately renew  your <?php echo $co_name; ?> identity.  Your identity and your access to <?php echo $co_name ?> resources will be continued for one year after you renew.  If you later decide you no longer wish to use <?php echo $co_name; ?> resources, you can always visit this page again to request immediate expiration of your identity.
</p>
<p>
If you wish to renew your identity, click the "Renew Now" button below.  If you wish to do nothing, click the "Cancel Operation" button below and you will be logged out of this site without any changes being made.
</p>
</div>
<div class="options">
<table class="renewnow">
<tr>
<td>
<form name="renewnow" method="POST" action="/registry/mgr.php">
<input type="hidden" name="operation" value="renewnow" id="operation">
<input type="submit" value="Renew Now" class="actionbutton">
</form>
</td>
<td>
<form name="cancel" method="GET" action="/Shibboleth.sso/Logout">
<input type="submit" value="Cancel Operation" class="cancelbutton">
</form>
</td>
</tr>
</table>
</div>
<?php
} else if ($status === "A") {
?>
<p>
Our records indicate that your <?php echo $co_name; ?> identity is active and will not expire for more than 30 days.  If you wish to continue to use your <?php echo $co_name; ?> identity, do nothing, or click the "Cancel Operation" button below to log out of this page without making any changes.  Your identity will remain active until the expiration date listed above.
</p>
<p>
If you no longer wish to use your <?php echo $co_name; ?> identity or any of the associated services, you may request immediate expiration of your identity by clicking the "Expire Now" button below.  Doing that will immediately expire your <?php echo $co_name; ?> identity and remove your access to all <?php echo $co_name; ?> resources associated with it. 
</p>
</div>
<div class="options">
<table class="expirenow">
<tr>
<td>
<form name="expirenow" method="POST" action="/registry/mgr.php">
<input type="hidden" name="operation" value="expirenow" id="operation">
<input type="submit" value="Expire Now" class="actionbutton">
</form>
</td>
<td>
<form name="cancel" method="GET" action="/Shibboleth.sso/Logout">
<input type="submit" value="Cancel Operation" class="cancelbutton">
</form>
</td>
</tr>
</table>
</div>
<?php
} else if ($status === "PC") {
?>
<p>
Our records indicate that your <?php echo $co_name; ?> identity is expired.  If you would like to renew your access to <?php echo $co_name; ?> resources, you may click the "Reopen Now" button below to request that your identity be reinstated.
</p>
<p>
If you do not wish to reopen your <?php echo $co_name; ?> account, no further action is necessary on your part.
</p>
</div>
<div class="options">
<table class="reopen">
<tr>
<td>
<form name="reopen" method="POST" action="/registry/mgr.php">
<input type="hidden" name="operation" value="reopen" id="operation">
<input type="submit" value="Reopen Now" class="actionbutton">
</form>
</td>
<td>
<form name="cancel" method="GET" action="/Shibboleth.sso/Logout">
<input type="submit" value="Cancel Operation" class="cancelbutton">
</form>
</td>
</tr>
</table>
</div>
<?php
}
?>
<?php
 }
?>
<?php
 }
?>
</body>
</html>
