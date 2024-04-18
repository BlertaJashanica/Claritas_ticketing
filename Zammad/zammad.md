# Ticket commando's API

## Aanmaken van een ticket:

```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets -H "Content-Type: application/json" -d '{ "title": "ticket1TEST", "group": "api", "customer": "api@claritas.net", "priority": "3 high", "article": { "subject": "onderwerp", "body": "ticket1 werkt", "type": "note", "internal": false } }'

```



## Updaten van een ticket:
```bash
curl -X PUT -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/3 -H "Content-Type: application/json" -d '{"title": "ticket1TEST","group": "api","state": "open","priority": "3 high","article": { "subject": "Update via API", "body": "Ticket1TEST", "internal": true}}'

```



## Delete een ticket:
```bash
curl -X DELETE -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/2'

```



## Bekijk een ticket:
```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/1
```



## Zoek een ticket:
```bash
curl -H "Authorization: Bearer 9ID_EF69Jl0tgPs32TfOXxWCTcVbVCo_jYD5fJvAzML1mJHn0ouIUhKGl0DIRiuB" http://localhost:8080/api/v1/tickets/search?query={search string}&limit=10
```
