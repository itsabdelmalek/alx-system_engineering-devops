# Fixes a 'phpp' typo to 'php' inside the WordPress file 'wp-settings.php'.
exec { 'fix-wordpress':
  command => 'sed -i.bak "s/phpp/php/g" /var/www/html/wp-settings.php',
  path    => '/usr/local/bin/:/bin/',
  onlyif  => 'grep -q "phpp" /var/www/html/wp-settings.php',
}
