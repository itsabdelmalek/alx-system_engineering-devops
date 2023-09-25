# webserver_manifest.pp

# Install Nginx package
package { 'nginx':
  ensure => 'installed',
}

# Enable and start Nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
}

# Configure Nginx for root page
file { '/etc/nginx/sites-available/default':
  content => "
  server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    location / {
      return 200 'Hello World!';
    }
  }",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Configure Nginx for redirection
file { '/etc/nginx/sites-available/redirect_me':
  content => "
  server {
    listen 80;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    location /redirect_me {
      return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
    }
  }",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

file { '/etc/nginx/sites-enabled/redirect_me':
  ensure  => 'link',
  target  => '/etc/nginx/sites-available/redirect_me',
  require => File['/etc/nginx/sites-available/redirect_me'],
  notify  => Service['nginx'],
}
