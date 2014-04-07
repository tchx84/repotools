Repository Tools
================

This a set of tools that helps me (and hopefully you) to manage YUM
repositories, following a testing and updates workflow.


What problems does it solve?
----------------------------

* safely upload packages to testing repositories.
* sign packages and update repositories metadata.
* deploy packages to updates, in a surpevised way.

repotools secret is a good balance between convention, configuration
and automatization.

How can I use it?
-----------------

0. Create your repository confiuration file.

    ```
    cp etc/repos.json.example etc/repos.json
    vim etc/repos.json
    ```

    As in any other testing and updates workflow, it is expected that you
    have atesting repository for each updates one,

    To make things a bit safer, you can specify filters for each repository
    such as accepted-architectures and packages keywords, repotools will
    purge whatever does not comply with your definitions.

    All steps include user confirmation so you can check what is finally
    going to impact your repositories.

1. Upload packages to a repository.

    ```
    ./upload.sh xo1 ./mock/*.rpm
    ```

    repotools will copy all the rpms in the ./mock/ directory that comply
    with the repository name xo1 and its definitions.

2. Sign packages and update repositories metadata.

    ```
    ./update.sh xo1 testing
    ```

    repotools will sign all the packages in the testing repository, and then
    it will update the repository metadata.

    Once the packages are sufficienty tested, you can deploy these packages
    to the updates final repository.

    ```
    ./update.sh xo1 updates
    ```

    In this case, repotools will find all latest versions of the packages in
    testing, that are not in updates already, and copy them to updates. The
    previous step will also purge anything that does not complies with the
    repository definition.

    Once the packages are copied to the updates repository, these packages
    will be signed and the repository metadata will be updated.

3. Done.

Tricks
------

* Update specific packages on updates repositories.

    ```
    ./update.sh xo1 updates kernel driver
    ```

    repotools will only deploy in the xo1 updates repository, packages that
    matches the kerwords "kernel" or "driver".

* Use some of the internal tools.

    ```
    ./helpers/find.py -d ~/Devel/repos -a x86_64 -s authbind
    ```

    repotools will list all packages are under ~/Devel/repos directory,
    recusively, that matches with the specified architectures and keywords.
