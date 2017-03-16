# Natural Language API Example

## Products

- [App Engine][1]


## Language

- [Python][2]


## APIs

- [Twitter API][3]
- [Natural Language API][4]

[1]: https://cloud.google.com/appengine/docs
[2]: https://python.org
[3]: https://dev.twitter.com/docs
[4]: https://cloud.google.com/natural-language/


## Prerequisites

1. A Google Cloud Platform Account
2. [A new Google Cloud Platform Project][5] for this lab with billing enabled
 (You can choose the region for App Engine deployment with advanced options.)
3. Enable the Natural Language API from [the API Manager][6]
4. Create application in [Twitter Application Management][7] and get "Consumer Key" and "Consumer Secret"

[5]: https://console.developers.google.com/project
[6]: https://console.developers.google.com
[7]: https://apps.twitter.com


## Deploy the application

```shell
$ pip install -r requirements.txt -t lib
$ gcloud app create
$ gcloud app deploy
```

By executing these commands on the Cloud Shell, the project id is automatically
 applied to the application and the application URL will be
 https://\<project id\>.appspot.com.


## Clean up
Clean up is really easy, but also super important: if you don't follow these
 instructions, you will continue to be billed for the project you created.

To clean up, navigate to the [Google Developers Console Project List][6],
 choose the project you created for this lab, and delete it. That's it.

[6]: https://console.developers.google.com/project