#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: Path to the file to create
        required: true
        type: str
    content:
        description: Content to write to the file
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a file with content
- name: Create a text file
  my_namespace.my_collection.my_own_module:
    path: /tmp/testfile.txt
    content: "Hello from my own module!"
'''

RETURN = r'''
path:
    description: Path to the created file
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
message:
    description: Success message
    type: str
    returned: always
    sample: 'File created successfully'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    if module.check_mode:
        result['changed'] = True
        result['path'] = path
        result['message'] = 'File would be created (check mode)'
        module.exit_json(**result)

    import os
    file_exists = os.path.exists(path)
    
    if file_exists:
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(msg=f'Failed to read file: {str(e)}', **result)
        
        if current_content == content:
            result['changed'] = False
            result['path'] = path
            result['message'] = 'File already exists with the same content'
            module.exit_json(**result)
    
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
        result['path'] = path
        result['message'] = 'File created successfully'
    except Exception as e:
        module.fail_json(msg=f'Failed to create file: {str(e)}', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()