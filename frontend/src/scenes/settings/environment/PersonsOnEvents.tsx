import { LemonTag, Link } from '@markettor/lemon-ui'
import { useActions, useValues } from 'kea'
import { LemonButton } from 'lib/lemon-ui/LemonButton'
import { LemonRadio, LemonRadioOption } from 'lib/lemon-ui/LemonRadio'
import { eventUsageLogic } from 'lib/utils/eventUsageLogic'
import markettor from 'markettor-js'
import { useState } from 'react'
import { teamLogic } from 'scenes/teamLogic'

import { TorQLQueryModifiers } from '~/queries/schema'

type PoEMode = NonNullable<TorQLQueryModifiers['personsOnEventsMode']>

const POE_OPTIONS: LemonRadioOption<PoEMode>[] = [
    {
        value: 'person_id_override_properties_on_events',
        label: (
            <span className="inline-flex items-center gap-1.5">
                Use person properties from the time of the event<LemonTag>RECOMMENDED</LemonTag>
            </span>
        ),
        description: (
            <>
                Fast queries. If the person property is updated, query results on past data <em>won't</em> change.
            </>
        ),
    },
    {
        value: 'person_id_override_properties_joined',
        label: 'Use person properties as of running the query',
        description: (
            <>
                Slower queries. If the person property is updated, query results on past data <em>will</em> change
                accordingly.
            </>
        ),
    },
    {
        value: 'person_id_no_override_properties_on_events',
        label: 'Use person IDs and person properties from the time of the event',
        description: (
            <>
                Fastest queries,{' '}
                <span className="underline">but funnels and unique user counts will be inaccurate</span>. If the person
                property is updated, query results on past data <em>won't</em> change.
            </>
        ),
    },
]

export function PersonsOnEvents(): JSX.Element {
    const { updateCurrentTeam } = useActions(teamLogic)
    const { reportPoEModeUpdated } = useActions(eventUsageLogic)
    const { currentTeam } = useValues(teamLogic)
    const savedPoEMode: PoEMode =
        currentTeam?.modifiers?.personsOnEventsMode ?? currentTeam?.default_modifiers?.personsOnEventsMode ?? 'disabled'
    const [poeMode, setPoeMode] = useState<PoEMode>(savedPoEMode)

    const handleChange = (mode: PoEMode): void => {
        updateCurrentTeam({ modifiers: { ...currentTeam?.modifiers, personsOnEventsMode: mode } })
        markettor.capture('user changed personsOnEventsMode setting', { personsOnEventsMode: mode })
        reportPoEModeUpdated(mode)
    }

    return (
        <>
            <p>
                Choose the behavior of person property filters. For the best performance,{' '}
                <strong>we strongly recommend the first option.</strong>{' '}
                <Link
                    to="https://markettor.com/docs/how-markettor-works/queries#filtering-on-person-properties"
                    target="blank"
                >
                    Learn about the details in our docs.
                </Link>
            </p>
            <LemonRadio value={poeMode} onChange={setPoeMode} options={POE_OPTIONS} />
            <div className="mt-4">
                <LemonButton
                    type="primary"
                    onClick={() => handleChange(poeMode)}
                    disabledReason={poeMode === savedPoEMode ? 'No changes to save' : undefined}
                >
                    Save
                </LemonButton>
            </div>
        </>
    )
}
