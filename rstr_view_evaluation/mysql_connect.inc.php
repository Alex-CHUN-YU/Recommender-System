
<?php

    function connect(){

        $db_server = "localhost";
        $db_name = "recommender_system";
        $db_user = "root";
        $db_passwd = "wmmkscsie";

        $con = mysqli_connect($db_server, $db_user, $db_passwd,$db_name);

        // Check connection
        if (mysqli_connect_errno()) {
            echo "Failed to connect to MySQL: " . mysqli_connect_error();
        }

        mysqli_set_charset($con, "utf8");

        return $con;
    }

?>
