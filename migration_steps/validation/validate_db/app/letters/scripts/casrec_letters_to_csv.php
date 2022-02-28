<?php

// Convert Casrec letters CSVs into a JSON of case numbers

// Assumed directory structure:
//
//   2022-02-21
//       letters_file.csv
//   2022-02-22
//       letters_file.csv
//   casrec_letters_to_csv.php

$mainDir = dirname(__FILE__);

$csv = fopen($mainDir . '/casrec_letters.csv', 'w');
fputcsv($csv, ['caseno','date','type']);

foreach (scandir($mainDir) as $dir) {
    if (!is_dir($dir) || in_array($dir, ['.','..'])) {
        continue;
    }

    foreach (scandir($mainDir.'/'.$dir) as $file) {
        if (!strpos($file, '.csv')) {
            continue;
        }

        $fp = fopen($mainDir.'/'.$dir.'/'.$file, 'r');

        $header = fgetcsv($fp);

        if (trim(strtolower($header[0]), "﻿ \t\n\r\0\x0B") != 'caseno') {
            die(sprintf("Unexpected column name %s in %s/%s", $header[0], $dir, $file));
        }

        while (($line = fgetcsv($fp)) !== FALSE) {
            fputcsv($csv, [
                trim($line[0], "﻿ \t\n\r\0\x0B"),
                $dir,
                explode('.', $file)[0]
            ]);
        }

        fclose($fp);
    }
}

fclose($csv);
