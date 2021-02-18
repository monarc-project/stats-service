Changelog
=========


v0.3.0 (2021-02-12)
-------------------

New
~~~
- [documentation] Added section about integration with MONARC and
  collect of the stats. [Cédric Bonhomme]
- [documentation] Added more help/information for the potential
  contributors. [Cédric Bonhomme]
- [templates] display visual data about risks. [Cédric Bonhomme]
- [views] added about_more route to the root_bp blueprint. The goal is
  to provide to a user more information about the current instance.
  [Cédric Bonhomme]
- [commamd] Added a command to purge stats older than the number of
  months specified in parameter. [Cédric Bonhomme]
- [configuration] added default wsgi file. [Cédric Bonhomme]

Changes
~~~~~~~
- [config] updated pyproject.toml and configuration for the version
  0.3.0. [Cédric Bonhomme]
- [documentation] Make the note about the collection and sharing more
  clear. [Cédric Bonhomme]
- [documentation] Added details about the security model. [Cédric
  Bonhomme]
- [documentation] Added note in architecture doc. [Cédric Bonhomme]
- [documentation] Rephrasing. [Cédric Bonhomme]
- [documentation] simplification of the presentation of the
  architecture. [Cédric Bonhomme]
- [style] Reformat web resources. [Cédric Bonhomme]
- [javascript] Moved to async function when getting infor from MOSP.
  [Cédric Bonhomme]
- [template] moving JS configuration variables in a dedicated file.
  [Cédric Bonhomme]
- [template] Charts for threats and vulnerabilities are now useing the
  averageRate values from MONARC. [Cédric Bonhomme]
- [commands] Try to improve the display of the legend. [Cédric Bonhomme]
- [commands] More responsiev charts. [Cédric Bonhomme]
- [commands] Removed debug print in commands/stats.py. [Cédric Bonhomme]
- [template] Improved stats.html template. [Cédric Bonhomme]
- [documentation] typo. [Cédric Bonhomme]
- [documentation] described how to give parameters when using the API
  (GET List on stats). [Cédric Bonhomme]
- [templates] commented the legendCallback. [Cédric Bonhomme]
- [core] Updated JavaScript dependencies. [Cédric Bonhomme]
- [core] Updated Python dependencies. [Cédric Bonhomme]
- [API] Removed debug log in processed.py. [Cédric Bonhomme]
- [misc] Updated copyright years. [Cédric Bonhomme]
- [contrib] Updated systemd ExecStart command with the link to the
  Python shim. [Cédric Bonhomme]
- [views] the route about.json now alson returns the contact email
  address. [Cédric Bonhomme]
- [template] Improved stats.html template. [Cédric Bonhomme]
- [dependencies] Updated dependencies. [Cédric Bonhomme]
- [template] Let the admin configure the addresses used in the
  about.html template. [Cédric Bonhomme]
- [template] Be more clear in the about page with intentions and how the
  system is working. [Cédric Bonhomme]
- [documentation] Updating documentation with stats_purge command
  interface. [Cédric Bonhomme]
- [template] updated about page. [Cédric Bonhomme]
- [template] minor improvements to the templates and to the CSS. [Cédric
  Bonhomme]

Fix
~~~
- Error when templating the configuration of the two bar charts. [Cédric
  Bonhomme]
- [commands] The payload of the GET request must be provided in the JSON
  payload. [Cédric Bonhomme]
- Added mising Jinja template. [Cédric Bonhomme]

Other
~~~~~
- Updated documentation. [Cédric Bonhomme]
- Updated dependencies. [Cédric Bonhomme]
- Updated documentation. [Cédric Bonhomme]
- Slight changes to bootstrap.py for the loading of the configuration.
  [Cédric Bonhomme]
- Updated poetry.lock. [Cédric Bonhomme]
- Updated README. [Cédric Bonhomme]
- Minimum version of Python is now 3.6.12. [Cédric Bonhomme]


v0.2.0 (2020-11-18)
-------------------

New
~~~
- [style] added logo sources. [Cédric Bonhomme]
- [template] added about HTML which will uses about.json endpoint.
  [Cédric Bonhomme]
- [static] added apple-touch-icon fro browsers miniatures and updated
  accordingly the layout. [Cédric Bonhomme]
- [processors] Added risk_averages_on_date processor: evaluates the
  averages for the risks per date. [Cédric Bonhomme]
- [API] Added an endpoint which lists the available processors. [Cédric
  Bonhomme]
- [processors] Trying new processor with generators to evaluates means.
  [Cédric Bonhomme]
- [utils] introduces the mean accumulator in utils.py. Usefull to
  process means of incoming series of values. [Cédric Bonhomme]
- [API] new namespace to call a postprocessor. [Cédric Bonhomme]
- [template] Added stats-async.html. [Cédric Bonhomme]
- [logging] define a proper logging function. [Cédric Bonhomme]
- [contrib] added update.sh script. [Cédric Bonhomme]
- [contrib] added set_env_vars script. [Cédric Bonhomme]
- [templates] Add default layout template with a dependency to Bootstrap
  5. [Cédric Bonhomme]
- [models] Added local boolean attribute for Client. [Cédric Bonhomme]
- [processors] wip: added threats_average_on_date function. [Cédric
  Bonhomme]
- [commands] Added a new client in order to delete a local client and
  all its related stats. [Cédric Bonhomme]
- Added contrib/install.sh for deployment with MONARC. [Cédric Bonhomme]
- [stats_bp] added view which will display visual information about
  stats. [Cédric Bonhomme]
- [documentation] Added new section about updates. [Cédric Bonhomme]

Changes
~~~~~~~
- [contrib] restored conf variable when creating new client. [Cédric
  Bonhomme]
- [contrib] restored conf variable when creating new client. [Cédric
  Bonhomme]
- [contrib] comment the lines which set the virtual env to use. [Cédric
  Bonhomme]
- [contrib] comment the lines which set configuration variables. [Cédric
  Bonhomme]
- [runtime] Updated Python runtime on Heroku to 3.8.6. [Cédric Bonhomme]
- [template] Removed OpenAPI Specification link from the navbar. [Cédric
  Bonhomme]
- [runtime] Updated Python runtime on Heroku to 3.9.0. [Cédric Bonhomme]
- [API] Restored authentication for processed namespace of the API..
  [Cédric Bonhomme]
- [style] removed useless blank line. [Cédric Bonhomme]
- [processor] added an assert on the value of the param
  processor_params. [Cédric Bonhomme]
- Updated dependencies. [Cédric Bonhomme]
- [GH workflows] Test and build the app for Python 3.9.0. [Cédric
  Bonhomme]
- [dependencies] Updated SQLAlchemy and other dependencies. [Cédric
  Bonhomme]
- [documentation] typos. [Cédric Bonhomme]
- [documentation] rephrasing. [Cédric Bonhomme]
- Added some debug logs. [Cédric Bonhomme]
- [documentation] updated documentation about processors and parameters.
  [Cédric Bonhomme]
- [documentation] Updated swagger file, [Cédric Bonhomme]
- [processor] Filter out from the result things that were not processed
  based on the params, these values are empty (set to zero) so useless
  for the client. [Cédric Bonhomme]
- [API + processors] it is now possible to pass parameters dedicated to
  the processors. [Cédric Bonhomme]
- Typo. [Cédric Bonhomme]
- [style] reformat new code. [Cédric Bonhomme]
- [processor] for the processor risk_averages_on_date the final values
  are now stored in a list of objects (date and value). [Cédric
  Bonhomme]
- [processor] for the processor risk_averages_on_date the final values
  are now stored in a list of objects (label and value). [Cédric
  Bonhomme]
- [processor] for the processor risk_averages_on_date the final values
  are now stored in a list. [Cédric Bonhomme]
- [documentation] Updated documentation with new processor. [Cédric
  Bonhomme]
- [processors] Some improvements to the risk_averages processor which is
  now using a function in order to initializes the different generators.
  [Cédric Bonhomme]
- [style] format. [Cédric Bonhomme]
- [style] format. [Cédric Bonhomme]
- [API] get anrs as a list. [Cédric Bonhomme]
- [API] the anrs argument s now in the body of the request. This is
  because we had issues with the length of the resulting URL with
  severall ANRs UUIDs as a URL parameter: UUIDs were cut. [Cédric
  Bonhomme]
- [models] convert datetime object to string in _asdict. [Cédric
  Bonhomme]
- [processors] Renamed risk_process to risk_averages. [Cédric Bonhomme]
- [documentation] Updated swagger file from the documentation. [Cédric
  Bonhomme]
- [API] Endoint api/v1/stats/processing renamed to
  api/v1/stats/processed. [Cédric Bonhomme]
- [API] cleaned new code in processing namesapce and updated
  documentation. [Cédric Bonhomme]
- [API] processing namespace, commit it's kinda working. [Cédric
  Bonhomme]
- [style] added some black magic. [Cédric Bonhomme]
- [postprocessors] The function threat_average_on_date() now processes
  the global averages of the averages per day for each threats (this is
  as well applicable to vulnerabilities). [Cédric Bonhomme]
- [template] Iterate over the values returned by the endpoint then sort
  the items per date in order to construction the options dict for the
  chart. [Cédric Bonhomme]
- [postprocessor] flatten a bit more the result of
  threat_average_on_date() [Cédric Bonhomme]
- [lib] removed useless comment. [Cédric Bonhomme]
- [postprocessor] directly use a string for the value of i, for the
  labels (labeli). [Cédric Bonhomme]
- [postprocessor] (test) provide labels after the evaluation of the
  postprocessor. [Cédric Bonhomme]
- [postprocessor] comment pop on data. [Cédric Bonhomme]
- Remove the labels just befor preparing the frames in
  postprocessors/threat_average_on_date. [Cédric Bonhomme]
- [documentation] Updated processed_data to processedData in the
  swagger.json file. [Cédric Bonhomme]
- [API] Changed case of processed_data to processedData. [Cédric
  Bonhomme]
- [dependencies] Updated pytest. [Cédric Bonhomme]
- [dependencies] Updated pygments. [Cédric Bonhomme]
- [API] in the namespace stats_ns the 'anrs' argument of the parser has
  been renamed to 'anrs[]'. [Cédric Bonhomme]
- [dependencies] Updated Numpy. [Cédric Bonhomme]
- [documentation] Updated documentation about the command line
  interface. [Cédric Bonhomme]
- [sync] Renamed parameter uuid to client-uuid. [Cédric Bonhomme]
- Updated pandas. [Cédric Bonhomme]
- [style] Format with black. [Cédric Bonhomme]
- [documentation] Updated docstrings. [Cédric Bonhomme]
- [logging] Added a logging capability for the
  statsservice.commands.stats module. [Cédric Bonhomme]
- [sync] tested and fixed stats pull command. [Cédric Bonhomme]
- [dependencies] updated psycog. [Cédric Bonhomme]
- [API] Marshall the result of a POST LIST requests with
  marshal_list_with. [Cédric Bonhomme]
- [API] returns newly created stats. [Cédric Bonhomme]
- [api] If some objects can not created we return the HTTP code 207
  (Multi-Status). If all objects of the batch POST request are created
  we simply return 204. [Cédric Bonhomme]
- [api] in case of duplicate stats rollback the session of the db with
  creating a new stat. [Cédric Bonhomme]
- [contrib] Updated install.sh. [Cédric Bonhomme]
- [documentation] Minor updated in logging.rst. [Cédric Bonhomme]
- [logging]: added a logger for statsservice.api.v1.client. [Cédric
  Bonhomme]
- [configuration] Updated default configuration files with the new
  LOG_PATH variable. [Cédric Bonhomme]
- [api] Removed useless log. [Cédric Bonhomme]
- [api] catch sqlalchemy.exc.IntegrityError,
  sqlalchemy.exc.InvalidRequestError errors. [Cédric Bonhomme]
- [API] catch psycopg2.errors.UniqueViolation errors. [Cédric Bonhomme]
- [API] import psycopg2.Error. [Cédric Bonhomme]
- [API] print integrity error code. [Cédric Bonhomme]
- [API] Do not use buld_save_objects. [Cédric Bonhomme]
- [sync] fixed dumpling of data to POST to an other stats service.
  [Cédric Bonhomme]
- [templates] Updated stats.html. [Cédric Bonhomme]
- Updated dpendencies. [Cédric Bonhomme]
- [commands] when pushing or pulling stats we must select client with
  their uuid and not their name. [Cédric Bonhomme]
- [templates] improve display of charts. [Cédric Bonhomme]
- [templates] Updated options of charts. [Cédric Bonhomme]
- [templates] Added link to MOSP instance defined in the configuration
  file. [Cédric Bonhomme]
- [stats_bp] added local_stats_only parameter for the vulnerabilities
  and threats routes. [Cédric Bonhomme]
- [deployment] Specify version of Node. [Cédric Bonhomme]
- [documentation] Added NodeJS buildpack. [Cédric Bonhomme]
- [install] updated contrib/install.sh with the npm command to install
  Chart.js. [Cédric Bonhomme]
- [template] added language parameter to the
  retrieve_information_from_mosp promise. [Cédric Bonhomme]
- [template] specify the language of the object when querying MOSP.
  [Cédric Bonhomme]
- [template] Query MOSP to translate UUID to labels in the stats
  dashboard. [Cédric Bonhomme]
- [templates] added more colors the stats dashboard. [Cédric Bonhomme]
- Refactorization. [Cédric Bonhomme]
- [documentation] Updated documentation about stats_bp blueprint.
  [Cédric Bonhomme]
- [documentation] updated swagger.json file. [Cédric Bonhomme]
- [apiv1] cleaning. [Cédric Bonhomme]
- [processors] cleaning. [Cédric Bonhomme]
- [postprocessors] Improved management of postprocessors. [Cédric
  Bonhomme]
- [stats_bp] avegare_date is the default format for the
  vulnerabilities.json route. [Cédric Bonhomme]
- [template] Improved test template for global stats. [Cédric Bonhomme]
- [processors] factorization of some methods used for threats and
  vulnerabilities since the structure of the stats for threats and
  vulnerabilities is the same. [Cédric Bonhomme]
- [documentation] Added more information about the overall interactions
  principles with MONARC. [Cédric Bonhomme]
- [documentation] Fixed cut and paste mistake. [Cédric Bonhomme]
- [documentation] updated section of the documentation related to the
  stats_bp blueprint. [Cédric Bonhomme]
- [stats_bp] updated test template and stats route. [Cédric Bonhomme]
- [processors] display the mean in a markdown table. [Cédric Bonhomme]
- [dependencies] Updated Pandas. [Cédric Bonhomme]
- [documentation] Typo. [Cédric Bonhomme]
- [contrib] change name of the command to create new local client.
  [Cédric Bonhomme]
- [documentation] minor update to the README. [Cédric Bonhomme]
- [commands] Refactored commands. [Cédric Bonhomme]
- [documentation] Installation with remote script. [Cédric Bonhomme]
- [documentation] Updated documentation with the new command. [Cédric
  Bonhomme]
- [documentation] Minor improvements. [Cédric Bonhomme]
- [commmands] catch any errors when creating new clients (this prevents
  scripts from being interrupted by an error). [Cédric Bonhomme]
- [stats_bp] added parameters mean and aggregated to the route threats.
  when requested format by the client is 'mean' the legacy behaviour is
  used, else it is aggregated. [Cédric Bonhomme]
- [documentation] Update for the stats_bp blueprint (threats.json
  endpoint) [Cédric Bonhomme]
- [documentation] renamed updates.md to updates.rst. [Cédric Bonhomme]
- [stats_bp] added nb_days URL parameter to the threats.json route.
  [Cédric Bonhomme]
- [stats_bp] Give the possibility to filter by anr, and filter with
  timedelta(weeks). [Cédric Bonhomme]
- [stats_bp] Returns the mean evaluation based on the threats. [Cédric
  Bonhomme]
- [sync] batch synchronization of stats. [Cédric Bonhomme]
- [commands] add the possibility to specify client token. [Cédric
  Bonhomme]
- [commands] removed useless import of uuid. [Cédric Bonhomme]
- [commands] add the possibility to specify UUID when creating client
  (since the name will probably be removed) [Cédric Bonhomme]
- [models] Precises the the name field for client should be deleted.
  [Cédric Bonhomme]
- [dependencies] Updated numpy. [Cédric Bonhomme]
- [dependencies] removed useless import and reformated some quotes.
  [Cédric Bonhomme]
- [dependencies] Updated MarkupSafe dependency. [Cédric Bonhomme]
- [dependencies] updated requirements.txt. [Cédric Bonhomme]
- [depoyment] Updated Heroku runtime to Python-3.8.4. [Cédric Bonhomme]
- [README] Updated contributors list. [README-bot]
- [README] Updated contributors list. [README-bot]
- [style] ignore bot. [Cédric Bonhomme]
- [style] ignore bot and reformat with black. [Cédric Bonhomme]
- [README] Updated contributors list. [README-bot]
- [README] Updated contributors list. [README-bot]
- [config] auto-generate secret_key if not found in the loaded
  configuration. [Cédric Bonhomme]
- [README] updated contributors section. [Cédric Bonhomme]

Fix
~~~
- [commands] Fixed deletion of clients via the command. [Cédric
  Bonhomme]
- [contrib] arguments checking. [Cédric Bonhomme]
- [accessibility] fixed accessibily issues. [Cédric Bonhomme]
- [template] Fixed issue in stats template: UUID are now stored os
  "object" in the response from the server. [Cédric Bonhomme]
- [API] added missing import. [Cédric Bonhomme]
- [API] Fix issue when deleting stats with ANR UUIDs. [Cédric Bonhomme]
- [processor] copy the dict of parameters passed to the processor.
  [Cédric Bonhomme]
- [documentation] typo. [Cédric Bonhomme]
- [documentation] typo. [Cédric Bonhomme]
- [bootstrap] processing has been renamed to processed. [Cédric
  Bonhomme]
- [template] stats template broken due to change in data format or the
  processor. [Cédric Bonhomme]
- [processors] renamed old variable. [Cédric Bonhomme]
- The fix. [Cédric Bonhomme]
- [API] object of type BaseQuery has no len() [Cédric Bonhomme]
- [postprocessor] check if the value is not None (null) before storing
  it for the client. [Cédric Bonhomme]
- [bootstrap] Check if LOG_PATH is defined. [Cédric Bonhomme]
- [sync] fixed client SQLAlchemy query. [Cédric Bonhomme]
- [stats_bp] query was not defined before use. [Cédric Bonhomme]
- [processors] mean values per threat were overwritten in the loop.
  [Cédric Bonhomme]
- [README] wrong script name. [Cédric Bonhomme]

Other
~~~~~
- Bumping version from 0.1.10 to 0.2.0. [Cédric Bonhomme]
- Export conf variable for flask cli. [Cédric Bonhomme]
- Added create_client.sh script. [Cédric Bonhomme]
- Added create_client.sh script. [Cédric Bonhomme]
- Chg [contrib] Installation of a recent Python with pyenv when
  installing Stats Service. [Cédric Bonhomme]
- Random generation of the database password when installing stats-
  service. [Cédric Bonhomme]
- Force use of Python >= 3.8. [Cédric Bonhomme]
- Removed reverse param in sort function. [Juan Rocha]
- Added sort by date in risk_averages_on_date() [Juan Rocha]
- Renamed type to stat_type and check if processorParams is not None.
  [Cédric Bonhomme]
- Updated numpy. [Cédric Bonhomme]
- Cleaning. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Removed the trace info. [Ruslan Baidan]
- Added the endpoint to get logged in client details. [Ruslan Baidan]
- Fixed merge conflicts. [Cédric Bonhomme]
- Added the reponse format definition. [Ruslan Baidan]
- Merge branch 'master' of https://github.com/monarc-project/stats-
  service. [Ruslan Baidan]

  * 'master' of https://github.com/monarc-project/stats-service:
    chg: [processors] Some improvements to the risk_averages processor which is now using a function in order to initializes the different generators.
    chg: [style] format.
    chg: [style] format.
    new: [processors] Trying new processor with generators to evaluates means.
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Added some extra params to the result. [Ruslan Baidan]
- Optimized the code to increase perfomance. [Ruslan Baidan]
- Optimized the processing of the threats and vulnerabilities, changed
  the response format. [Ruslan Baidan]
- Restored the default value. [Ruslan Baidan]
- Changed the default value of local stats. [Ruslan Baidan]
- Fixed the type param. [Ruslan Baidan]
- Fixed the anrs param. [Ruslan Baidan]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Reverted the anrs getting from args. [Ruslan Baidan]
- Fixed swagger. [Ruslan Baidan]
- Replaced the anrs list fetching from the request. [Ruslan Baidan]
- Attempt to get the passed body pararms from json. [Ruslan Baidan]
- Added the `anrs` param to the processed stats endpoint, and replaced
  the endpoint to the `post` method. [Ruslan Baidan]
- Fis: [API] Added missing file. [Cédric Bonhomme]
- Cleaned up the processor things from /stats endpoint and renamed
  "postprocessor" to "processor". [Ruslan Baidan]
- Add date as property. [Juan Rocha]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Removed the extra param in result of stats creation. [Ruslan Baidan]
- Reverted the anrs param change. [Ruslan Baidan]
- Chg; [documentation] Updated logging.rst. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Updated README. [Cédric Bonhomme]
- New" [documentation] Added information about the logging capacities.
  [Cédric Bonhomme]
- Chg [logging] Improved format of the logger. [Cédric Bonhomme]
- Typo. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Create codeql-analysis.yml. [Cedric]
- Added NodeJS Heroku buildpack. [Cédric Bonhomme]
- Updated Heroku Python runtime. [Cédric Bonhomme]
- Updated dependencies (SQLAlchemy and Pandas). [Cédric Bonhomme]
- Removed useless comment. [Cédric Bonhomme]
- Updated comments. [Cédric Bonhomme]
- Removed useless imports. [Cédric Bonhomme]
- Bugfix. [Cédric Bonhomme]
- Test: fetch inforation about previously retrieved threats from MOSP.
  [Cédric Bonhomme]
- Dramatic improvement. [Cédric Bonhomme]
- Various improvements and fixes. [Cédric Bonhomme]
- Removed useless print. [Cédric Bonhomme]
- Removed tests. [Cédric Bonhomme]
- Fixed the limit to 0. [Ruslan Baidan]
- Added the functionality to get the last records of the stats for
  multiple anrs. [Ruslan Baidan]
- Fixed the mistake. [Ruslan Baidan]
- Added the argument to get the last record of the stats. [Ruslan
  Baidan]
- Every 4 hours. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Fixed the authuntication issue when the key is not correct. [Ruslan
  Baidan]
- Added a secret key. [Ruslan Baidan]


v0.1.10 (2020-07-16)
--------------------

New
~~~
- [actions] publish on release creation. [Cédric Bonhomme]
- [api] added identity.py which uses Flask_Principal for the management
  of roles/permissions. [Cédric Bonhomme]
- [documentation] Documented the new route for the version checking.
  [Cédric Bonhomme]
- [root blueprint] added a route to check the version of the service.
  [Cédric Bonhomme]

Changes
~~~~~~~
- Bump version number to test the publish workflow. [Cédric Bonhomme]
- [tests] testing auto publish. [Cédric Bonhomme]
- [tests] Replaced Python 3.6.7 by Python 3.6.11. [Cédric Bonhomme]
- [tests] Python 3.6.1 is not available on GitHub Action. [Cédric
  Bonhomme]
- [tests] use a matrix strategy for the Python GitHub Action. [Cédric
  Bonhomme]
- [models] renamed function name my_secret to secret_token. [Cédric
  Bonhomme]
- [tests] uncomment lint tests. [Cédric Bonhomme]
- [tests] temporary cmment lint tests. [Cédric Bonhomme]
- [tests] updated GitHub Actions workflow for the tests. [Cédric
  Bonhomme]
- [style] reformated with black. [Cédric Bonhomme]
- [style] reformated with black. [Cédric Bonhomme]
- [documentation] updated documentation for create_client command.
  [Cédric Bonhomme]
- [authentication] updated create_user command, added new SECRET_KEY
  variable. [Cédric Bonhomme]
- [commands] Updated is_object_published command based on the changes in
  MOSP. [Cédric Bonhomme]
- [api] fix flake8 warning. [Cédric Bonhomme]
- [lib] Updated comments. [Cédric Bonhomme]
- [lib] refactored processor in order to have different function per
  type of stats, later callable in v1/stats.py with getattr(). [Cédric
  Bonhomme]
- [documentation] the command drop_all_collections has been removed for
  long time. [Cédric Bonhomme]
- [lib] removed a useless (re-)definition of a funtion. [Cédric
  Bonhomme]
- [style] reformat with black. [Cédric Bonhomme]
- [style] reformat. [Cédric Bonhomme]
- [lib stats] process averages for threats. [Cédric Bonhomme]
- [style] Reformat with black. [Cédric Bonhomme]
- [documentation] Updated README with the STATS_CONFIG variable. Python
  >= 3.6.1 is now required (previously >= 3.8). [Cédric Bonhomme]

Fix
~~~
- [test] client is active by default. [Cédric Bonhomme]
- [api] addded missing decorator for v1/client.py POST endoiubt. [Cédric
  Bonhomme]
- [authentication] added missing import. [Cédric Bonhomme]
- [api] the call to the processor was in the bad indentation level.
  [Cédric Bonhomme]
- [api] use Date instead of Row in the response marshalling. [Cédric
  Bonhomme]

Other
~~~~~
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Changed the default value of is_active to true. [Ruslan Baidan]
- Removed the beginning of the aggregation logic. [Ruslan Baidan]
- Removed useless import. [Cédric Bonhomme]
- Merge. [Cédric Bonhomme]
- Added the roles and removed updated_at. [Ruslan Baidan]
- Changes... wip... [Cédric Bonhomme]
- Merge branch 'master' of https://github.com/monarc-project/stats-
  service. [Ruslan Baidan]

  * 'master' of https://github.com/monarc-project/stats-service:
    chg: [documentation] the command drop_all_collections has been removed for long time.
- Simplified the get stats params. [Ruslan Baidan]
- Fixed the condition. [Ruslan Baidan]
- Fixed the idention and made date_to, date_from not required. [Ruslan
  Baidan]
- Renamed Organization to Client, replaced the fileds: day, week, month,
  quarter, year to date. [Ruslan Baidan]


v0.1.9 (2020-07-08)
-------------------

New
~~~
- [views] Added new root_bp blueprint with a simply view which for the
  moment simply redirects to api.doc. [Cédric Bonhomme]
- [documentation] Added local TOC for deployment.rst. [Cédric Bonhomme]
- [deployment] Added deployment via PyPI. [Cédric Bonhomme]
- [lib] Added bridge module with a MOSP platform. [Cédric Bonhomme]
- [lib] added processors module. [Cédric Bonhomme]
- [style] Added .editorconfig. [Cédric Bonhomme]
- [lib] added JSON validation module. [Cédric Bonhomme]
- [comunity] added GitHub templates. [Cédric Bonhomme]
- [lib] added new lib utils in order to gather the different kind of
  required process on stats data. [Cédric Bonhomme]
- [documents] Added created_at and updated_at properties for
  organizations. [Cédric Bonhomme]
- [api v1] Added a new namespace for the API v1 in order to create new
  organizations. [Cédric Bonhomme]
- [api v1] implement DELETE. [Cédric Bonhomme]
- [stats/risks] added filtering on MongoEngine DynamicField. [Cédric
  Bonhomme]
- [documentation] added section about deployment in the documentation.
  [Cédric Bonhomme]
- [heroku] added file for Heroku. [Cédric Bonhomme]
- [configuration] added default configuration file for Heroku. [Cédric
  Bonhomme]
- [documents] added quarter property for stats: Number of quarter of a
  year. Possible values [1,2,3,4]. [Cédric Bonhomme]
- [documentation] added section about the new list_organizations
  command. [Cédric Bonhomme]
- [commands] added command to list organizations. [Cédric Bonhomme]
- [api v2] added athentication decorator for API v2. [Cédric Bonhomme]
- [documents] added missing year attribute for stats. [Cédric Bonhomme]
- [api v2] added a new API. [Cédric Bonhomme]
- [stats] added stats blueprint which will provided specific stats with
  different endpoints. [Cédric Bonhomme]
- [documents] added __str__ method for stats. [Cédric Bonhomme]
- [commands] added new commands in order to create organization. [Cédric
  Bonhomme]
- [api] added day, month and year as filters fo the stats resource.
  [Cédric Bonhomme]
- [commands] Added a new command to drop all collections. [Cédric
  Bonhomme]
- [documentation] Added section about data pulling for the command line
  interface. [Cédric Bonhomme]
- [commands] added pull-stats commands in order to retrieve stats from a
  central stat-api instance. [Cédric Bonhomme]
- [commands] Push stats commands is now construction the URL of the
  endpoint with urllib.parse.urljoin. [Cédric Bonhomme]
- [commands] Push stats for the organization specified in parameter to
  an other stats. [Cédric Bonhomme]
- [test] Added structure for the tests. [Cédric Bonhomme]
- [test] Added structure for the tests. [Cédric Bonhomme]
- [documentation] Added a Sphinx documentation. [Cédric Bonhomme]
- [license] added COPYING file. [Cédric Bonhomme]

Changes
~~~~~~~
- [documentation] Updated index.rst/ [Cédric Bonhomme]
- [documentation] Updated swagger.json file. [Cédric Bonhomme]
- [api] save the stats in bulk. [Cédric Bonhomme]
- [API] Post accept a list of stats. [Cédric Bonhomme]
- [models] do not slice the generated token. [Cédric Bonhomme]
- [commands] only print error message when db_init fails. [Cédric
  Bonhomme]
- [commands] updated is_object_published and db_create commands. [Cédric
  Bonhomme]
- [documentation] updated documentation related to the command line.
  [Cédric Bonhomme]
- [api] provide more clear information message about the failure of the
  authentication. [Cédric Bonhomme]
- [api] reply with 403 when authentication fails. [Cédric Bonhomme]
- [configuration] Updated Heroku configuration file with the new
  variable for MOSP. [Cédric Bonhomme]
- [lib] Updated lib for interactions with MOSP: MOSP instance URL is now
  configurable. [Cédric Bonhomme]
- [documentation] Minor rephrazing. [Cédric Bonhomme]
- [documentation] Added example of wsgi mod Apache configuration.
  [Cédric Bonhomme]
- [documentation] Removed useless lib when deploying with poetry and
  systemd. [Cédric Bonhomme]
- [documentation] cosmethic changes. [Cédric Bonhomme]
- [documentation] Added information about how to configure the
  PostgreSQL user. [Cédric Bonhomme]
- [style] Reformated with black. [Cédric Bonhomme]
- [api] Updated help description for arguments. [Cédric Bonhomme]
- [deployment] Updated Programming Language classifier. [Cédric
  Bonhomme]
- [depencies] Updated requirements.txt for Heroku only. [Cédric
  Bonhomme]
- [documentation] Updated OpenAPI specification file. [Cédric Bonhomme]
- [documentation] Deployment with systemd. [Cédric Bonhomme]
- [api] Added more checks on the type of the parameters. [Cédric
  Bonhomme]
- [api]. The type is now a required parameter. The choices are provided
  by the OpenAPI Specification. [Cédric Bonhomme]
- [deployment] Added missing INSTANCE_URL configuration variable.
  [Cédric Bonhomme]
- [deployment] Tell Poetry to also include the instance package. [Cédric
  Bonhomme]
- [configuration] Improved configuration loading and customization.
  [Cédric Bonhomme]
- [documentation] Updated OpenAPI specification file. [Cédric Bonhomme]
- [api] Updated help string for the OpenAPI Specification. [Cédric
  Bonhomme]
- [api] Updated help string for the OpenAPI Specification. [Cédric
  Bonhomme]
- [style] Reformat with black. [Cédric Bonhomme]
- [api] Added custom URL attributes date_from and date_to. [Cédric
  Bonhomme]
- [API] Check if value of the query parameter is not None or ''. [Cédric
  Bonhomme]
- [dependencies] udated idna. [Cédric Bonhomme]
- [style] format code with black. [Cédric Bonhomme]
- [deployment] MongoDB is no more supported, removed related environment
  variables. [Cédric Bonhomme]
- [requirements] Updated requirements in poetry.lock and
  requirements.txt (for Heroku). [Cédric Bonhomme]
- [documentation] updated section about deployment from Pypi. [Cédric
  Bonhomme]
- [documentation] added Heroku button deployment. [Cédric Bonhomme]
- [documentation] added section about deployment from Pypi. [Cédric
  Bonhomme]
- Group threat stats per anr UUID then per threat UUID. [Cédric
  Bonhomme]
- [api] handle the case when no type has been precised by the client.
  [Cédric Bonhomme]
- [lib] added aggregate threat function. we must still define how the
  client will ask for aggregation, probably via a parameter in the
  query. [Cédric Bonhomme]
- Updated requirements.txt. [Cédric Bonhomme]
- Removed useless stuff and updated api/v1/stats.py. [Cédric Bonhomme]
- [style] cosmethic change in models/organization.py. [Cédric Bonhomme]
- [models] Updated __str__ function for organization objects. [Cédric
  Bonhomme]
- [dependencies] Updated pandas. [Cédric Bonhomme]
- [documentation] Removed now deprecated section about token
  authentication and fixed an issue with the PDF generation of the
  documentation. [Cédric Bonhomme]
- [style] Do not trim trailing white spaces for .md and .rst files.
  [Cédric Bonhomme]
- [models] Updated order of attributes for Organization. [Cédric
  Bonhomme]
- MongoEngine has been replaced by SQLAlchemy. [Cédric Bonhomme]
- [commands ] Catch any exceptions when pushing to remote server.
  [Cédric Bonhomme]
- [dependencies] Updated sphinx and flake8. [Cédric Bonhomme]
- [documentation] update documentation with status of the tests and the
  documentation. [Cédric Bonhomme]
- [doc] updated information about push commands. [Cédric Bonhomme]
- [lib] updated dependencies. [Cédric Bonhomme]
- [commands] the token of the organization on the remote central stats
  service can be given in parameter. [Cédric Bonhomme]
- [commands] update push commands with new headers. [Cédric Bonhomme]
- [documents] Pre save data validation and cleaning. [Cédric Bonhomme]
- [documentation] minor changes to the documentation. [Cédric Bonhomme]
- [documentation] Updated documentation. [Cédric Bonhomme]
- [style] added missing space. [Cédric Bonhomme]
- [style] reformated with black. [Cédric Bonhomme]
- [api v1] Updated message returned when stats object is deleted.
  [Cédric Bonhomme]
- [stats/risks] removed useless import. [Cédric Bonhomme]
- [core] update MarkupSafe. [Cédric Bonhomme]
- [core] Updated serialization library. [Cédric Bonhomme]
- [Heroku] Updated project keywords. [Cédric Bonhomme]
- [documentation] Renamed requirements file for the generation of the
  documentation. [Cédric Bonhomme]
- [documentation] updated swagger.json. [Cédric Bonhomme]
- [api v1] updated pagination. [Cédric Bonhomme]
- [documentation] improved documentation. [Cédric Bonhomme]
- [api] authentication is mandatory. [Cédric Bonhomme]
- [documentation] added requirements-dev.txt for sphinx. [Cédric
  Bonhomme]
- [documentation] include dev packages in the poetry export to
  requirements.txt. [Cédric Bonhomme]
- [documentation] include dev packages in the poetry export to
  requirements.txt. [Cédric Bonhomme]
- [config] updated default configuration file. [Cédric Bonhomme]
- [Heroku] added retryWrites=false at the end of the conntection string.
  [Cédric Bonhomme]
- [Heroku] import render_template. [Cédric Bonhomme]
- [Heroku] specify a custom URL for heroku. [Cédric Bonhomme]
- [Heroku] new environment variable. [Cédric Bonhomme]
- [Heroku] change the way the server is launched. [Cédric Bonhomme]
- [Heroku] Load the appropriate port for Heroku. [Cédric Bonhomme]
- [core] format with black. [Cédric Bonhomme]
- [api v1] minor changes to the requestParser and to the arguments.
  [Cédric Bonhomme]
- [documentation] fix version of API in documentation. [Cédric Bonhomme]
- [documentation] updated documentation to reflect the API version
  numbering change. [Cédric Bonhomme]
- [api] swap API v1 and API v2. [Cédric Bonhomme]
- [api v2] refactorized API v2. [Cédric Bonhomme]
- [core] updated MarkupSage. [Cédric Bonhomme]
- [api v2] do not skip None value. [Cédric Bonhomme]
- [documents] data is required for stats. [Cédric Bonhomme]
- [api v2] do not skip None values in nested fields. [Cédric Bonhomme]
- [api v2] default is empty list when no data. [Cédric Bonhomme]
- [documents] anr UUID is not unique. [Cédric Bonhomme]
- [core] updated Flask-restx and other dependencies. [Cédric Bonhomme]
- [core] reformat with black and added a new fiel for the marshalling of
  stats object for api v2. [Cédric Bonhomme]
- [documents] anr property of a stat is now a UUID. [Cédric Bonhomme]
- [api v2] management of per_page and number of element of a page.
  [Cédric Bonhomme]
- [api v2] added pagination - wip. [Cédric Bonhomme]
- [core] renamed statsapi to statsservice. [Cédric Bonhomme]
- [documentation] fixed broken link. [Cédric Bonhomme]
- [documentation] changes description of stats blueprint. [Cédric
  Bonhomme]
- [documentation] added doc for the blueprint stats. [Cédric Bonhomme]
- [documentation] forgot to mention anr. [Cédric Bonhomme]
- [documents] added anr field. [Cédric Bonhomme]
- [api] added comments. [Cédric Bonhomme]
- [documentation] typo. [Cédric Bonhomme]
- [documentation] added new example. [Cédric Bonhomme]
- [documentation] added some example on methods for filters. Will list
  all the methods soonish. [Cédric Bonhomme]
- [documentation] updated README. [Cédric Bonhomme]
- [api] the token of organizations is not returned by the API. [Cédric
  Bonhomme]
- [core] style format. [Cédric Bonhomme]
- [documents] make token unique for organizations. [Cédric Bonhomme]
- [api] when creating a new stat (POST request) it is no more needed to
  send the id/token of the organization in the data or in the URL, since
  it uses the authentication mechanism. [Cédric Bonhomme]
- [documentation] typo. [Cédric Bonhomme]
- [api] updated authentication to the API with the token X-API-KEY.
  [Cédric Bonhomme]
- [documentation] improved documentation. [Cédric Bonhomme]
- [documentation] updated documentation about the authentication with
  X-API-KEY token. [Cédric Bonhomme]
- [documentation] fixes and added some refs. [Cédric Bonhomme]
- [commands] updated name of organization. [Cédric Bonhomme]
- [documentation] updated documentation and README. [Cédric Bonhomme]
- [documents] updated organization documents. [Cédric Bonhomme]
- [documentation] Getting all stats from the month of February of type
  *risk* for an organization. [Cédric Bonhomme]
- [documentation] added some complementary information on the filtering
  possibilities of the API. [Cédric Bonhomme]
- [api] plural name for view with Create, Update, Fetch, List. Singular
  for Delete. [Cédric Bonhomme]
- [documents] make uuid unique for stats documents. [Cédric Bonhomme]
- [commands] push the uuid of the stats to ensure unicity of stats.
  [Cédric Bonhomme]
- [api] removed Update and Delete method from the Stats view. [Cédric
  Bonhomme]
- [documentation] provide more information about the push-stats command.
  [Cédric Bonhomme]
- [documentation] updated presentation. [Cédric Bonhomme]
- [documentation] minor update to command-line-interface doc. [Cédric
  Bonhomme]
- [documentation] now using official ReadTheDocs theme. [Cédric
  Bonhomme]
- [documentation] how to push stats to a central server. [Cédric
  Bonhomme]
- [dependencies] added flake8 as dev dependency. [Cédric Bonhomme]
- [documentation] explicitely specify the master doc for Sphinx. [Cédric
  Bonhomme]
- [documentation] removed contents caption and indexes. [Cédric
  Bonhomme]
- [doc] fixed README. [Cédric Bonhomme]
- [core] Restructured the code to allow a more evolutive API (also with
  version of the API in the URL). [Cédric Bonhomme]
- [resource] changed pagination settings for stats resource. [Cédric
  Bonhomme]
- [resource] testing API limits and pagination. [Cédric Bonhomme]
- [doc] Updated README, the token can now be submitted. [Cédric
  Bonhomme]
- [doc] Updated documentation in the README. [Cédric Bonhomme]
- [authentication] Updated README with the authentication method.
  [Cédric Bonhomme]
- [authentication] added HTTP token based authentication for StatsView.
  [Cédric Bonhomme]
- [resources] added filters for the stars resource. [Cédric Bonhomme]

Fix
~~~
- [models] generated token is always the same when the web process is
  initialized by the system. [Cédric Bonhomme]
- [documentation] fixed Heroku button and PDF generation. [Cédric
  Bonhomme]
- [api] fixed pagination: shift (offset) should start at 0 and page
  number at 1. [Cédric Bonhomme]
- SyntaxError: non-default argument follows default argument. [Cédric
  Bonhomme]
- [typo] forgot 'as' [Cédric Bonhomme]
- [api] bad view wre imported for organization. [Cédric Bonhomme]
- [api] Object of type UUID is not JSON serializable fixed when listing
  stats. [Cédric Bonhomme]
- [core] fixed some warnings. [Cédric Bonhomme]
- [models] added a missing import for Organization. [Cédric Bonhomme]

Other
~~~~~
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Changed the creating of the stats to accept batch requests. [Ruslan
  Baidan]
- Fix issue with wrong url generated by swagger ui. [Cédric Bonhomme]
- Typo. [Cédric Bonhomme]
- Updated docs. [Cédric Bonhomme]
- Updated depdencies. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Groups threats stats data by anr first" [Cédric Bonhomme]
- Updated README. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Updated Heroku deployment. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Updated Sphinx. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-service.
  [Cédric Bonhomme]
- Style change. [Cédric Bonhomme]
- Improvements to the Python Heroku deployment. [Cédric Bonhomme]
- Removed postdeploy scripts. [Cédric Bonhomme]
- Add mongolab:sandbox addons. [Cédric Bonhomme]
- Aded requirements.txt for Heroku. [Cédric Bonhomme]
- Merge branch 'master' of github.com:cedricbonhomme/stats-api. [Cédric
  Bonhomme]
- Chjg: [documentation] Improvements. [Cédric Bonhomme]
- Updated docs. [Cédric Bonhomme]
- Display a message in case of duplicate stats. [Cédric Bonhomme]
- Added uuid for stats. [Cédric Bonhomme]
- Added first commands - WIP. [Cédric Bonhomme]
- Enable authentication for StatsResource. Fixed missing import. [Cédric
  Bonhomme]
- Added optional authentication. [Cédric Bonhomme]
- Updated dependencies. [Cédric Bonhomme]
- Merge branch 'master' of github.com:monarc-project/stats-api. [Cédric
  Bonhomme]
- Changed title of section in README. [Cédric Bonhomme]
- Added more information in the README. [Cédric Bonhomme]
- Added more information in the README. [Cédric Bonhomme]
- Added more information in the README. [Cédric Bonhomme]
- Added some black magic. [Cédric Bonhomme]
- Added initial files. [Cédric Bonhomme]
