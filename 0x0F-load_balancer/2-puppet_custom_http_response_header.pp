class nginx {
  package { 'nginx':
    ensure => 'installed',
  }

  file { '/var/www/html/index.html':
    content => 'Hello World!',
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/default':
    content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
    }

    location / {
        add_header X-Served-By $host;
        return 200 'Hello World!';
    }
}",
    require => Package['nginx'],
  }

  exec { 'reload_nginx':
    command     => 'service nginx reload',
    refreshonly => true,
    subscribe   => File['/etc/nginx/sites-available/default'],
  }

  service { 'nginx':
    ensure => 'running',
    enable => true,
    require => [File['/etc/nginx/sites-available/default'], Exec['reload_nginx']],
  }
}

# Apply the nginx class
include nginx
