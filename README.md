# Space Cloud
### File management for FITS files
### Backup to S3
### FITS header editor

Description will go here.

## Technical stuff

To start, rename the `.env_example` file to `.env` end fill it in with your AWS credentials.

### paths

`/` - GET all uploads

`/new` - POST new upload

`/<pk>` - GET upload details

`/header/<pk>` - PUT update FITS file header of uploaded file

`export/<pk>` - GET export file to S3
