<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);
//$db = new SQLite3("/home/dnaber/djangosite/wikifeedme/nomnom.db");
$db = new SQLite3("../nomnom.db");
if (!$db) {
  die("Could not open DB");
}

function printRandom($type, $db) {
  $results = $db->query("SELECT * from nom where kind='".$type."' ORDER BY RANDOM() LIMIT 1");
  while ($row = $results->fetchArray()) {
    ?>
    <a href="<?php echo $row['link']?>"><?php echo $row['name']?></a> <span class="chefkoch"> <a href="https://www.google.de/search?q=<?php echo $row['name']?>+Rezept&amp;wo=2&amp;ie=utf-8&amp;oe=utf-8">Google</a></span>
  <?php
  }
}

function printCount($type, $db) {
  $results = $db->query("SELECT count(*) AS count from nom where kind='".$type."'");
  while ($row = $results->fetchArray()) {
    echo $row['count'];
  }
}
?>

<!doctype html>
<html lang="de">
<head>
  <title>WikiFeedMe</title>
  <meta name="robots" content="nofollow"/>
  <link rel="shortcut icon" href="../static/wikifeedme/favicon.ico" />
  <link type="text/css" rel="stylesheet" href="../static/wikifeedme/main.css" />
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style type='text/css'>
    @import url(http://weloveiconfonts.com/api/?family=fontelico);
    [class*="fontelico-"]:before {
      font-family: 'fontelico', sans-serif;
    }
    @font-face {
      font-family: 'Great Vibes';
      font-style: normal;
      font-weight: 400;
      src: local('Great Vibes'), local('GreatVibes-Regular'), url(../static/wikifeedme/6q1c0ofG6NKsEhAc2eh-3YbN6UDyHWBl620a-IRfuBk.woff) format('woff');
    }
    @font-face {
      font-family: 'Arapey';
      font-style: normal;
      font-weight: 400;
      src: local('Arapey Regular'), local('Arapey-Regular'), url(../static/wikifeedme/hTZBMDBEmuM7E6AJpWkyGA.woff) format('woff');
    }
  </style>
</head>
<body>

<?php if (isset($_GET['info'])) { ?>
  Starter: <?php printCount('Starter', $db);?>,
  MainCourse: <?php printCount('MainCourse', $db); ?>,
  Dessert: <?php printCount('Dessert', $db); ?>,
  Cheese: <?php printCount('Cheese', $db); ?>
<?php } ?>

<p style="text-align: right"><a href="../about">Über</a></p>

<ol>

  <li>
    <p>Folgende Speisen hat das Wiki-Orakel für Dich ausgesucht.<br/>
      Suche die Rezepte und bereite die Speisen zu:</p>

    <div class="main">

      <div class="type">
        Vorspeise
      </div>
      <div class="course">
        <?php printRandom("Starter", $db); ?>
      </div>

      <div class="type">
        Hauptgericht
      </div>
      <div class="course">
        <?php printRandom("MainCourse", $db); ?>
      </div>

      <div class="type">
        Dessert
      </div>
      <div class="course">
        <?php printRandom("Dessert", $db); ?>
      </div>

      <div style="margin-top: 30px;margin-left: 12px">
        <a href="?1415111914.9"><span class="fontelico-spin3"></span> Neue Vorschläge</a>
      </div>

    </div>

  </li>

  <li><p>Fotografiere Deine Speisen.</p></li>

  <li><p>Verspeise Deine Speisen.</p></li>

  <li><p>Lade die Bilder Deiner Speisen
      <a href="https://commons.wikimedia.org/wiki/Special:UploadWizard?setlang=de">auf Wikimedia Commons</a> hoch<br/>und binde sie in der Wikipedia ein.</p></li>
</ol>

<?php require("../analytics.php") ?>

</body>
</html>

<?php
$db->close();
?>
