<?php

function get_xml_result($xml){
	$to_url = "http://127.0.0.1:9000/getXMLResult";
	$post = array(
		'xml' => $xml
	);
	$postData = json_encode($post);
	$ch = curl_init();
	$options = array(
		CURLOPT_URL=>$to_url,
		CURLOPT_HEADER=>0,
		CURLOPT_VERBOSE=>0,
		CURLOPT_RETURNTRANSFER=>true,
		CURLOPT_USERAGENT=>'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
		CURLOPT_POST=>true,
	);
	curl_setopt_array($ch, $options);

	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Content-Length: ' . strlen($postData)));
	curl_setopt($ch, CURLOPT_POSTFIELDS,$postData);
	// CURLOPT_RETURNTRANSFER=true 會傳回網頁回應,
	// false 時只回傳成功與否
	$response = curl_exec($ch);
	curl_close($ch);
	return $response;
} ?>