<?php
if (isset($_SERVER['REQUEST_URI']) && $_SERVER['REQUEST_URI'] !== "/") {
  http_response_code(404);
  echo "404 Not Found";
  exit();
}
?>
<!doctype html>
<html lang="de">
<head>
  <title>WikiFeedMe</title>

  <link rel="shortcut icon" href="static/wikifeedme/favicon.ico" />
  <link type="text/css" rel="stylesheet" href="static/wikifeedme/main.css" />
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style type='text/css'>
    @font-face {
      font-family: 'Arapey';
      font-style: normal;
      font-weight: 400;
      src: local('Arapey Regular'), local('Arapey-Regular'), url(static/wikifeedme/hTZBMDBEmuM7E6AJpWkyGA.woff) format('woff');
    }
  </style>
  <style type='text/css'>
    body {
      margin-top: 100px;
      text-align: center;
    }
  </style>
  <?php require("analytics.php") ?>
</head>
<body>

<p>
  Viele Wikipedia-Artikel über Mahlzeiten haben noch kein Foto.<br/>
  Was liegt da näher, als das Gericht selber zuzubereiten, zu fotografieren, und in der Wikipedia einzubinden?
</p>

<a href="feedMe" class="mainButton">Zufallsmenü zusammenstellen</a>

</body>
</html>
