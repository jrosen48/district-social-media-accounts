# district-social-media-accounts

## For accessing Facebook data, see the access-facebook directory

### Dependencies

`pip install facebook-scraper`

### Run

`python access.py`

### Process

Run `process-data.R`

This creates a large (~ 1.5GB) file, `processed-joined-facebook-data.csv` (ignored for this repository), with posts for approximately 6,700 districts, and a link to their NCES ID.

District NCES data is available in `nces-info-for-districts.csv`

### Extension

This could also be done for schools, which have a greater number of links to Facebook from their homepages, but have a lower proportion of all schools (relative to districts) with Facebook accounts. This is not yet processed but could be done using the `facebook-accounts-from-school-homepages.csv` fgile.

## The access-twitter files and directory are still in a draft form
