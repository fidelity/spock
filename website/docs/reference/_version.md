---
sidebar_label: _version
title: _version
---

Git implementation of _version.py.

#### get\_keywords

```python
def get_keywords()
```

Get the keywords needed to look up the version information.

## VersioneerConfig Objects

```python
class VersioneerConfig()
```

Container for Versioneer configuration parameters.

#### get\_config

```python
def get_config()
```

Create, populate and return the VersioneerConfig() object.

## NotThisMethod Objects

```python
class NotThisMethod(Exception)
```

Exception raised if a method is not valid for the current scenario.

#### register\_vcs\_handler

```python
def register_vcs_handler(vcs, method)
```

Create decorator to mark a method as the handler of a VCS.

#### run\_command

```python
def run_command(commands, args, cwd=None, verbose=False, hide_stderr=False, env=None)
```

Call the given command(s).

#### versions\_from\_parentdir

```python
def versions_from_parentdir(parentdir_prefix, root, verbose)
```

Try to determine the version from the parent directory name.

Source tarballs conventionally unpack into a directory that includes both
the project name and a version string. We will also support searching up
two directory levels for an appropriately named parent directory

#### git\_get\_keywords

```python
@register_vcs_handler("git", "get_keywords")
def git_get_keywords(versionfile_abs)
```

Extract version information from the given file.

#### git\_versions\_from\_keywords

```python
@register_vcs_handler("git", "keywords")
def git_versions_from_keywords(keywords, tag_prefix, verbose)
```

Get version information from git keywords.

#### git\_pieces\_from\_vcs

```python
@register_vcs_handler("git", "pieces_from_vcs")
def git_pieces_from_vcs(tag_prefix, root, verbose, run_command=run_command)
```

Get version from &#x27;git describe&#x27; in the root of the source tree.

This only gets called if the git-archive &#x27;subst&#x27; keywords were *not*
expanded, and _version.py hasn&#x27;t already been rewritten with a short
version string, meaning we&#x27;re inside a checked out source tree.

#### plus\_or\_dot

```python
def plus_or_dot(pieces)
```

Return a + if we don&#x27;t already have one, else return a .

#### render\_pep440

```python
def render_pep440(pieces)
```

Build up version string, with post-release &quot;local version identifier&quot;.

Our goal: TAG[+DISTANCE.gHEX[.dirty]] . Note that if you
get a tagged build and then dirty it, you&#x27;ll get TAG+0.gHEX.dirty

Exceptions:
1: no tags. git_describe was just HEX. 0+untagged.DISTANCE.gHEX[.dirty]

#### render\_pep440\_pre

```python
def render_pep440_pre(pieces)
```

TAG[.post0.devDISTANCE] -- No -dirty.

Exceptions:
1: no tags. 0.post0.devDISTANCE

#### render\_pep440\_post

```python
def render_pep440_post(pieces)
```

TAG[.postDISTANCE[.dev0]+gHEX] .

The &quot;.dev0&quot; means dirty. Note that .dev0 sorts backwards
(a dirty tree will appear &quot;older&quot; than the corresponding clean one),
but you shouldn&#x27;t be releasing software with -dirty anyways.

Exceptions:
1: no tags. 0.postDISTANCE[.dev0]

#### render\_pep440\_old

```python
def render_pep440_old(pieces)
```

TAG[.postDISTANCE[.dev0]] .

The &quot;.dev0&quot; means dirty.

Exceptions:
1: no tags. 0.postDISTANCE[.dev0]

#### render\_git\_describe

```python
def render_git_describe(pieces)
```

TAG[-DISTANCE-gHEX][-dirty].

Like &#x27;git describe --tags --dirty --always&#x27;.

Exceptions:
1: no tags. HEX[-dirty]  (note: no &#x27;g&#x27; prefix)

#### render\_git\_describe\_long

```python
def render_git_describe_long(pieces)
```

TAG-DISTANCE-gHEX[-dirty].

Like &#x27;git describe --tags --dirty --always -long&#x27;.
The distance/hash is unconditional.

Exceptions:
1: no tags. HEX[-dirty]  (note: no &#x27;g&#x27; prefix)

#### render

```python
def render(pieces, style)
```

Render the given version pieces into the requested style.

#### get\_versions

```python
def get_versions()
```

Get version information or return default if unable to do so.

