# 2-puppet_custom_http_response_header.pp

# Define a class that sets up the custom HTTP response header
class custom_header {
  
  # Define the custom header name and value
  $header_name = 'X-Served-By'
  $header_value = $::hostname

  # Install Nginx
  package { 'nginx':
    ensure => installed,
  }

  # Create a custom Nginx config file with the desired header
  file { '/etc/nginx/sites-available/custom_header':
    ensure  => present,
    content => "server {\n\tlisten 80;\n\tserver_name _;\n\n\tlocation / {\n\t\tadd_header $header_name $header_value;\n\t\treturn 200 'Hello, World!';\n\t}\n}",
  }

  # Create a symlink to enable the config
  file { '/etc/nginx/sites-enabled/custom_header':
    ensure => link,
    target => '/etc/nginx/sites-available/custom_header',
    require => File['/etc/nginx/sites-available/custom_header'],
  }

  # Restart Nginx
  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/etc/nginx/sites-enabled/custom_header'],
  }
}

# Include the class to apply the configuration
include custom_header
