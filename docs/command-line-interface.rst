
.. _cli:

Command Line Interface
======================

In this section commands are presented per categories:

.. contents::
    :local:
    :depth: 1


Database
--------

Creation of the database
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask db_create --help
    Usage: flask db_create [OPTIONS]

      Create the database from configuration parameters.

    Options:
      --help  Show this message and exit.


Initialization of the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask db_init --help
    Usage: flask db_init [OPTIONS]

      Initialize the database.

    Options:
      --help  Show this message and exit.


Drop all the database
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask db_empty --help
    Usage: flask db_empty [OPTIONS]

      Empty the database.

    Options:
      --help  Show this message and exit.


Will ask for confirmation and eventually drop all collections.



Clients
-------

Create a client
~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_create --help
    Usage: flask client_create [OPTIONS]

    Create a new local client.

    Options:
    --name TEXT   Name of the client.  [required]
    --uuid TEXT   UUID of the client.
    --token TEXT  Token of the client.
    --role TEXT   Role of the client (user or admin).  [default: user]
    --help        Show this message and exit.


A client name must be specified and is unique.

Example:

.. code-block:: bash

    $ flask client_create --name NC3
    UUID: fb9b4d21-4082-445c-a6e6-5d42a1cd9202
    Name: NC3
    Role: 1
    Token: fB5odBNDwzgia7SRm_Q-7tuiLtvIVHBZ2yOc9MopNMWzzoxdrF9K2cBo8rgS4eP_0Xsr0E0QCA_jsQyjhXGaaQ
    Created at: 2020-07-15 09:27:51.701245


List all clients
~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_list
    UUID: 7bb21fc8-9617-4da5-a60a-fbccda8cc583
    Name: CIRCL
    Role: 1
    Token: IR1KPdoh94m8aoCV5cuRU5ROKWXS8m6lE5M96gklf1Ar6wbrogL_bFnDdpV_AMrejApVsGfyNecp8THBXy108w
    Created at: 2020-07-23 07:56:16.556226

    UUID: aaaded6e-4039-448a-93bb-7cd7a696bc15
    Name: SMILE
    Role: 1
    Token: wwqREga9eZUVH-cz2N40voD7BkirP5K0tlkANqK-cKYjVXjy4YgdhtDGJAuw1oHntH79OSm3OzleVZEO3GRCeA
    Created at: 2020-07-23 07:57:47.658965

    UUID: f490f727-9a1a-404b-bb91-ae36f643c6fe
    Name: NC3
    Role: 1
    Token: RFXhRd4fDN7jQifaoBe3wF6TdGts6GSic2ec8qH0dft8Z2k-Q4ulZBoa_50CrrUC6rLYSAEwJZsGySpuuuounw
    Created at: 2020-07-17 12:48:05.192735



Delete a client
~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_delete --help
    Usage: flask client_delete [OPTIONS]

      Delete the client specified with its UUID and all the related local stats.

    Options:
      --uuid TEXT  UUID of the client to delete.
      -y, --yes    Automatically reply yes to the confirmation message for the
                   deletion of the client.

      --help       Show this message and exit.


Set a location for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_coordinates_set --help
    Usage: flask client_coordinates_set [OPTIONS]

    Set the coordinates of the client specified with its UUID.

    Options:
    --uuid TEXT       UUID of the client.  [required]
    --latitude TEXT   Latitude of the client.  [required]
    --longitude TEXT  Longitude of the client.  [required]
    --help            Show this message and exit.


Unset the location for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_coordinates_unset --help
    Usage: flask client_coordinates_unset [OPTIONS]

      Unset the coordinates of the client specified with its UUID.

    Options:
      --uuid TEXT  UUID of the client.  [required]
      --help       Show this message and exit.


Activate the stats sharing for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_sharing_activate --help
    Usage: flask client_sharing_activate [OPTIONS]

      Set the is_sharing_enabled attribute of a local client, specified with its
      UUID, to True.

    Options:
      --uuid TEXT  UUID of the client.  [required]
      --help       Show this message and exit.


Deactivate the stats sharing for a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ flask client_sharing_deactivate --help
    Usage: flask client_sharing_deactivate [OPTIONS]

      Set the is_sharing_enabled attribute of a local client, specified with its
      UUID, to False.

    Options:
      --uuid TEXT  UUID of the client.  [required]
      --help       Show this message and exit.


Stats
------

Pushing data
~~~~~~~~~~~~

Pushing data to a central stats server.

.. code-block:: bash

    $ flask stats_push --help
    Usage: flask stats_push [OPTIONS]

    Pushes the clients stats to the global stats server.

    Only the stats of the clients with the flag `is_sharing_enabled` set to
    True will be pushed.

    If you specify the UUID of a client only the stats of this client will be
    pushed (and if `is_sharing_enabled` is set to True for this client).

    The parameter `remote_token` is used for the authentication to the remote
    stats service and to 'identify' the client on the remote side.

    Options:
    --local-client-uuid TEXT  UUID of the client related to the stats.
    --remote-token TEXT       Client token on remote side.
    --date-from [%Y-%m-%d]    Only stats more recent than this date will be
                            pushed. Default value is 1 month before the
                            current day.

    --date-to [%Y-%m-%d]      Only stats older than this date will be pushed.
                            Default value is today.

    --help                    Show this message and exit.


This command can be executed for example with cron.

The address of the central stats server must be specified in the configuration
file.

The same remote token can be used to push the stats from different local clients.


Pulling data
~~~~~~~~~~~~

Pulling data from a central stats server.

.. code-block:: bash

    $ flask stats_pull --help
    Usage: flask stats_pull [OPTIONS]

      Pull stats from an other stats instance for the local client specified in
      parameter.

    Options:
      --client-uuid TEXT        Local client uuid
      --token TEXT       Client token on remote side  [required]
      --stats-type TEXT  Type of the stats to import (risk, vulnerability,
                         threat).  [required]

      --help             Show this message and exit.


Delete stats
~~~~~~~~~~~~

.. code-block:: bash

    $ flask stats_delete --help
    Usage: flask stats_delete [OPTIONS]

    Delete the stats of a local client.

    Options:
    --client-uuid TEXT  UUID of the client related to the stats.
    -y, --yes           Automatically reply yes to the confirmation message.
    --help              Show this message and exit.

Purging stats
~~~~~~~~~~~~~

.. code-block:: bash

    $ flask stats_purge --help
    Usage: flask stats_purge [OPTIONS]

    Delete the stats older than the number of months specified in parameter.

    Options:
    --nb-month INTEGER  Age (in months) of the stats to purge.
    --help              Show this message and exit.


Interactions with MOSP
----------------------

.. code-block:: bash

    $ flask mosp_is_object_published --help
    Usage: flask mosp_is_object_published [OPTIONS]

      Check if an object has been published on MOSP. Returns a boolean.

    Options:
      --uuid TEXT    UUID of the object  [required]
      -v, --verbose  Display the object
      --help         Show this message and exit.

Examples:

.. code-block:: bash

    $ flask mosp_is_object_published --uuid f3caa83b-28fb-49fd-b7ad-6e4cd1aaad06
    False
    $ flask mosp_is_object_published --uuid f3caa83b-28fb-49fd-b7ad-6e4cd1aaad07
    True
    $ flask mosp_is_object_published --uuid f3caa83b-28fb-49fd-b7ad-6e4cd1aaad07 -v
    {
        "data": [
            {
                "description": "Mobile Mitigations  from MITRE ATT&CK® \r\n© 2020 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.",
                "json_object": {
                    "authors": [
                        "MITRE ATT&CK®"
                    ],
                    "label": "MITRE ATT&CK - Mobile Mitigations",
                    "language": "EN",
                    "refs": [
                        "https://attack.mitre.org/mitigations/mobile/"
                    ],
                    "uuid": "f3caa83b-28fb-49fd-b7ad-6e4cd1aaad07",
                    "values": [
                        {
                            "code": "M1013 - Application Developer Guidance",
                            "description": "This mitigation describes any guidance or training given to developers of applications to avoid introducing security weaknesses that an adversary may be able to take advantage of.",
                            "importance": 0,
                            "uuid": "90624dfc-21b6-4172-8848-a4042860656b"
                        },
                        {
                            "code": "M1005 - Application Vetting",
                            "description": "Enterprises can vet applications for exploitable vulnerabilities or unwanted (privacy-invasive or malicious) behaviors. Enterprises can inspect applications themselves or use a third-party service.",
                            "importance": 0,
                            "uuid": "7fd9df45-7351-420c-8116-57d48fa23c40"
                        },
                        {
                            "code": "M1002 - Attestation",
                            "description": "Enable remote attestation capabilities when available (such as Android SafetyNet or Samsung Knox TIMA Attestation) and prohibit devices that fail the attestation from accessing enterprise resources.",
                            "importance": 0,
                            "uuid": "5617161e-a40d-461a-ae8e-6a0650392e3a"
                        },
                        {
                            "code": "M1007 - Caution with Device Administrator Access",
                            "description": "Warn device users not to accept requests to grant Device Administrator access to applications without good reason.",
                            "importance": 0,
                            "uuid": "63138250-3821-45f3-a820-55d0ffa30367"
                        },
                        {
                            "code": "M1010 - Deploy Compromised Device Detection Method",
                            "description": "A variety of methods exist that can be used to enable enterprises to identify compromised (e.g. rooted/jailbroken) devices, whether using security mechanisms built directly into the device, third-party mobile security applications, enterprise mobility management (EMM)/mobile device management (MDM) capabilities, or other methods. Some methods may be trivial to evade while others may be more sophisticated.",
                            "importance": 0,
                            "uuid": "6501d616-1a60-4b38-a40a-847ad5d28058"
                        },
                        {
                            "code": "M1009 - Encrypt Network Traffic",
                            "description": "Application developers should encrypt all of their application network traffic using the Transport Layer Security (TLS) protocol to ensure protection of sensitive data and deter network-based attacks. If desired, application developers could perform message-based encryption of data before passing it for TLS encryption.",
                            "importance": 0,
                            "uuid": "c591b8fd-5f57-4064-b5c5-f0acd38ae41f"
                        },
                        {
                            "code": "M1012 - Enterprise Policy",
                            "description": "An enterprise mobility management (EMM), also known as mobile device management (MDM), system can be used to provision policies to mobile devices to control aspects of their allowed behavior.",
                            "importance": 0,
                            "uuid": "b141135f-2c2f-4588-9d4c-6c7abd243e23"
                        },
                        {
                            "code": "M1014 - Interconnection Filtering",
                            "description": "In order to mitigate Signaling System 7 (SS7) exploitation, the Communications, Security, Reliability, and Interoperability Council (CSRIC) describes filtering interconnections between network operators to block inappropriate requests.",
                            "importance": 0,
                            "uuid": "6066f816-7914-4228-96b6-155f4501d70c"
                        },
                        {
                            "code": "M1003 - Lock Bootloader",
                            "description": "On devices that provide the capability to unlock the bootloader (hence allowing any operating system code to be flashed onto the device), perform periodic checks to ensure that the bootloader is locked.",
                            "importance": 0,
                            "uuid": "148c35e1-7837-42a2-9884-4e475a48e6a3"
                        },
                        {
                            "code": "M1001 - Security Updates",
                            "description": "Install security updates in response to discovered vulnerabilities.",
                            "importance": 0,
                            "uuid": "057adb3d-1eeb-4f04-a9c6-c08b514bc785"
                        },
                        {
                            "code": "M1004 - System Partition Integrity",
                            "description": "Ensure that Android devices being used include and enable the Verified Boot capability, which cryptographically ensures the integrity of the system partition.",
                            "importance": 0,
                            "uuid": "daa42611-836d-464e-aab5-80d41da314cf"
                        },
                        {
                            "code": "M1006 - Use Recent OS Version",
                            "description": "New mobile operating system versions bring not only patches against discovered vulnerabilities but also often bring security architecture improvements that provide resilience against potential vulnerabilities or weaknesses that have not yet been discovered. They may also bring improvements that block use of observed adversary techniques.",
                            "importance": 0,
                            "uuid": "f4bbe273-dc6c-4b5d-8c66-286effded2c7"
                        },
                        {
                            "code": "M1011 - User Guidance",
                            "description": "Describes any guidance or training given to users to set particular configuration settings or avoid specific potentially risky behaviors.",
                            "importance": 0,
                            "uuid": "8f023e31-b83d-4323-ba0e-888ec025b35f"
                        }
                    ],
                    "version": 6.3
                },
                "last_updated": "2020-05-27T09:54:06.727943",
                "name": "MITRE ATT&CK - Mobile Mitigations "
            }
        ],
        "metadata": {
            "count": "1",
            "limit": "10",
            "offset": "0"
        }
    }
    True
