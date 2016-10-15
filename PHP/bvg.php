<?

include 'simple_html_dom.php';

// set the timezone correctly
date_default_timezone_set('Europe/Berlin');
$time_now = time();

$lines = array
    (
    array("Strassmannstr",
        array("Warschauer"),
        array("Hauptbahnhof", "Sportpark")
        )
    ,
    array("S+Landsberger+Allee+%28Berlin%29",
        array("Ringbahn S 42"),
        array("Ringbahn S 41")
         )
    ,
    array("S+Landsberger+Allee+%28Berlin%29",
        array("Pankow","<!-- TODO S8/S85/S9 -->"),
        array("Zeuthen","nau","Flughafen")
        )
    ,
    array("Bersarinplatz",
        array("neweide"),
        array("Lichtenberg")
        )
   );

$num_results_per_direction = 5;

///////////////////////////////////////////////

echo "{\n";

// stationn
foreach($lines as $station) {
    $_station     = $station;
    $station_name = array_shift($_station);
    $directions   = $_station;

    $html      = file_get_html('http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=' . $station_name .'&start=Suchen&boardType=depRT');
    $alltrains = $html->find('table[class=ivu_table]')[0]->children(3);


    $num_directions = sizeof($directions);
    // echo $station_name;
    // echo ' station in ';
    // echo $num_directions;
    // echo ' directions<br>';
    // richtungen
    foreach($directions as $direction) {

        unset($trains_to_destination);
        $trains_to_destination = array();
        // ziele
        //     echo 'Trains from ';
        // echo $station_name;
        // echo ':<br>';
        foreach($direction as $destination) {
            // zuge
            // echo 'Trains from ';
            // echo $station_name;
            // echo ' to ';
            // echo $destination;
            // echo "<br>\n";
            foreach($alltrains->children as $train) {

                $_time_dep_str = $train->children(0)->plaintext;
                $_time_dep_str = str_replace('*', '', $_time_dep_str);
                $_time_dep     = strtotime($_time_dep_str);

                $train_time_left_secs = $_time_dep - $time_now;

                $train_line = $train->children(1)->plaintext;

                $train_dir  = $train->children(2)->plaintext;

                // does this train have the desired destination?
                if (strpos($train_dir, $destination) !== false) {

                    // is the train in the past?
                    if ($train_time_left_secs > 0) {
                        // echo $train_time_left_secs;
                        // echo " secs<br>\n";

                        $trains_to_destination[] = $train_time_left_secs;
                    }
                }

            } // trains

        } // destinations

        // echo '<br>';

        sort($trains_to_destination);

        for ($i=count($trains_to_destination); $i < $num_results_per_direction; $i++) {
            $trains_to_destination[] = -999;
        }

        // echo "direction: ";
        // echo $direction[0];
        $counter = 0;
        foreach ($trains_to_destination as $train) {
            echo $train . " ";
            // $counter++;
            if(++$counter >= $num_results_per_direction)
                break;
        }

        echo "\n";
    } // directions
} // stations

echo "}";

/*

// load the page and extract the main section
$html = file_get_html('http://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=strassmannstr&start=Suchen&boardType=depRT');
$alltrains = $html->find('table[class=ivu_table]')[0]->children(3);

foreach($alltrains->children as $train) {

    $_time_dep_str = $train->children(0)->plaintext;
    $_time_dep_str = str_replace('*', '', $time_dep_str);
    $_time_dep     = strtotime($time_dep_str);

    $_time_left_secs = $time_dep - $time_now;

    $_line = $train->children(1)->plaintext;

    $_dir  = $train->children(2)->plaintext;

    $time[] = $_time_left_secs;

}

echo $time_now;
echo '<br>';
echo date('H:i:s', $time_now);
echo '<br><br>';

    echo $line;
    echo ' going to ';
    echo $dir;
    echo ' leaves at ';
    echo $time_dep_str;
    echo ' which is in ';
    echo $time_left_secs;
    echo ' secs';
    echo '<br>';
*/


?>
