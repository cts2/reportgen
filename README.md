### reportgen
reportgen is a Github issue tracker reporting tool. Using the Github REST API, issues are parsed and output as a PDF.

### Usage
```
reportgen.py [-h] -u USER -r REPOS [--open] [-o OUT]
```

Parameters

```
-u (USER): Github user name
-r (REPOS): Github repository name
-o (OUT): PDF output file name
--open: When set, opens the resulting PDF automatically
```

