import pypd

apikey = 'apikey'
pypd.api_key = apikey

# fetch some dataz
incidents = pypd.Incident.find(maximum=10)

# how do dataz?
ep = pypd.EscalationPolicy.find_one()
print(ep['id'])
print(ep.get('name'))
print(ep.json)  # not a string, a json-compat dict
print(ep.__json__())  # a json encoded string, json encoder interface compat
print(ep._data)  # raw data, best not to access it this way!

# nice embedded property things
incident = pypd.Incident.find_one()
log_entries = incident.log_entries()
alerts = incident.alerts()

# incident actions
# incident.snooze(from_email='jdc@pagerduty.com', 3600) # snooze for an hour
# incident.snooze(from_email='jdc@pagerduty.com', 3600) # snooze for an hour
# incident.snooze(from_email='jdc@pagerduty.com', 3600) # snooze for an hour
# incident.resolve(from_email='jdc@pagerduty.com', resolution='We solved a thing')
# incident.merge(from_email='jdc@pagerduty.com', [another_incident, ])
# incident.create_note(from_email='jdc@pagerduty.com', 'Duly noted.')

# find users
user = pypd.User.find_one(email="hareeshksahadevan@gmail.com")

# create an event
pypd.Event.create(data={
    'service_key': 'apikey',
    'event_type': 'trigger',
    'description': 'this is a trigger event!',
    'contexts': [
        {
            'type': 'link',
            'href': 'http://sibin.pagerduty.com',
            'text': 'View on PD',
        },
    ],
})

# create a version 2 event
pypd.EventV2.create(data={
    'routing_key': apikey,
    'event_action': 'trigger',
    'payload': {
        'summary': 'this is an error event!',
        'severity': 'error',
        'source': 'pypd bot',
    }
})
