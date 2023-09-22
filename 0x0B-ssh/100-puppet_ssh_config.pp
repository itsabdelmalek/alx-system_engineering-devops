#!/user/bin/env bash
# Define a custom resource type for managing SSH client configuration

# Define SSH client configuration content
$ssh_config_content = @(EOL)
Host *
    IdentityFile ~/.ssh/school
    PasswordAuthentication no
EOL

# Apply the configuration
file { '/etc/ssh/ssh_config':
  ensure  => present,
  mode    => '0644',
  content => $ssh_config_content,
}
