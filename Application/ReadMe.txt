Building installer package on Win and Mac
=========================================

Windows
-------
Change Application/VersionNumber.txt

Build once with Qt Creator. This will compile the UI and Resource files

Run Installer/deploy.bat to create a pyinstaller package

Run Installer/Win/build_install to generate the QFW installer package.
This will also update the config/packages files with version number and date

Check in the changed files (VersionNumber.txt and updated config/packages files)


Mac
---
Make sure all the Windows steps above have been run. Get all the latest files from GitLab.
This should get you the updated UI files and the correct version information.

Note: The Mac build does not update version numbers and dates in various files. It relies on this to be processed on the Win side.

Run Installer/deploy to create a pyinstaller package

Run Installer/Mac/build_install to generate the QFW installer package

