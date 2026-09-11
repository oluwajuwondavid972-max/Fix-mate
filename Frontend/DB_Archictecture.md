USERS
─────
id
name
location
...


TECHNICIANS
───────────
id
name
specialization
location
rating
verification_status
...


SERVICES
────────
id
technician_id
category
...


BOOKINGS
────────
id
user_id
technician_id
problem
status
price
commission
...


DIAGNOSTIC_SESSIONS
───────────────────
id
user_id
device
problem
diagnosis
confidence
outcome
...