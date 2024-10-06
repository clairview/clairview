-- These mimic the markettor main-db property, event and event-property tables, and are only used
-- for testing (so we can use `sqlx::test`)

-- Create a unique contraint on markettor_eventdefinition for team_id and name, matching the django one

CREATE TABLE IF NOT EXISTS markettor_eventdefinition (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    volume_30_day INTEGER,
    query_usage_30_day INTEGER,
    team_id INTEGER NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT markettor_eventdefinition_team_id_name_80fa0b87_uniq UNIQUE (team_id, name)
);


CREATE TABLE IF NOT EXISTS markettor_propertydefinition (
    id UUID PRIMARY KEY,
    name VARCHAR(400) NOT NULL,
    is_numerical BOOLEAN NOT NULL,
    query_usage_30_day INTEGER,
    property_type VARCHAR(50),
    property_type_format VARCHAR(50),
    volume_30_day INTEGER,
    team_id INTEGER NOT NULL,
    group_type_index SMALLINT,
    type SMALLINT NOT NULL DEFAULT 1
);

CREATE UNIQUE INDEX markettor_propertydefinition_uniq ON markettor_propertydefinition (team_id, name, type, coalesce(group_type_index, -1));


CREATE TABLE IF NOT EXISTS markettor_eventproperty (
    id SERIAL PRIMARY KEY,
    event VARCHAR(400)NOT NULL,
    property VARCHAR(400) NOT NULL,
    team_id INTEGER NOT NULL
);

CREATE UNIQUE INDEX markettor_event_property_unique_team_event_property ON markettor_eventproperty (team_id, event, property);