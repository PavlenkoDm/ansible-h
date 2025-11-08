# Ansible Collection - my_own_namespace.yandex_cloud_elk

Custom Ansible collection containing `my_own_module` for creating text files on remote hosts.

## Description

This collection provides:

- **my_own_module**: A custom module for creating text files with specified content
- **create_file role**: A role that uses my_own_module to create files with default parameters

## Installation

```bash
ansible-galaxy collection install my_own_namespace.yandex_cloud_elk
```

## Usage

### Using the module directly

```yaml
- name: Create a file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/myfile.txt
    content: "Hello, World!"
```

### Using the role

```yaml
- hosts: localhost
  roles:
    - role: my_own_namespace.yandex_cloud_elk.create_file
      file_path: /tmp/myfile.txt
      file_content: "Hello from role!"
```

## Module Parameters

### my_own_module

- `path` (required, string): Path to the file to create
- `content` (required, string): Content to write to the file

## Role Variables

### create_file

- `file_path` (default: `/tmp/default_file.txt`): Path to the file
- `file_content` (default: "This is a default content..."): File content

## License

GPL-3.0-or-later

## Author

Dmitry Pavlenko
