# Styleguides
## Git Commit Conventions
* Use the present tense ("Add feature" instead of "Adding feature" or "Added feature").
* Use the imperative mood ("Remove attribute" not "Removes attribute").
* Limit the first line to 72 characters or less.
* More details can be specified in the subsequent lines, *i.e.* in the body of the commit.
* Commits must be named as follows: `[Type] Description`.

### Commit Types
Consider starting the commit message with the following "types" (should be placed in brackets):
* **[_Nothing_]**: 
* **Feat**: Adding a new (important) feature
* **Fix**: a bug fix or fixing test
* **Test**: adding of new tests
* **Clean**: (re)move some files / folders
* **Refactor**: refactoring code
* **Merge**: merging commits / branches
* **Docs**: changes to the documentation

### Examples
* Simple commit without body
```
[Add] Add the possibility to create a puzzle from an image
```
* More details provided in the body of the commit
```
[Refactor] Make the code of the random solver more readable
* Add new method `eggs`
* Rename the `spam_ham` attribute to `ham_egg`
```
* Reference and close an issue reported on Github
```
**[Fix]** Fix broken test test_compatibility_matrix
Fix #5
```