DROP FUNCTION update_partitions;
DROP FUNCTION create_partitions;

ALTER TABLE markettor_event rename to old_markettor_event;
CREATE TABLE markettor_event (like old_markettor_event including defaults);

ALTER SEQUENCE markettor_event_id_seq OWNED BY markettor_event."id";

INSERT INTO public.markettor_event (id, event, properties, elements, timestamp, team_id, distinct_id, elements_hash)
SELECT id, event, properties, elements, timestamp, team_id, distinct_id, elements_hash
FROM public.old_markettor_event;

DROP TABLE old_markettor_event CASCADE;
DROP TABLE markettor_event_partitions_manifest CASCADE;

ALTER TABLE markettor_action_events DROP COLUMN timestamp, DROP COLUMN event;
ALTER TABLE markettor_element DROP COLUMN timestamp, DROP COLUMN event;

CREATE UNIQUE INDEX markettor_event_pkey ON public.markettor_event USING btree (id);
CREATE INDEX markettor_event_team_id_a8b4c6dc ON public.markettor_event USING btree (team_id);
CREATE INDEX markettor_event_idx_distinct_id ON public.markettor_event USING btree (distinct_id);
CREATE INDEX markettor_eve_element_48becd_idx ON public.markettor_event USING btree (elements_hash);
CREATE INDEX markettor_eve_timesta_1f6a8c_idx ON public.markettor_event USING btree ("timestamp", team_id, event);
ALTER TABLE markettor_event ADD CONSTRAINT markettor_event_team_id_a8b4c6dc_fk_markettor_team_id FOREIGN KEY (team_id) REFERENCES markettor_team(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE markettor_action_events ADD CONSTRAINT markettor_action_events_event_id_7077ea70_fk_markettor_event_id FOREIGN KEY (event_id) REFERENCES markettor_event(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE markettor_element ADD CONSTRAINT markettor_element_event_id_bb6549a0_fk_markettor_event_id FOREIGN KEY (event_id) REFERENCES markettor_event(id) DEFERRABLE INITIALLY DEFERRED;