with source as (
    select * from {{ source('raw', 'device_events') }}
)
select
    event_id,
    device_id,
    capability,
    attribute,
    value,
    unit,
    ts as event_time,
    ingested_at
from source
