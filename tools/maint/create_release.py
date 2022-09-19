#!/usr/bin/env python3
# Copyright 2022 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

from datetime import datetime
import os
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(script_dir))

sys.path.append(root_dir)
from tools import shared, utils


def main():
  if subprocess.check_output(['git', 'status', '-uno', '--porcelain'], cwd=root_dir).strip():
    print('tree is not clean')
    return 1

  shared.set_version_globals()

  old_version = [shared.EMSCRIPTEN_VERSION_MAJOR, shared.EMSCRIPTEN_VERSION_MINOR,
                 shared.EMSCRIPTEN_VERSION_TINY]
  new_version = list(old_version)
  new_version[2] += 1

  old_version = '.'.join(str(v) for v in old_version)
  new_version = '.'.join(str(v) for v in new_version)

  print('Creating new release: %s' % new_version)

  version_file = os.path.join(root_dir, 'emscripten-version.txt')
  changelog_file = os.path.join(root_dir, 'ChangeLog.md')

  old_content = utils.read_file(version_file)
  utils.write_file(version_file, old_content.replace(old_version, new_version))

  changelog = utils.read_file(changelog_file)
  marker = f'{old_version} (in development)'
  pos = changelog.find(marker)
  assert pos != -1
  pos += 2 * len(marker) + 1

  # Add new entry
  today = datetime.now().strftime('%m/%d/%y')
  new_entry = f'{old_version} - {today}'
  new_entry = '\n\n' + new_entry + '\n' + ('-' * len(new_entry))
  changelog = changelog[:pos] + new_entry + changelog[pos:]

  # Update the "in development" entry
  changelog = changelog.replace(f'{old_version} (in development)', f'{new_version} (in development)')

  utils.write_file(changelog_file, changelog)

  branch_name = 'version_' + new_version

  # Create a new git branch
  subprocess.check_call(['git', 'checkout', '-b', branch_name], cwd=root_dir)

  # Create auto-generated changes to the new git branch
  subprocess.check_call(['git', 'add', '-u', '.'], cwd=root_dir)
  subprocess.check_call(['git', 'commit', '-m', new_version], cwd=root_dir)

  print('New relase created in branch: `%s`' % branch_name)

  # TODO(sbc): Maybe create the tag too, and even push both to `origin`?
  return 0


if __name__ == '__main__':
  sys.exit(main())