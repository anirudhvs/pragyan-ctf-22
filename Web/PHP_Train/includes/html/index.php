<?php
    show_source("index.php");
    include 'constants.php';
    error_reporting(0);
    if(isset($_GET["param1"])) {
        if(!strcmp($_GET["param1"], CONSTANT1)) {
            echo FLAG1;
        }
    }

    if(isset($_GET["param2"]) && isset($_GET["param3"])) {
        $str2 = $_GET["param2"];
        $str3 = $_GET["param3"];
        if(($str2 !== $str3) && (sha1($str2) === sha1($str3))) {
            echo FLAG2;
        }
    }

    if(isset($_GET["param4"])) {
        $str4 = $_GET["param4"];
        $str4=trim($str4);
        if($str4 == '1.2e3' && $str4 !== '1.2e3') {
            echo FLAG3;
        }
    }

    if(isset($_GET["param5"])) {
        $str5 = $_GET["param5"];
        if($str5 == 89 && $str5 !== '89' && $str5 !== 89 && strlen(trim($str5)) == 2) {
            echo FLAG4;
        }
    }

    if(isset($_GET["param6"])) {
        $str6 = $_GET["param6"];
        if(hash('md4', $str6) == 0) {
            echo FLAG5;
        }
    }

    if(isset($_GET["param7"])) {
        $str7 = $_GET["param7"];
        $var1 = 'helloworld';
        $var2 = preg_replace("/$var1/", '', $str7);
        if($var1 === $var2) {
            echo FLAG6;
        }
    }

    if(isset($_GET["param8"])) {
        $str8 = $_GET["param8"];
        $comp = range(1, 25);
        if(in_array($str8, $comp)) {
            if(preg_match("/\.env/", $str8)) {
                echo FLAG7;
            }
        }
    }

?>