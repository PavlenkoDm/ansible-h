# Ansible Role: create_file

Creates a text file on the target host using the custom `my_own_module`.

## Requirements

This role is part of the `my_own_namespace.yandex_cloud_elk` collection.

## Role Variables

Available variables with their default values (see `defaults/main.yml`):

```yaml
file_path: /tmp/default_file.txt
```

Path where the file will be created.

```yaml
file_content: |
  This is a default content.
  Created by create_file role.
```

Content to write to the file. Supports multi-line strings.

## Dependencies

None.

## Example Playbook

```yaml
---
- name: Use create_file role
  hosts: localhost

  roles:
    - role: my_own_namespace.yandex_cloud_elk.create_file
      file_path: /tmp/my_custom_file.txt
      file_content: |
        Hello World!
        This is a custom file.
```

## Example with default values

```yaml
---
- name: Use create_file role with defaults
  hosts: localhost

  roles:
    - role: my_own_namespace.yandex_cloud_elk.create_file
```

This will create `/tmp/default_file.txt` with default content.

## License

GPL-3.0-or-later

## Author Information

Dmitry Pavlenko
