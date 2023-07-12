bit.io database export artifact

This directory contains data exported from a bit.io database at the epoch
time shown in the parent directory's name. This export artifact was exported
using pg_dump's directory output format, with compression enabled. It can be
restored to any target database natively via pg_restore.

For more information about bit.io's sunset please visit
https://docs.bit.io/docs/sunset.

For more information on how to use pg_dump and pg_restore please visit
https://www.postgresql.org/docs/current/app-pgdump.html.

Please note that pg_dump artifacts created via pg_dump version 14 (such as this
artifact) most likely require pg_restore version 14 in order to be imported into
a target postgres database. The target postgres database most likely will also
need to be version 14.
