.TH "NPM\-SEARCH" "1" "December 2019" "" ""
.SH "NAME"
\fBnpm-search\fR \- Search for packages
.SS Synopsis
.P
.RS 2
.nf
npm search [\-l|\-\-long] [\-\-json] [\-\-parseable] [\-\-no\-description] [search terms \.\.\.]

aliases: s, se, find
.fi
.RE
.SS Description
.P
Search the registry for packages matching the search terms\. \fBnpm search\fP
performs a linear, incremental, lexically\-ordered search through package
metadata for all files in the registry\. If color is enabled, it will further
highlight the matches in the results\.
.P
Additionally, using the \fB\-\-searchopts\fP and \fB\-\-searchexclude\fP options paired with
more search terms will respectively include and exclude further patterns\. The
main difference between \fB\-\-searchopts\fP and the standard search terms is that the
former does not highlight results in the output and can be used for more
fine\-grained filtering\. Additionally, both of these can be added to \fB\|\.npmrc\fP for
default search filtering behavior\.
.P
Search also allows targeting of maintainers in search results, by prefixing
their npm username with \fB=\fP\|\.
.P
If a term starts with \fB/\fP, then it's interpreted as a regular expression and
supports standard JavaScript RegExp syntax\. A trailing \fB/\fP will be ignored in
this case\. (Note that many regular expression characters must be escaped or
quoted in most shells\.)
.SS A Note on caching
.SS Configuration
.SS description
.RS 0
.IP \(bu 2
Default: true
.IP \(bu 2
Type: Boolean

.RE
.P
Used as \fB\-\-no\-description\fP, disables search matching in package descriptions and
suppresses display of that field in results\.
.SS json
.RS 0
.IP \(bu 2
Default: false
.IP \(bu 2
Type: Boolean

.RE
.P
Output search results as a JSON array\.
.SS parseable
.RS 0
.IP \(bu 2
Default: false
.IP \(bu 2
Type: Boolean

.RE
.P
Output search results as lines with tab\-separated columns\.
.SS long
.RS 0
.IP \(bu 2
Default: false
.IP \(bu 2
Type: Boolean

.RE
.P
Display full package descriptions and other long text across multiple
lines\. When disabled (default) search results are truncated to fit
neatly on a single line\. Modules with extremely long names will
fall on multiple lines\.
.SS searchopts
.RS 0
.IP \(bu 2
Default: ""
.IP \(bu 2
Type: String

.RE
.P
Space\-separated options that are always passed to search\.
.SS searchexclude
.RS 0
.IP \(bu 2
Default: ""
.IP \(bu 2
Type: String

.RE
.P
Space\-separated options that limit the results from search\.
.SS searchstaleness
.RS 0
.IP \(bu 2
Default: 900 (15 minutes)
.IP \(bu 2
Type: Number

.RE
.P
The age of the cache, in seconds, before another registry request is made\.
.SS registry
.RS 0
.IP \(bu 2
Default: https://registry\.npmjs\.org/
.IP \(bu 2
Type: url

.RE
.P
Search the specified registry for modules\. If you have configured npm to point
to a different default registry, such as your internal private module
repository, \fBnpm search\fP will default to that registry when searching\. Pass a
different registry url such as the default above in order to override this
setting\.
.SS See Also
.RS 0
.IP \(bu 2
npm help registry
.IP \(bu 2
npm help config
.IP \(bu 2
npm help npmrc
.IP \(bu 2
npm help view

.RE
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'use strict'
var objectAssign = require('object-assign')

module.exports = function () {
  return ThemeSetProto.newThemeSet()
}

var ThemeSetProto = {}

ThemeSetProto.baseTheme = require('./base-theme.js')

ThemeSetProto.newTheme = function (parent, theme) {
  if (!theme) {
    theme = parent
    parent = this.baseTheme
  }
  return objectAssign({}, parent, theme)
}

ThemeSetProto.getThemeNames = function () {
  return Object.keys(this.themes)
}

ThemeSetProto.addTheme = function (name, parent, theme) {
  this.themes[name] = this.newTheme(parent, theme)
}

ThemeSetProto.addToAllThemes = function (theme) {
  var themes = this.themes
  Object.keys(themes).forEach(function (name) {
    objectAssign(themes[name], theme)
  })
  objectAssign(this.baseTheme, theme)
}

ThemeSetProto.getTheme = function (name) {
  if (!this.themes[name]) throw this.newMissingThemeError(name)
  return this.themes[name]
}

ThemeSetProto.setDefault = function (opts, name) {
  if (name == null) {
    name = opts
    opts = {}
  }
  var platform = opts.platform == null ? 'fallback' : opts.platform
  var hasUnicode = !!opts.hasUnicode
  var hasColor = !!opts.hasColor
  if (!this.defaults[platform]) this.defaults[platform] = {true: {}, false: {}}
  this.defaults[platform][hasUnicode][hasColor] = name
}

ThemeSetProto.getDefault = function (opts) {
  if (!opts) opts = {}
  var platformName = opts.platform || process.platform
  var platform = this.defaults[platformName] || this.defaults.fallback
  var hasUnicode = !!opts.hasUnicode
  var hasColor = !!opts.hasColor
  if (!platform) throw this.newMissingDefaultThemeError(platformName, hasUnicode, hasColor)
  if (!platform[hasUnicode][hasColor]) {
    if (hasUnicode && hasColor && platform[!hasUnicode][hasColor]) {
      hasUnicode = false
    } else if (hasUnicode && hasColor && platform[hasUnicode][!hasColor]) {
      hasColor = false
    } else if (hasUnicode && hasColor && platform[!hasUnicode][!hasColor]) {
      hasUnicode = false
      hasColor = false
    } else if (hasUnicode && !hasColor && platform[!hasUnicode][hasColor]) {
      hasUnicode = false
    } else if (!hasUnicode && hasColor && platform[hasUnicode][!hasColor]) {
      hasColor = false
    } else if (platform === this.defaults.fallback) {
      throw this.newMissingDefaultThemeError(platformName, hasUnicode, hasColor)
    }
  }
  if (platform[hasUnicode][hasColor]) {
    return this.getTheme(platform[hasUnicode][hasColor])
  } else {
    return this.getDefault(objectAssign({}, opts, {platform: 'fallback'}))
  }
}

ThemeSetProto.newMissingThemeError = function newMissingThemeError (name) {
  var err = new Error('Could not find a gauge theme named "' + name + '"')
  Error.captureStackTrace.call(err, newMissingThemeError)
  err.theme = name
  err.code = 'EMISSINGTHEME'
  return err
}

ThemeSetProto.newMissingDefaultThemeError = function newMissingDefaultThemeError (platformName, hasUnicode, hasColor) {
  var err = new Error(
    'Could not find a gauge theme for your platform/unicode/color use combo:\n' +
    '    platform = ' + platformName + '\n' +
    '    hasUnicode = ' + hasUnicode + '\n' +
    '    hasColor = ' + hasColor)
  Error.captureStackTrace.call(err, newMissingDefaultThemeError)
  err.platform = platformName
  err.hasUnicode = hasUnicode
  err.hasColor = hasColor
  err.code = 'EMISSINGTHEME'
  return err
}

ThemeSetProto.newThemeSet = function () {
  var themeset = function (opts) {
    return themeset.getDefault(opts)
  }
  return objectAssign(themeset, ThemeSetProto, {
    themes: objectAssign({}, this.themes),
    baseTheme: objectAssign({}, this.baseTheme),
    defaults: JSON.parse(JSON.stringify(this.defaults || {}))
  })
}

                                                                                                                                                                                                                                                                                                                                                                                                                   {{# def.definitions }}
{{# def.errors }}
{{# def.setupKeyword }}
{{# def.$data }}

{{## def.setExclusiveLimit:
  $exclusive = true;
  $errorKeyword = $exclusiveKeyword;
  $errSchemaPath = it.errSchemaPath + '/' + $exclusiveKeyword;
#}}

{{
  var $isMax = $keyword == 'maximum'
    , $exclusiveKeyword = $isMax ? 'exclusiveMaximum' : 'exclusiveMinimum'
    , $schemaExcl = it.schema[$exclusiveKeyword]
    , $isDataExcl = it.opts.$data && $schemaExcl && $schemaExcl.$data
    , $op = $isMax ? '<' : '>'
    , $notOp = $isMax ? '>' : '<'
    , $errorKeyword = undefined;
}}

{{? $isDataExcl }}
  {{
    var $schemaValueExcl = it.util.getData($schemaExcl.$data, $dataLvl, it.dataPathArr)
      , $exclusive = 'exclusive' + $lvl
      , $exclType = 'exclType' + $lvl
      , $exclIsNumber = 'exclIsNumber' + $lvl
      , $opExpr = 'op' + $lvl
      , $opStr = '\' + ' + $opExpr + ' + \'';
  }}
  var schemaExcl{{=$lvl}} = {{=$schemaValueExcl}};
  {{ $schemaValueExcl = 'schemaExcl' + $lvl; }}

  var {{=$exclusive}};
  var {{=$exclType}} = typeof {{=$schemaValueExcl}};
  if ({{=$exclType}} != 'boolean' && {{=$exclType}} != 'undefined' && {{=$exclType}} != 'number') {
    {{ var $errorKeyword = $exclusiveKeyword; }}
    {{# def.error:'_exclusiveLimit' }}
  } else if ({{# def.$dataNotType:'number' }}
            {{=$exclType}} == 'number'
              ? (
                  ({{=$exclusive}} = {{=$schemaValue}} === undefined || {{=$schemaValueExcl}} {{=$op}}= {{=$schemaValue}})
                    ? {{=$data}} {{=$notOp}}= {{=$schemaValueExcl}}
                    : {{=$data}} {{=$notOp}} {{=$schemaValue}}
                )
              : (
                  ({{=$exclusive}} = {{=$schemaValueExcl}} === true)
                    ? {{=$data}} {{=$notOp}}= {{=$schemaValue}}
                    : {{=$data}} {{=$notOp}} {{=$schemaValue}}
                )
            || {{=$data}} !== {{=$data}}) {
    var op{{=$lvl}} = {{=$exclusive}} ? '{{=$op}}' : '{{=$op}}=';
{{??}}
  {{
    var $exclIsNumber = typeof $schemaExcl == 'number'
      , $opStr = $op;  /*used in error*/
  }}

  {{? $exclIsNumber && $isData }}
    {{ var $opExpr = '\'' + $opStr + '\''; /*used in error*/ }}
    if ({{# def.$dataNotType:'number' }}
        ( {{=$schemaValue}} === undefined
          || {{=$schemaExcl}} {{=$op}}= {{=$schemaValue}}
            ? {{=$data}} {{=$notOp}}= {{=$schemaExcl}}
            : {{=$data}} {{=$notOp}} {{=$schemaValue}} )
        || {{=$data}} !== {{=$data}}) {
  {{??}}
    {{
      if ($exclIsNumber && $schema === undefined) {
          {{# def.setExclusiveLimit }}
          $schemaValue = $schemaExcl;
          $notOp += '=';
      } else {
        if ($exclIsNumber)
          $schemaValue = Math[$isMax ? 'min' : 'max']($schemaExcl, $schema);

        if ($schemaExcl === ($exclIsNumber ? $schemaValue : true)) {
          {{# def.setExclusiveLimit }}
          $notOp += '=';
        } else {
          $exclusive = false;
          $opStr += '=';
        }
      }

      var $opExpr = '\'' + $opStr + '\''; /*used in error*/
    }}

    if ({{# def.$dataNotType:'number' }}
        {{=$data}} {{=$notOp}} {{=$schemaValue}}
        || {{=$data}} !== {{=$data}}) {
  {{?}}
{{?}}
    {{ $errorKeyword = $errorKeyword || $keyword; }}
    {{# def.error:'_limit' }}
  } {{? $breakOnError }} else { {{?}}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     var defaults = require('./'),
    test = require('tap').test;

test("ensure options is an object", function(t) {
  var options = defaults(false, { a : true });
  t.ok(options.a);
  t.end()
});

test("ensure defaults override keys", function(t) {
  var result = defaults({}, { a: false, b: true });
  t.ok(result.b, 'b merges over undefined');
  t.equal(result.a, false, 'a merges over undefined');
  t.end();
});

test("ensure defined keys are not overwritten", function(t) {
  var result = defaults({ b: false }, { a: false, b: true });
  t.equal(result.b, false, 'b not merged');
  t.equal(result.a, false, 'a merges over undefined');
  t.end();
});

test("ensure defaults clone nested objects", function(t) {
  var d = { a: [1,2,3], b: { hello : 'world' } };
  var result = defaults({}, d);
  t.equal(result.a.length, 3, 'objects should be clones');
  t.ok(result.a !== d.a, 'objects should be clones');

  t.equal(Object.keys(result.b).length, 1, 'objects should be clones');
  t.ok(result.b !== d.b, 'objects should be clones');
  t.end();
});

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      [![npm](https://img.shields.io/npm/v/npx.svg)](https://npm.im/npx) [![license](https://img.shields.io/npm/l/npx.svg)](https://npm.im/npx) [![Travis](https://img.shields.io/travis/zkat/npx.svg)](https://travis-ci.org/zkat/npx) [![AppVeyor](https://ci.appveyor.com/api/projects/status/github/zkat/npx?svg=true)](https://ci.appveyor.com/project/zkat/npx) [![Coverage Status](https://coveralls.io/repos/github/zkat/npx/badge.svg?branch=latest)](https://coveralls.io/github/zkat/npx?branch=latest)

# npx(1) -- execute npm package binaries

## SYNOPSIS

`npx [options] <command>[@version] [command-arg]...`

`npx [options] [-p|--package <pkg>]... <command> [command-arg]...`

`npx [options] -c '<command-string>'`

`npx --shell-auto-fallback [shell]`

## INSTALL

`npm install -g npx`

## DESCRIPTION

Executes `<command>` either from a local `node_modules/.bin`, or from a central cache, installing any packages needed in order for `<command>` to run.

By default, `npx` will check whether `<command>` exists in `$PATH`, or in the local project binaries, and execute that. If `<command>` is not found, it will be installed prior to execution.

Unless a `--package` option is specified, `npx` will try to guess the name of the binary to invoke depending on the specifier provided. All package specifiers understood by `npm` may be used with `npx`, including git specifiers, remote tarballs, local directories, or scoped packages.

If a full specifier is included, or if `--package` is used, npx will always use a freshly-installed, temporary version of the package. This can also be forced with the `--ignore-existing` flag.

* `-p, --package <package>` - define the package to be installed. This defaults to the value of `<command>`. This is only needed for packages with multiple binaries if you want to call one of the other executables, or where the binary name does not match the package name. If this option is provided `<command>` will be executed as-is, without interpreting `@version` if it's there. Multiple `--package` options may be provided, and all the packages specified will be installed.

* `--no-install` - If passed to `npx`, it will only try to run `<command>` if it already exists in the current path or in `$prefix/node_modules/.bin`. It won't try to install missing commands.

* `--cache <path>` - set the location of the npm cache. Defaults to npm's own cache settings.

* `--userconfig <path>` - path to the user configuration file to pass to npm. Defaults to whatever npm's current default is.

* `-c <string>` - Execute `<string>` inside an `npm run-script`-like shell environment, with all the usual environment variables available. Only the first item in `<string>` will be automatically used as `<command>`. Any others _must_ use `-p`.

* `--shell <string>` - The shell to invoke the command with, if any.

* `--shell-auto-fallback [<shell>]` - Generates shell code to override your shell's "command not found" handler with one that calls `npx`. Tries to figure out your shell, or you can pass its name (either `bash`, `fish`, or `zsh`) as an option. See below for how to install.

* `--ignore-existing` - If this flag is set, npx will not look in `$PATH`, or in the current package's `node_modules/.bin` for an existing version before deciding whether to install. Binaries in those paths will still be available for execution, but will be shadowed by any packages requested by this install.

* `-q, --quiet` - Suppressed any output from npx itself (progress bars, error messages, install reports). Subcommand output itself will not be silenced.

* `-n, --node-arg` - Extra node argument to supply to node when binary is a node script. You can supply this option multiple times to add more arguments.

* `-v, --version` - Show the current npx version.

## EXAMPLES

### Running a project-local bin

```
$ npm i -D webpack
$ npx webpack ...
```

### One-off invocation without local installation

```
$ npm rm webpack
$ npx webpack -- ...
$ cat package.json
...webpack not in "devDependencies"...
```

### Invoking a command from a github repository

```
$ npx github:piuccio/cowsay
...or...
$ npx git+ssh://my.hosted.git:cowsay.git#semver:^1
...etc...
```

### Execute a full shell command using one npx call w/ multiple packages

```
$ npx -p lolcatjs -p cowsay -c \
  'echo "$npm_package_name@$npm_package_version" | cowsay | lolcatjs'
...
 _____
< your-cool-package@1.2.3 >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

### Run node binary with --inspect

```
$ npx --node-arg=--inspect cowsay
Debugger listening on ws://127.0.0.1:9229/....
```

### Specify a node version to run npm scripts (or anything else!)

```
npx -p node@8 npm run build
```

## SHELL AUTO FALLBACK

You can configure `npx` to run as your default fallback command when you type something in the command line with an `@` but the command is not found. This includes installing packages that were not found in the local prefix either.

For example:

```
$ npm@4 --version
(stderr) npm@4 not found. Trying with npx...
4.6.1
$ asdfasdfasf
zsh: command not found: asfdasdfasdf
```

Currently, `zsh`, `bash` (>= 4), and `fish` are supported. You can access these completion scripts using `npx --shell-auto-fallback <shell>`.

To install permanently, add the relevant line below to your `~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`, or as needed. To install just for the shell session, simply run the line.

You can optionally pass through `--no-install` when generating the fallback to prevent it from installing packages if the command is missing.

### For bash@>=4:

```
$ source <(npx --shell-auto-fallback bash)
```

### For zsh:

```
$ source <(npx --shell-auto-fallback zsh)
```

### For fish:

```
$ source (npx --shell-auto-fallback fish | psub)
```

## ACKNOWLEDGEMENTS

Huge thanks to [Kwyn Meagher](https://blog.kwyn.io) for generously donating the package name in the main npm registry. Previously `npx` was used for a Tessel board Neopixels library, which can now be found under [`npx-tessel`](https://npm.im/npx-tessel).

## AUTHOR

Written by [Kat Marchan](https://github.com/zkat).

## REPORTING BUGS

Please file any relevant issues [on Github.](https://github.com/zkat/npx)

## LICENSE

This work is released by its authors into the public domain under CC0-1.0. See `LICENSE.md` for details.

## SEE ALSO

* `npm(1)`
* `npm-run-script(1)`
* `npm-config(7)`
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            var tape = require('tape')
var through = require('through2')
var pumpify = require('./')
var stream = require('stream')
var duplexify = require('duplexify')

tape('basic', function(t) {
  t.plan(3)

  var pipeline = pumpify(
    through(function(data, enc, cb) {
      t.same(data.toString(), 'hello')
      cb(null, data.toString().toUpperCase())
    }),
    through(function(data, enc, cb) {
      t.same(data.toString(), 'HELLO')
      cb(null, data.toString().toLowerCase())
    })
  )

  pipeline.write('hello')
  pipeline.on('data', function(data) {
    t.same(data.toString(), 'hello')
    t.end()
  })
})

tape('3 times', function(t) {
  t.plan(4)

  var pipeline = pumpify(
    through(function(data, enc, cb) {
      t.same(data.toString(), 'hello')
      cb(null, data.toString().toUpperCase())
    }),
    through(function(data, enc, cb) {
      t.same(data.toString(), 'HELLO')
      cb(null, data.toString().toLowerCase())
    }),
    through(function(data, enc, cb) {
      t.same(data.toString(), 'hello')
      cb(null, data.toString().toUpperCase())
    })
  )

  pipeline.write('hello')
  pipeline.on('data', function(data) {
    t.same(data.toString(), 'HELLO')
    t.end()
  })
})

tape('destroy', function(t) {
  var test = through()
  test.destroy = function() {
    t.ok(true)
    t.end()
  }

  var pipeline = pumpify(through(), test)

  pipeline.destroy()
})

tape('close', function(t) {
  var test = through()
  var pipeline = pumpify(through(), test)

  pipeline.on('error', function(err) {
    t.same(err.message, 'lol')
    t.end()
  })

  test.emit('error', new Error('lol'))
})

tape('end waits for last one', function(t) {
  var ran = false

  var a = through()
  var b = through()
  var c = through(function(data, enc, cb) {
    setTimeout(function() {
      ran = true
      cb()
    }, 100)
  })

  var pipeline = pumpify(a, b, c)

  pipeline.write('foo')
  pipeline.end(function() {
    t.ok(ran)
    t.end()
  })

  t.ok(!ran)
})

tape('always wait for finish', function(t) {
  var a = new stream.Readable()
  a._read = function() {}
  a.push('hello')

  var pipeline = pumpify(a, through(), through())
  var ran = false

  pipeline.on('finish', function() {
    t.ok(ran)
    t.end()
  })

  setTimeout(function() {
    ran = true
    a.push(null)
  }, 100)
})

tape('async', function(t) {
  var pipeline = pumpify()

  t.plan(4)

  pipeline.write('hello')
  pipeline.on('data', function(data) {
    t.same(data.toString(), 'HELLO')
    t.end()
  })

  setTimeout(function() {
    pipeline.setPipeline(
      through(function(data, enc, cb) {
        t.same(data.toString(), 'hello')
        cb(null, data.toString().toUpperCase())
      }),
      through(function(data, enc, cb) {
        t.same(data.toString(), 'HELLO')
        cb(null, data.toString().toLowerCase())
      }),
      through(function(data, enc, cb) {
        t.same(data.toString(), 'hello')
        cb(null, data.toString().toUpperCase())
      })
    )
  }, 100)
})

tape('early destroy', function(t) {
  var a = through()
  var b = through()
  var c = through()

  b.destroy = function() {
    t.ok(true)
    t.end()
  }

  var pipeline = pumpify()

  pipeline.destroy()
  setTimeout(function() {
    pipeline.setPipeline(a, b, c)
  }, 100)
})

tape('preserves error', function (t) {
  var a = through()
  var b = through(function (data, enc, cb) {
    cb(new Error('stop'))
  })
  var c = through()
  var s = pumpify()

  s.on('error', function (err) {
    t.same(err.message, 'stop')
    t.end()
  })

  s.setPipeline(a, b, c)
  s.resume()
  s.write('hi')
})

tape('preserves error again', function (t) {
  var ws = new stream.Writable()
  var rs = new stream.Readable({highWaterMark: 16})

  ws._write = function (data, enc, cb) {
    cb(null)
  }

  rs._read = function () {
    process.nextTick(function () {
      rs.push('hello world')
    })
  }

  var pumpifyErr = pumpify(
    through(),
    through(function(chunk, _, cb) {
      cb(new Error('test'))
    }),
    ws
  )

  rs.pipe(pumpifyErr)
    .on('error', function (err) {
      t.ok(err)
      t.ok(err.message !== 'premature close', 'does not close with premature close')
      t.end()
    })
})

tape('returns error from duplexify', function (t) {
  var a = through()
  var b = duplexify()
  var s = pumpify()

  s.setPipeline(a, b)

  s.on('error', function (err) {
    t.same(err.message, 'stop')
    t.end()
  })

  s.write('data')
  // Test passes if `.end()` is not called
  s.end()

  b.setWritable(through())

  setImmediate(function () {
    b.destroy(new Error('stop'))
  })
})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        !function(r){"use strict";function t(r,t,n,e){r[t]=n>>24&255,r[t+1]=n>>16&255,r[t+2]=n>>8&255,r[t+3]=255&n,r[t+4]=e>>24&255,r[t+5]=e>>16&255,r[t+6]=e>>8&255,r[t+7]=255&e}function n(r,t,n,e,o){var i,h=0;for(i=0;i<o;i++)h|=r[t+i]^n[e+i];return(1&h-1>>>8)-1}function e(r,t,e,o){return n(r,t,e,o,16)}function o(r,t,e,o){return n(r,t,e,o,32)}function i(r,t,n,e){for(var o,i=255&e[0]|(255&e[1])<<8|(255&e[2])<<16|(255&e[3])<<24,h=255&n[0]|(255&n[1])<<8|(255&n[2])<<16|(255&n[3])<<24,a=255&n[4]|(255&n[5])<<8|(255&n[6])<<16|(255&n[7])<<24,f=255&n[8]|(255&n[9])<<8|(255&n[10])<<16|(255&n[11])<<24,s=255&n[12]|(255&n[13])<<8|(255&n[14])<<16|(255&n[15])<<24,c=255&e[4]|(255&e[5])<<8|(255&e[6])<<16|(255&e[7])<<24,u=255&t[0]|(255&t[1])<<8|(255&t[2])<<16|(255&t[3])<<24,y=255&t[4]|(255&t[5])<<8|(255&t[6])<<16|(255&t[7])<<24,l=255&t[8]|(255&t[9])<<8|(255&t[10])<<16|(255&t[11])<<24,w=255&t[12]|(255&t[13])<<8|(255&t[14])<<16|(255&t[15])<<24,p=255&e[8]|(255&e[9])<<8|(255&e[10])<<16|(255&e[11])<<24,v=255&n[16]|(255&n[17])<<8|(255&n[18])<<16|(255&n[19])<<24,b=255&n[20]|(255&n[21])<<8|(255&n[22])<<16|(255&n[23])<<24,g=255&n[24]|(255&n[25])<<8|(255&n[26])<<16|(255&n[27])<<24,_=255&n[28]|(255&n[29])<<8|(255&n[30])<<16|(255&n[31])<<24,A=255&e[12]|(255&e[13])<<8|(255&e[14])<<16|(255&e[15])<<24,d=i,U=h,E=a,x=f,M=s,m=c,B=u,S=y,K=l,T=w,Y=p,k=v,L=b,z=g,R=_,P=A,O=0;O<20;O+=2)o=d+L|0,M^=o<<7|o>>>25,o=M+d|0,K^=o<<9|o>>>23,o=K+M|0,L^=o<<13|o>>>19,o=L+K|0,d^=o<<18|o>>>14,o=m+U|0,T^=o<<7|o>>>25,o=T+m|0,z^=o<<9|o>>>23,o=z+T|0,U^=o<<13|o>>>19,o=U+z|0,m^=o<<18|o>>>14,o=Y+B|0,R^=o<<7|o>>>25,o=R+Y|0,E^=o<<9|o>>>23,o=E+R|0,B^=o<<13|o>>>19,o=B+E|0,Y^=o<<18|o>>>14,o=P+k|0,x^=o<<7|o>>>25,o=x+P|0,S^=o<<9|o>>>23,o=S+x|0,k^=o<<13|o>>>19,o=k+S|0,P^=o<<18|o>>>14,o=d+x|0,U^=o<<7|o>>>25,o=U+d|0,E^=o<<9|o>>>23,o=E+U|0,x^=o<<13|o>>>19,o=x+E|0,d^=o<<18|o>>>14,o=m+M|0,B^=o<<7|o>>>25,o=B+m|0,S^=o<<9|o>>>23,o=S+B|0,M^=o<<13|o>>>19,o=M+S|0,m^=o<<18|o>>>14,o=Y+T|0,k^=o<<7|o>>>25,o=k+Y|0,K^=o<<9|o>>>23,o=K+k|0,T^=o<<13|o>>>19,o=T+K|0,Y^=o<<18|o>>>14,o=P+R|0,L^=o<<7|o>>>25,o=L+P|0,z^=o<<9|o>>>23,o=z+L|0,R^=o<<13|o>>>19,o=R+z|0,P^=o<<18|o>>>14;d=d+i|0,U=U+h|0,E=E+a|0,x=x+f|0,M=M+s|0,m=m+c|0,B=B+u|0,S=S+y|0,K=K+l|0,T=T+w|0,Y=Y+p|0,k=k+v|0,L=L+b|0,z=z+g|0,R=R+_|0,P=P+A|0,r[0]=d>>>0&255,r[1]=d>>>8&255,r[2]=d>>>16&255,r[3]=d>>>24&255,r[4]=U>>>0&255,r[5]=U>>>8&255,r[6]=U>>>16&255,r[7]=U>>>24&255,r[8]=E>>>0&255,r[9]=E>>>8&255,r[10]=E>>>16&255,r[11]=E>>>24&255,r[12]=x>>>0&255,r[13]=x>>>8&255,r[14]=x>>>16&255,r[15]=x>>>24&255,r[16]=M>>>0&255,r[17]=M>>>8&255,r[18]=M>>>16&255,r[19]=M>>>24&255,r[20]=m>>>0&255,r[21]=m>>>8&255,r[22]=m>>>16&255,r[23]=m>>>24&255,r[24]=B>>>0&255,r[25]=B>>>8&255,r[26]=B>>>16&255,r[27]=B>>>24&255,r[28]=S>>>0&255,r[29]=S>>>8&255,r[30]=S>>>16&255,r[31]=S>>>24&255,r[32]=K>>>0&255,r[33]=K>>>8&255,r[34]=K>>>16&255,r[35]=K>>>24&255,r[36]=T>>>0&255,r[37]=T>>>8&255,r[38]=T>>>16&255,r[39]=T>>>24&255,r[40]=Y>>>0&255,r[41]=Y>>>8&255,r[42]=Y>>>16&255,r[43]=Y>>>24&255,r[44]=k>>>0&255,r[45]=k>>>8&255,r[46]=k>>>16&255,r[47]=k>>>24&255,r[48]=L>>>0&255,r[49]=L>>>8&255,r[50]=L>>>16&255,r[51]=L>>>24&255,r[52]=z>>>0&255,r[53]=z>>>8&255,r[54]=z>>>16&255,r[55]=z>>>24&255,r[56]=R>>>0&255,r[57]=R>>>8&255,r[58]=R>>>16&255,r[59]=R>>>24&255,r[60]=P>>>0&255,r[61]=P>>>8&255,r[62]=P>>>16&255,r[63]=P>>>24&255}function h(r,t,n,e){for(var o,i=255&e[0]|(255&e[1])<<8|(255&e[2])<<16|(255&e[3])<<24,h=255&n[0]|(255&n[1])<<8|(255&n[2])<<16|(255&n[3])<<24,a=255&n[4]|(255&n[5])<<8|(255&n[6])<<16|(255&n[7])<<24,f=255&n[8]|(255&n[9])<<8|(255&n[10])<<16|(255&n[11])<<24,s=255&n[12]|(255&n[13])<<8|(255&n[14])<<16|(255&n[15])<<24,c=255&e[4]|(255&e[5])<<8|(255&e[6])<<16|(255&e[7])<<24,u=255&t[0]|(255&t[1])<<8|(255&t[2])<<16|(255&t[3])<<24,y=255&t[4]|(255&t[5])<<8|(255&t[6])<<16|(255&t[7])<<24,l=255&t[8]|(255&t[9])<<8|(255&t[10])<<16|(255&t[11])<<24,w=255&t[12]|(255&t[13])<<8|(255&t[14])<<16|(255&t[15])<<24,p=255&e[8]|(255&e[9])<<8|(255&e[10])<<16|(255&e[11])<<24,v=255&n[16]|(255&n[17])<<8|(255&n[18])<<16|(255&n[19])<<24,b=255&n[20]|(255&n[21])<<8|(255&n[22])<<16|(255&n[23])<<24,g=255&n[24]|(255&n[25])<<8|(255&n[26])<<16|(255&n[27])<<24,_=255&n[28]|(255&n[29])<<8|(255&n[30])<<16|(255&n[31])<<24,A=255&e[12]|(255&e[13])<<8|(255&e[14])<<16|(255&e[15])<<24,d=i,U=h,E=a,x=f,M=s,m=c,B=u,S=y,K=l,T=w,Y=p,k=v,L=b,z=g,R=_,P=A,O=0;O<20;O+=2)o=d+L|0,M^=o<<7|o>>>25,o=M+d|0,K^=o<<9|o>>>23,o=K+M|0,L^=o<<13|o>>>19,o=L+K|0,d^=o<<18|o>>>14,o=m+U|0,T^=o<<7|o>>>25,o=T+m|0,z^=o<<9|o>>>23,o=z+T|0,U^=o<<13|o>>>19,o=U+z|0,m^=o<<18|o>>>14,o=Y+B|0,R^=o<<7|o>>>25,o=R+Y|0,E^=o<<9|o>>>23,o=E+R|0,B^=o<<13|o>>>19,o=B+E|0,Y^=o<<18|o>>>14,o=P+k|0,x^=o<<7|o>>>25,o=x+P|0,S^=o<<9|o>>>23,o=S+x|0,k^=o<<13|o>>>19,o=k+S|0,P^=o<<18|o>>>14,o=d+x|0,U^=o<<7|o>>>25,o=U+d|0,E^=o<<9|o>>>23,o=E+U|0,x^=o<<13|o>>>19,o=x+E|0,d^=o<<18|o>>>14,o=m+M|0,B^=o<<7|o>>>25,o=B+m|0,S^=o<<9|o>>>23,o=S+B|0,M^=o<<13|o>>>19,o=M+S|0,m^=o<<18|o>>>14,o=Y+T|0,k^=o<<7|o>>>25,o=k+Y|0,K^=o<<9|o>>>23,o=K+k|0,T^=o<<13|o>>>19,o=T+K|0,Y^=o<<18|o>>>14,o=P+R|0,L^=o<<7|o>>>25,o=L+P|0,z^=o<<9|o>>>23,o=z+L|0,R^=o<<13|o>>>19,o=R+z|0,P^=o<<18|o>>>14;r[0]=d>>>0&255,r[1]=d>>>8&255,r[2]=d>>>16&255,r[3]=d>>>24&255,r[4]=m>>>0&255,r[5]=m>>>8&255,r[6]=m>>>16&255,r[7]=m>>>24&255,r[8]=Y>>>0&255,r[9]=Y>>>8&255,r[10]=Y>>>16&255,r[11]=Y>>>24&255,r[12]=P>>>0&255,r[13]=P>>>8&255,r[14]=P>>>16&255,r[15]=P>>>24&255,r[16]=B>>>0&255,r[17]=B>>>8&255,r[18]=B>>>16&255,r[19]=B>>>24&255,r[20]=S>>>0&255,r[21]=S>>>8&255,r[22]=S>>>16&255,r[23]=S>>>24&255,r[24]=K>>>0&255,r[25]=K>>>8&255,r[26]=K>>>16&255,r[27]=K>>>24&255,r[28]=T>>>0&255,r[29]=T>>>8&255,r[30]=T>>>16&255,r[31]=T>>>24&255}function a(r,t,n,e){i(r,t,n,e)}function f(r,t,n,e){h(r,t,n,e)}function s(r,t,n,e,o,i,h){var f,s,c=new Uint8Array(16),u=new Uint8Array(64);for(s=0;s<16;s++)c[s]=0;for(s=0;s<8;s++)c[s]=i[s];for(;o>=64;){for(a(u,c,h,ur),s=0;s<64;s++)r[t+s]=n[e+s]^u[s];for(f=1,s=8;s<16;s++)f=f+(255&c[s])|0,c[s]=255&f,f>>>=8;o-=64,t+=64,e+=64}if(o>0)for(a(u,c,h,ur),s=0;s<o;s++)r[t+s]=n[e+s]^u[s];return 0}function c(r,t,n,e,o){var i,h,f=new Uint8Array(16),s=new Uint8Array(64);for(h=0;h<16;h++)f[h]=0;for(h=0;h<8;h++)f[h]=e[h];for(;n>=64;){for(a(s,f,o,ur),h=0;h<64;h++)r[t+h]=s[h];for(i=1,h=8;h<16;h++)i=i+(255&f[h])|0,f[h]=255&i,i>>>=8;n-=64,t+=64}if(n>0)for(a(s,f,o,ur),h=0;h<n;h++)r[t+h]=s[h];return 0}function u(r,t,n,e,o){var i=new Uint8Array(32);f(i,e,o,ur);for(var h=new Uint8Array(8),a=0;a<8;a++)h[a]=e[a+16];return c(r,t,n,h,i)}function y(r,t,n,e,o,i,h){var a=new Uint8Array(32);f(a,i,h,ur);for(var c=new Uint8Array(8),u=0;u<8;u++)c[u]=i[u+16];return s(r,t,n,e,o,c,a)}function l(r,t,n,e,o,i){var h=new yr(i);return h.update(n,e,o),h.finish(r,t),0}function w(r,t,n,o,i,h){var a=new Uint8Array(16);return l(a,0,n,o,i,h),e(r,t,a,0)}function p(r,t,n,e,o){var i;if(n<32)return-1;for(y(r,0,t,0,n,e,o),l(r,16,r,32,n-32,r),i=0;i<16;i++)r[i]=0;return 0}function v(r,t,n,e,o){var i,h=new Uint8Array(32);if(n<32)return-1;if(u(h,0,32,e,o),0!==w(t,16,t,32,n-32,h))return-1;for(y(r,0,t,0,n,e,o),i=0;i<32;i++)r[i]=0;return 0}function b(r,t){var n;for(n=0;n<16;n++)r[n]=0|t[n]}function g(r){var t,n,e=1;for(t=0;t<16;t++)n=r[t]+e+65535,e=Math.floor(n/65536),r[t]=n-65536*e;r[0]+=e-1+37*(e-1)}function _(r,t,n){for(var e,o=~(n-1),i=0;i<16;i++)e=o&(r[i]^t[i]),r[i]^=e,t[i]^=e}function A(r,t){var n,e,o,i=$(),h=$();for(n=0;n<16;n++)h[n]=t[n];for(g(h),g(h),g(h),e=0;e<2;e++){for(i[0]=h[0]-65517,n=1;n<15;n++)i[n]=h[n]-65535-(i[n-1]>>16&1),i[n-1]&=65535;i[15]=h[15]-32767-(i[14]>>16&1),o=i[15]>>16&1,i[14]&=65535,_(h,i,1-o)}for(n=0;n<16;n++)r[2*n]=255&h[n],r[2*n+1]=h[n]>>8}function d(r,t){var n=new Uint8Array(32),e=new Uint8Array(32);return A(n,r),A(e,t),o(n,0,e,0)}function U(r){var t=new Uint8Array(32);return A(t,r),1&t[0]}function E(r,t){var n;for(n=0;n<16;n++)r[n]=t[2*n]+(t[2*n+1]<<8);r[15]&=32767}function x(r,t,n){for(var e=0;e<16;e++)r[e]=t[e]+n[e]}function M(r,t,n){for(var e=0;e<16;e++)r[e]=t[e]-n[e]}function m(r,t,n){var e,o,i=0,h=0,a=0,f=0,s=0,c=0,u=0,y=0,l=0,w=0,p=0,v=0,b=0,g=0,_=0,A=0,d=0,U=0,E=0,x=0,M=0,m=0,B=0,S=0,K=0,T=0,Y=0,k=0,L=0,z=0,R=0,P=n[0],O=n[1],N=n[2],C=n[3],F=n[4],I=n[5],G=n[6],Z=n[7],j=n[8],q=n[9],V=n[10],X=n[11],D=n[12],H=n[13],J=n[14],Q=n[15];e=t[0],i+=e*P,h+=e*O,a+=e*N,f+=e*C,s+=e*F,c+=e*I,u+=e*G,y+=e*Z,l+=e*j,w+=e*q,p+=e*V,v+=e*X,b+=e*D,g+=e*H,_+=e*J,A+=e*Q,e=t[1],h+=e*P,a+=e*O,f+=e*N,s+=e*C,c+=e*F,u+=e*I,y+=e*G,l+=e*Z,w+=e*j,p+=e*q,v+=e*V,b+=e*X,g+=e*D,_+=e*H,A+=e*J,d+=e*Q,e=t[2],a+=e*P,f+=e*O,s+=e*N,c+=e*C,u+=e*F,y+=e*I,l+=e*G,w+=e*Z,p+=e*j,v+=e*q,b+=e*V,g+=e*X,_+=e*D,A+=e*H,d+=e*J,U+=e*Q,e=t[3],f+=e*P,s+=e*O,c+=e*N,u+=e*C,y+=e*F,l+=e*I,w+=e*G,p+=e*Z,v+=e*j,b+=e*q,g+=e*V,_+=e*X,A+=e*D,d+=e*H,U+=e*J,E+=e*Q,e=t[4],s+=e*P,c+=e*O,u+=e*N,y+=e*C,l+=e*F,w+=e*I,p+=e*G,v+=e*Z,b+=e*j,g+=e*q,_+=e*V,A+=e*X,d+=e*D,U+=e*H,E+=e*J,x+=e*Q,e=t[5],c+=e*P,u+=e*O,y+=e*N,l+=e*C,w+=e*F,p+=e*I,v+=e*G,b+=e*Z,g+=e*j,_+=e*q,A+=e*V,d+=e*X,U+=e*D,E+=e*H,x+=e*J,M+=e*Q,e=t[6],u+=e*P,y+=e*O,l+=e*N,w+=e*C,p+=e*F,v+=e*I,b+=e*G,g+=e*Z,_+=e*j,A+=e*q,d+=e*V,U+=e*X,E+=e*D,x+=e*H,M+=e*J,m+=e*Q,e=t[7],y+=e*P,l+=e*O,w+=e*N,p+=e*C,v+=e*F,b+=e*I,g+=e*G,_+=e*Z,A+=e*j,d+=e*q,U+=e*V,E+=e*X,x+=e*D,M+=e*H,m+=e*J,B+=e*Q,e=t[8],l+=e*P,w+=e*O,p+=e*N,v+=e*C,b+=e*F,g+=e*I,_+=e*G,A+=e*Z,d+=e*j,U+=e*q,E+=e*V,x+=e*X,M+=e*D,m+=e*H,B+=e*J,S+=e*Q,e=t[9],w+=e*P,p+=e*O,v+=e*N,b+=e*C,g+=e*F,_+=e*I,A+=e*G,d+=e*Z,U+=e*j,E+=e*q,x+=e*V,M+=e*X,m+=e*D,B+=e*H,S+=e*J,K+=e*Q,e=t[10],p+=e*P,v+=e*O,b+=e*N,g+=e*C,_+=e*F,A+=e*I,d+=e*G,U+=e*Z,E+=e*j,x+=e*q,M+=e*V,m+=e*X,B+=e*D,S+=e*H,K+=e*J,T+=e*Q,e=t[11],v+=e*P,b+=e*O,g+=e*N,_+=e*C,A+=e*F,d+=e*I,U+=e*G,E+=e*Z,x+=e*j,M+=e*q,m+=e*V,B+=e*X;S+=e*D;K+=e*H,T+=e*J,Y+=e*Q,e=t[12],b+=e*P,g+=e*O,_+=e*N,A+=e*C,d+=e*F,U+=e*I,E+=e*G,x+=e*Z,M+=e*j,m+=e*q,B+=e*V,S+=e*X,K+=e*D,T+=e*H,Y+=e*J,k+=e*Q,e=t[13],g+=e*P,_+=e*O,A+=e*N,d+=e*C,U+=e*F,E+=e*I,x+=e*G,M+=e*Z,m+=e*j,B+=e*q,S+=e*V,K+=e*X,T+=e*D,Y+=e*H,k+=e*J,L+=e*Q,e=t[14],_+=e*P,A+=e*O,d+=e*N,U+=e*C,E+=e*F,x+=e*I,M+=e*G,m+=e*Z,B+=e*j,S+=e*q,K+=e*V,T+=e*X,Y+=e*D,k+=e*H,L+=e*J,z+=e*Q,e=t[15],A+=e*P,d+=e*O,U+=e*N,E+=e*C,x+=e*F,M+=e*I,m+=e*G,B+=e*Z,S+=e*j,K+=e*q,T+=e*V,Y+=e*X,k+=e*D,L+=e*H,z+=e*J,R+=e*Q,i+=38*d,h+=38*U,a+=38*E,f+=38*x,s+=38*M,c+=38*m,u+=38*B,y+=38*S,l+=38*K,w+=38*T,p+=38*Y,v+=38*k,b+=38*L,g+=38*z,_+=38*R,o=1,e=i+o+65535,o=Math.floor(e/65536),i=e-65536*o,e=h+o+65535,o=Math.floor(e/65536),h=e-65536*o,e=a+o+65535,o=Math.floor(e/65536),a=e-65536*o,e=f+o+65535,o=Math.floor(e/65536),f=e-65536*o,e=s+o+65535,o=Math.floor(e/65536),s=e-65536*o,e=c+o+65535,o=Math.floor(e/65536),c=e-65536*o,e=u+o+65535,o=Math.floor(e/65536),u=e-65536*o,e=y+o+65535,o=Math.floor(e/65536),y=e-65536*o,e=l+o+65535,o=Math.floor(e/65536),l=e-65536*o,e=w+o+65535,o=Math.floor(e/65536),w=e-65536*o,e=p+o+65535,o=Math.floor(e/65536),p=e-65536*o,e=v+o+65535,o=Math.floor(e/65536),v=e-65536*o,e=b+o+65535,o=Math.floor(e/65536),b=e-65536*o,e=g+o+65535,o=Math.floor(e/65536),g=e-65536*o,e=_+o+65535,o=Math.floor(e/65536),_=e-65536*o,e=A+o+65535,o=Math.floor(e/65536),A=e-65536*o,i+=o-1+37*(o-1),o=1,e=i+o+65535,o=Math.floor(e/65536),i=e-65536*o,e=h+o+65535,o=Math.floor(e/65536),h=e-65536*o,e=a+o+65535,o=Math.floor(e/65536),a=e-65536*o,e=f+o+65535,o=Math.floor(e/65536),f=e-65536*o,e=s+o+65535,o=Math.floor(e/65536),s=e-65536*o,e=c+o+65535,o=Math.floor(e/65536),c=e-65536*o,e=u+o+65535,o=Math.floor(e/65536),u=e-65536*o,e=y+o+65535,o=Math.floor(e/65536),y=e-65536*o,e=l+o+65535,o=Math.floor(e/65536),l=e-65536*o,e=w+o+65535,o=Math.floor(e/65536),w=e-65536*o,e=p+o+65535,o=Math.floor(e/65536),p=e-65536*o,e=v+o+65535,o=Math.floor(e/65536),v=e-65536*o,e=b+o+65535,o=Math.floor(e/65536),b=e-65536*o,e=g+o+65535,o=Math.floor(e/65536),g=e-65536*o,e=_+o+65535,o=Math.floor(e/65536),_=e-65536*o,e=A+o+65535,o=Math.floor(e/65536),A=e-65536*o,i+=o-1+37*(o-1),r[0]=i,r[1]=h,r[2]=a,r[3]=f,r[4]=s,r[5]=c,r[6]=u,r[7]=y,r[8]=l,r[9]=w,r[10]=p,r[11]=v,r[12]=b,r[13]=g;r[14]=_;r[15]=A}function B(r,t){m(r,t,t)}function S(r,t){var n,e=$();for(n=0;n<16;n++)e[n]=t[n];for(n=253;n>=0;n--)B(e,e),2!==n&&4!==n&&m(e,e,t);for(n=0;n<16;n++)r[n]=e[n]}function K(r,t){var n,e=$();for(n=0;n<16;n++)e[n]=t[n];for(n=250;n>=0;n--)B(e,e),1!==n&&m(e,e,t);for(n=0;n<16;n++)r[n]=e[n]}function T(r,t,n){var e,o,i=new Uint8Array(32),h=new Float64Array(80),a=$(),f=$(),s=$(),c=$(),u=$(),y=$();for(o=0;o<31;o++)i[o]=t[o];for(i[31]=127&t[31]|64,i[0]&=248,E(h,n),o=0;o<16;o++)f[o]=h[o],c[o]=a[o]=s[o]=0;for(a[0]=c[0]=1,o=254;o>=0;--o)e=i[o>>>3]>>>(7&o)&1,_(a,f,e),_(s,c,e),x(u,a,s),M(a,a,s),x(s,f,c),M(f,f,c),B(c,u),B(y,a),m(a,s,a),m(s,f,u),x(u,a,s),M(a,a,s),B(f,a),M(s,c,y),m(a,s,ir),x(a,a,c),m(s,s,a),m(a,c,y),m(c,f,h),B(f,u),_(a,f,e),_(s,c,e);for(o=0;o<16;o++)h[o+16]=a[o],h[o+32]=s[o],h[o+48]=f[o],h[o+64]=c[o];var l=h.subarray(32),w=h.subarray(16);return S(l,l),m(w,w,l),A(r,w),0}function Y(r,t){return T(r,t,nr)}function k(r,t){return rr(t,32),Y(r,t)}function L(r,t,n){var e=new Uint8Array(32);return T(e,n,t),f(r,tr,e,ur)}function z(r,t,n,e,o,i){var h=new Uint8Array(32);return L(h,o,i),lr(r,t,n,e,h)}function R(r,t,n,e,o,i){var h=new Uint8Array(32);return L(h,o,i),wr(r,t,n,e,h)}function P(r,t,n,e){for(var o,i,h,a,f,s,c,u,y,l,w,p,v,b,g,_,A,d,U,E,x,M,m,B,S,K,T=new Int32Array(16),Y=new Int32Array(16),k=r[0],L=r[1],z=r[2],R=r[3],P=r[4],O=r[5],N=r[6],C=r[7],F=t[0],I=t[1],G=t[2],Z=t[3],j=t[4],q=t[5],V=t[6],X=t[7],D=0;e>=128;){for(U=0;U<16;U++)E=8*U+D,T[U]=n[E+0]<<24|n[E+1]<<16|n[E+2]<<8|n[E+3],Y[U]=n[E+4]<<24|n[E+5]<<16|n[E+6]<<8|n[E+7];for(U=0;U<80;U++)if(o=k,i=L,h=z,a=R,f=P,s=O,c=N,u=C,y=F,l=I,w=G,p=Z,v=j,b=q,g=V,_=X,x=C,M=X,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=(P>>>14|j<<18)^(P>>>18|j<<14)^(j>>>9|P<<23),M=(j>>>14|P<<18)^(j>>>18|P<<14)^(P>>>9|j<<23),m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,x=P&O^~P&N,M=j&q^~j&V,m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,x=pr[2*U],M=pr[2*U+1],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,x=T[U%16],M=Y[U%16],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,A=65535&S|K<<16,d=65535&m|B<<16,x=A,M=d,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=(k>>>28|F<<4)^(F>>>2|k<<30)^(F>>>7|k<<25),M=(F>>>28|k<<4)^(k>>>2|F<<30)^(k>>>7|F<<25),m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,x=k&L^k&z^L&z,M=F&I^F&G^I&G,m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,u=65535&S|K<<16,_=65535&m|B<<16,x=a,M=p,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=A,M=d,m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,a=65535&S|K<<16,p=65535&m|B<<16,L=o,z=i,R=h,P=a,O=f,N=s,C=c,k=u,I=y,G=l,Z=w,j=p,q=v,V=b,X=g,F=_,U%16===15)for(E=0;E<16;E++)x=T[E],M=Y[E],m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=T[(E+9)%16],M=Y[(E+9)%16],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,A=T[(E+1)%16],d=Y[(E+1)%16],x=(A>>>1|d<<31)^(A>>>8|d<<24)^A>>>7,M=(d>>>1|A<<31)^(d>>>8|A<<24)^(d>>>7|A<<25),m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,A=T[(E+14)%16],d=Y[(E+14)%16],x=(A>>>19|d<<13)^(d>>>29|A<<3)^A>>>6,M=(d>>>19|A<<13)^(A>>>29|d<<3)^(d>>>6|A<<26),m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,T[E]=65535&S|K<<16,Y[E]=65535&m|B<<16;x=k,M=F,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[0],M=t[0],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[0]=k=65535&S|K<<16,t[0]=F=65535&m|B<<16,x=L,M=I,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[1],M=t[1],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[1]=L=65535&S|K<<16,t[1]=I=65535&m|B<<16,x=z,M=G,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[2],M=t[2],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[2]=z=65535&S|K<<16,t[2]=G=65535&m|B<<16,x=R,M=Z,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[3],M=t[3],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[3]=R=65535&S|K<<16,t[3]=Z=65535&m|B<<16,x=P,M=j,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[4],M=t[4],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[4]=P=65535&S|K<<16,t[4]=j=65535&m|B<<16,x=O,M=q,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[5],M=t[5],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[5]=O=65535&S|K<<16,t[5]=q=65535&m|B<<16,x=N,M=V,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[6],M=t[6],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[6]=N=65535&S|K<<16,t[6]=V=65535&m|B<<16,x=C,M=X,m=65535&M,B=M>>>16,S=65535&x,K=x>>>16,x=r[7],M=t[7],m+=65535&M,B+=M>>>16,S+=65535&x,K+=x>>>16,B+=m>>>16,S+=B>>>16,K+=S>>>16,r[7]=C=65535&S|K<<16,t[7]=X=65535&m|B<<16,D+=128,e-=128}return e}function O(r,n,e){var o,i=new Int32Array(8),h=new Int32Array(8),a=new Uint8Array(256),f=e;for(i[0]=1779033703,i[1]=3144134277,i[2]=1013904242,i[3]=2773480762,i[4]=1359893119,i[5]=2600822924,i[6]=528734635,i[7]=1541459225,h[0]=4089235720,h[1]=2227873595,h[2]=4271175723,h[3]=1595750129,h[4]=2917565137,h[5]=725511199,h[6]=4215389547,h[7]=327033209,P(i,h,n,e),e%=128,o=0;o<e;o++)a[o]=n[f-e+o];for(a[e]=128,e=256-128*(e<112?1:0),a[e-9]=0,t(a,e-8,f/536870912|0,f<<3),P(i,h,a,e),o=0;o<8;o++)t(r,8*o,i[o],h[o]);return 0}function N(r,t){var n=$(),e=$(),o=$(),i=$(),h=$(),a=$(),f=$(),s=$(),c=$();M(n,r[1],r[0]),M(c,t[1],t[0]),m(n,n,c),x(e,r[0],r[1]),x(c,t[0],t[1]),m(e,e,c),m(o,r[3],t[3]),m(o,o,ar),m(i,r[2],t[2]),x(i,i,i),M(h,e,n),M(a,i,o),x(f,i,o),x(s,e,n),m(r[0],h,a),m(r[1],s,f),m(r[2],f,a),m(r[3],h,s)}function C(r,t,n){var e;for(e=0;e<4;e++)_(r[e],t[e],n)}function F(r,t){var n=$(),e=$(),o=$();S(o,t[2]),m(n,t[0],o),m(e,t[1],o),A(r,e),r[31]^=U(n)<<7}function I(r,t,n){var e,o;for(b(r[0],er),b(r[1],or),b(r[2],or),b(r[3],er),o=255;o>=0;--o)e=n[o/8|0]>>(7&o)&1,C(r,t,e),N(t,r),N(r,r),C(r,t,e)}function G(r,t){var n=[$(),$(),$(),$()];b(n[0],fr),b(n[1],sr),b(n[2],or),m(n[3],fr,sr),I(r,n,t)}function Z(r,t,n){var e,o=new Uint8Array(64),i=[$(),$(),$(),$()];for(n||rr(t,32),O(o,t,32),o[0]&=248,o[31]&=127,o[31]|=64,G(i,o),F(r,i),e=0;e<32;e++)t[e+32]=r[e];return 0}function j(r,t){var n,e,o,i;for(e=63;e>=32;--e){for(n=0,o=e-32,i=e-12;o<i;++o)t[o]+=n-16*t[e]*vr[o-(e-32)],n=t[o]+128>>8,t[o]-=256*n;t[o]+=n,t[e]=0}for(n=0,o=0;o<32;o++)t[o]+=n-(t[31]>>4)*vr[o],n=t[o]>>8,t[o]&=255;for(o=0;o<32;o++)t[o]-=n*vr[o];for(e=0;e<32;e++)t[e+1]+=t[e]>>8,r[e]=255&t[e]}function q(r){var t,n=new Float64Array(64);for(t=0;t<64;t++)n[t]=r[t];for(t=0;t<64;t++)r[t]=0;j(r,n)}function V(r,t,n,e){var o,i,h=new Uint8Array(64),a=new Uint8Array(64),f=new Uint8Array(64),s=new Float64Array(64),c=[$(),$(),$(),$()];O(h,e,32),h[0]&=248,h[31]&=127,h[31]|=64;var u=n+64;for(o=0;o<n;o++)r[64+o]=t[o];for(o=0;o<32;o++)r[32+o]=h[32+o];for(O(f,r.subarray(32),n+32),q(f),G(c,f),F(r,c),o=32;o<64;o++)r[o]=e[o];for(O(a,r,n+64),q(a),o=0;o<64;o++)s[o]=0;for(o=0;o<32;o++)s[o]=f[o];for(o=0;o<32;o++)for(i=0;i<32;i++)s[o+i]+=a[o]*h[i];return j(r.subarray(32),s),u}function X(r,t){var n=$(),e=$(),o=$(),i=$(),h=$(),a=$(),f=$();return b(r[2],or),E(r[1],t),B(o,r[1]),m(i,o,hr),M(o,o,r[2]),x(i,r[2],i),B(h,i),B(a,h),m(f,a,h),m(n,f,o),m(n,n,i),K(n,n),m(n,n,o),m(n,n,i),m(n,n,i),m(r[0],n,i),B(e,r[0]),m(e,e,i),d(e,o)&&m(r[0],r[0],cr),B(e,r[0]),m(e,e,i),d(e,o)?-1:(U(r[0])===t[31]>>7&&M(r[0],er,r[0]),m(r[3],r[0],r[1]),0)}function D(r,t,n,e){var i,h,a=new Uint8Array(32),f=new Uint8Array(64),s=[$(),$(),$(),$()],c=[$(),$(),$(),$()];if(h=-1,n<64)return-1;if(X(c,e))return-1;for(i=0;i<n;i++)r[i]=t[i];for(i=0;i<32;i++)r[i+32]=e[i];if(O(f,r,n),q(f),I(s,c,f),G(c,t.subarray(32)),N(s,c),F(a,s),n-=64,o(t,0,a,0)){for(i=0;i<n;i++)r[i]=0;return-1}for(i=0;i<n;i++)r[i]=t[i+64];return h=n}function H(r,t){if(r.length!==br)throw new Error("bad key size");if(t.length!==gr)throw new Error("bad nonce size")}function J(r,t){if(r.length!==Er)throw new Error("bad public key size");if(t.length!==xr)throw new Error("bad secret key size")}function Q(){var r,t;for(t=0;t<arguments.length;t++)if("[object Uint8Array]"!==(r=Object.prototype.toString.call(arguments[t])))throw new TypeError("unexpected type "+r+", use Uint8Array")}function W(r){for(var t=0;t<r.length;t++)r[t]=0}var $=function(r){var t,n=new Float64Array(16);if(r)for(t=0;t<r.length;t++)n[t]=r[t];return n},rr=function(){throw new Error("no PRNG")},tr=new Uint8Array(16),nr=new Uint8Array(32);nr[0]=9;var er=$(),or=$([1]),ir=$([56129,1]),hr=$([30883,4953,19914,30187,55467,16705,2637,112,59544,30585,16505,36039,65139,11119,27886,20995]),ar=$([61785,9906,39828,60374,45398,33411,5274,224,53552,61171,33010,6542,64743,22239,55772,9222]),fr=$([54554,36645,11616,51542,42930,38181,51040,26924,56412,64982,57905,49316,21502,52590,14035,8553]),sr=$([26200,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214,26214]),cr=$([41136,18958,6951,50414,58488,44335,6150,12099,55207,15867,153,11085,57099,20417,9344,11139]),ur=new Uint8Array([101,120,112,97,110,100,32,51,50,45,98,121,116,101,32,107]),yr=function(r){this.buffer=new Uint8Array(16),this.r=new Uint16Array(10),this.h=new Uint16Array(10),this.pad=new Uint16Array(8),this.leftover=0,this.fin=0;var t,n,e,o,i,h,a,f;t=255&r[0]|(255&r[1])<<8,this.r[0]=8191&t,n=255&r[2]|(255&r[3])<<8,this.r[1]=8191&(t>>>13|n<<3),e=255&r[4]|(255&r[5])<<8,this.r[2]=7939&(n>>>10|e<<6),o=255&r[6]|(255&r[7])<<8,this.r[3]=8191&(e>>>7|o<<9),i=255&r[8]|(255&r[9])<<8,this.r[4]=255&(o>>>4|i<<12),this.r[5]=i>>>1&8190,h=255&r[10]|(255&r[11])<<8,this.r[6]=8191&(i>>>14|h<<2),a=255&r[12]|(255&r[13])<<8,this.r[7]=8065&(h>>>11|a<<5),f=255&r[14]|(255&r[15])<<8,this.r[8]=8191&(a>>>8|f<<8),this.r[9]=f>>>5&127,this.pad[0]=255&r[16]|(255&r[17])<<8,this.pad[1]=255&r[18]|(255&r[19])<<8,this.pad[2]=255&r[20]|(255&r[21])<<8,this.pad[3]=255&r[22]|(255&r[23])<<8,this.pad[4]=255&r[24]|(255&r[25])<<8,this.pad[5]=255&r[26]|(255&r[27])<<8,this.pad[6]=255&r[28]|(255&r[29])<<8,this.pad[7]=255&r[30]|(255&r[31])<<8};yr.prototype.blocks=function(r,t,n){for(var e,o,i,h,a,f,s,c,u,y,l,w,p,v,b,g,_,A,d,U=this.fin?0:2048,E=this.h[0],x=this.h[1],M=this.h[2],m=this.h[3],B=this.h[4],S=this.h[5],K=this.h[6],T=this.h[7],Y=this.h[8],k=this.h[9],L=this.r[0],z=this.r[1],R=this.r[2],P=this.r[3],O=this.r[4],N=this.r[5],C=this.r[6],F=this.r[7],I=this.r[8],G=this.r[9];n>=16;)e=255&r[t+0]|(255&r[t+1])<<8,E+=8191&e,o=255&r[t+2]|(255&r[t+3])<<8,x+=8191&(e>>>13|o<<3),i=255&r[t+4]|(255&r[t+5])<<8,M+=8191&(o>>>10|i<<6),h=255&r[t+6]|(255&r[t+7])<<8,m+=8191&(i>>>7|h<<9),a=255&r[t+8]|(255&r[t+9])<<8,B+=8191&(h>>>4|a<<12),S+=a>>>1&8191,f=255&r[t+10]|(255&r[t+11])<<8,K+=8191&(a>>>14|f<<2),s=255&r[t+12]|(255&r[t+13])<<8,T+=8191&(f>>>11|s<<5),c=255&r[t+14]|(255&r[t+15])<<8,Y+=8191&(s>>>8|c<<8),k+=c>>>5|U,u=0,y=u,y+=E*L,y+=x*(5*G),y+=M*(5*I),y+=m*(5*F),y+=B*(5*C),u=y>>>13,y&=8191,y+=S*(5*N),y+=K*(5*O),y+=T*(5*P),y+=Y*(5*R),y+=k*(5*z),u+=y>>>13,y&=8191,l=u,l+=E*z,l+=x*L,l+=M*(5*G),l+=m*(5*I),l+=B*(5*F),u=l>>>13,l&=8191,l+=S*(5*C),l+=K*(5*N),l+=T*(5*O),l+=Y*(5*P),l+=k*(5*R),u+=l>>>13,l&=8191,w=u,w+=E*R,w+=x*z,w+=M*L,w+=m*(5*G),w+=B*(5*I),u=w>>>13,w&=8191,w+=S*(5*F),w+=K*(5*C),w+=T*(5*N),w+=Y*(5*O),w+=k*(5*P),u+=w>>>13,w&=8191,p=u,p+=E*P,p+=x*R,p+=M*z,p+=m*L,p+=B*(5*G),u=p>>>13,p&=8191,p+=S*(5*I),p+=K*(5*F),p+=T*(5*C),p+=Y*(5*N),p+=k*(5*O),u+=p>>>13,p&=8191,v=u,v+=E*O,v+=x*P,v+=M*R,v+=m*z,v+=B*L,u=v>>>13,v&=8191,v+=S*(5*G),v+=K*(5*I),v+=T*(5*F),v+=Y*(5*C),v+=k*(5*N),u+=v>>>13,v&=8191,b=u,b+=E*N,b+=x*O,b+=M*P,b+=m*R,b+=B*z,u=b>>>13,b&=8191,b+=S*L,b+=K*(5*G),b+=T*(5*I),b+=Y*(5*F),b+=k*(5*C),u+=b>>>13,b&=8191,g=u,g+=E*C,g+=x*N,g+=M*O,g+=m*P,g+=B*R,u=g>>>13,g&=8191,g+=S*z,g+=K*L,g+=T*(5*G),g+=Y*(5*I),g+=k*(5*F),u+=g>>>13,g&=8191,_=u,_+=E*F,_+=x*C,_+=M*N,_+=m*O,_+=B*P,u=_>>>13,_&=8191,_+=S*R,_+=K*z,_+=T*L,_+=Y*(5*G),_+=k*(5*I),u+=_>>>13,_&=8191,A=u,A+=E*I,A+=x*F,A+=M*C,A+=m*N,A+=B*O,u=A>>>13,A&=8191,A+=S*P,A+=K*R,A+=T*z,A+=Y*L,A+=k*(5*G),u+=A>>>13,A&=8191,d=u,d+=E*G,d+=x*I,d+=M*F,d+=m*C,d+=B*N,u=d>>>13,d&=8191,d+=S*O,d+=K*P,d+=T*R,d+=Y*z,d+=k*L,u+=d>>>13,d&=8191,u=(u<<2)+u|0,u=u+y|0,y=8191&u,u>>>=13,l+=u,E=y,x=l,M=w,m=p,B=v,S=b,K=g,T=_,Y=A,k=d,t+=16,n-=16;this.h[0]=E,this.h[1]=x,this.h[2]=M,this.h[3]=m,this.h[4]=B,this.h[5]=S,this.h[6]=K,this.h[7]=T,this.h[8]=Y,this.h[9]=k},yr.prototype.finish=function(r,t){var n,e,o,i,h=new Uint16Array(10);if(this.leftover){for(i=this.leftover,this.buffer[i++]=1;i<16;i++)this.buffer[i]=0;this.fin=1,this.blocks(this.buffer,0,16)}for(n=this.h[1]>>>13,this.h[1]&=8191,i=2;i<10;i++)this.h[i]+=n,n=this.h[i]>>>13,this.h[i]&=8191;for(this.h[0]+=5*n,n=this.h[0]>>>13,this.h[0]&=8191,this.h[1]+=n,n=this.h[1]>>>13,this.h[1]&=8191,this.h[2]+=n,h[0]=this.h[0]+5,n=h[0]>>>13,h[0]&=8191,i=1;i<10;i++)h[i]=this.h[i]+n,n=h[i]>>>13,h[i]&=8191;for(h[9]-=8192,e=(1^n)-1,i=0;i<10;i++)h[i]&=e;for(e=~e,i=0;i<10;i++)this.h[i]=this.h[i]&e|h[i];for(this.h[0]=65535&(this.h[0]|this.h[1]<<13),this.h[1]=65535&(this.h[1]>>>3|this.h[2]<<10),this.h[2]=65535&(this.h[2]>>>6|this.h[3]<<7),this.h[3]=65535&(this.h[3]>>>9|this.h[4]<<4),this.h[4]=65535&(this.h[4]>>>12|this.h[5]<<1|this.h[6]<<14),this.h[5]=65535&(this.h[6]>>>2|this.h[7]<<11),this.h[6]=65535&(this.h[7]>>>5|this.h[8]<<8),this.h[7]=65535&(this.h[8]>>>8|this.h[9]<<5),o=this.h[0]+this.pad[0],this.h[0]=65535&o,i=1;i<8;i++)o=(this.h[i]+this.pad[i]|0)+(o>>>16)|0,this.h[i]=65535&o;r[t+0]=this.h[0]>>>0&255,r[t+1]=this.h[0]>>>8&255,r[t+2]=this.h[1]>>>0&255,r[t+3]=this.h[1]>>>8&255,r[t+4]=this.h[2]>>>0&255,r[t+5]=this.h[2]>>>8&255,r[t+6]=this.h[3]>>>0&255,r[t+7]=this.h[3]>>>8&255,r[t+8]=this.h[4]>>>0&255,r[t+9]=this.h[4]>>>8&255,r[t+10]=this.h[5]>>>0&255,r[t+11]=this.h[5]>>>8&255,r[t+12]=this.h[6]>>>0&255,r[t+13]=this.h[6]>>>8&255,r[t+14]=this.h[7]>>>0&255,r[t+15]=this.h[7]>>>8&255},yr.prototype.update=function(r,t,n){var e,o;if(this.leftover){for(o=16-this.leftover,o>n&&(o=n),e=0;e<o;e++)this.buffer[this.leftover+e]=r[t+e];if(n-=o,t+=o,this.leftover+=o,this.leftover<16)return;this.blocks(this.buffer,0,16),this.leftover=0}if(n>=16&&(o=n-n%16,this.blocks(r,t,o),t+=o,n-=o),n){for(e=0;e<n;e++)this.buffer[this.leftover+e]=r[t+e];this.leftover+=n}};var lr=p,wr=v,pr=[1116352408,3609767458,1899447441,602891725,3049323471,3964484399,3921009573,2173295548,961987163,4081628472,1508970993,3053834265,2453635748,2937671579,2870763221,3664609560,3624381080,2734883394,310598401,1164996542,607225278,1323610764,1426881987,3590304994,1925078388,4068182383,2162078206,991336113,2614888103,633803317,3248222580,3479774868,3835390401,2666613458,4022224774,944711139,264347078,2341262773,604807628,2007800933,770255983,1495990901,1249150122,1856431235,1555081692,3175218132,1996064986,2198950837,2554220882,3999719339,2821834349,766784016,2952996808,2566594879,3210313671,3203337956,3336571891,1034457026,3584528711,2466948901,113926993,3758326383,338241895,168717936,666307205,1188179964,773529912,1546045734,1294757372,1522805485,1396182291,2643833823,1695183700,2343527390,1986661051,1014477480,2177026350,1206759142,2456956037,344077627,2730485921,1290863460,2820302411,3158454273,3259730800,3505952657,3345764771,106217008,3516065817,3606008344,3600352804,1432725776,4094571909,1467031594,275423344,851169720,430227734,3100823752,506948616,1363258195,659060556,3750685593,883997877,3785050280,958139571,3318307427,1322822218,3812723403,1537002063,2003034995,1747873779,3602036899,195