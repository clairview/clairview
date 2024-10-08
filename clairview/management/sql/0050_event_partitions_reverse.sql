DROP FUNCTION update_partitions;
DROP FUNCTION create_partitions;

ALTER TABLE clairview_event rename to old_clairview_event;
CREATE TABLE clairview_event (like old_clairview_event including defaults);

ALTER SEQUENCE clairview_event_id_seq OWNED BY clairview_event."id";

INSERT INTO public.clairview_event (id, event, properties, elements, timestamp, team_id, distinct_id, elements_hash)
SELECT id, event, properties, elements, timestamp, team_id, distinct_id, elements_hash
FROM public.old_clairview_event;

DROP TABLE old_clairview_event CASCADE;
DROP TABLE clairview_event_partitions_manifest CASCADE;

ALTER TABLE clairview_action_events DROP COLUMN timestamp, DROP COLUMN event;
ALTER TABLE clairview_element DROP COLUMN timestamp, DROP COLUMN event;

CREATE UNIQUE INDEX clairview_event_pkey ON public.clairview_event USING btree (id);
CREATE INDEX clairview_event_team_id_a8b4c6dc ON public.clairview_event USING btree (team_id);
CREATE INDEX clairview_event_idx_distinct_id ON public.clairview_event USING btree (distinct_id);
CREATE INDEX clairview_eve_element_48becd_idx ON public.clairview_event USING btree (elements_hash);
CREATE INDEX clairview_eve_timesta_1f6a8c_idx ON public.clairview_event USING btree ("timestamp", team_id, event);
ALTER TABLE clairview_event ADD CONSTRAINT clairview_event_team_id_a8b4c6dc_fk_clairview_team_id FOREIGN KEY (team_id) REFERENCES clairview_team(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE clairview_action_events ADD CONSTRAINT clairview_action_events_event_id_7077ea70_fk_clairview_event_id FOREIGN KEY (event_id) REFERENCES clairview_event(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE clairview_element ADD CONSTRAINT clairview_element_event_id_bb6549a0_fk_clairview_event_id FOREIGN KEY (event_id) REFERENCES clairview_event(id) DEFERRABLE INITIALLY DEFERRED;