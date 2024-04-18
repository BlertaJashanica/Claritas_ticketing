# Ticket commando's API

## Ticket aanmaken

```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets -H "Content-Type: application/json" -d '{ "title": "help!!!!", "group": "api", "customer": "api@claritas.net", "priority": "3 high", "article": { "subject": "onderwerp", "body": "u broek staat open", "type": "note", "internal": false } }'

```



## Ticket updaten:
```bash
curl -X PUT -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/3 -H "Content-Type: application/json" -d '{"title": "No help for you","group": "api","state": "open","priority": "3 high","article": { "subject": "Update via API", "body": "Heres my reason for updating this ticket...", "internal": true}}'

```



## Delete ticket:
```bash
curl -X DELETE -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/2'

```



## Bekijk ticket:
```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/1
```



## Zoek ticket:
```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/search?query={search string}&limit=10
```