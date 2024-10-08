import { LemonSelect } from '@clairview/lemon-ui'
import clairview from 'clairview-js'

import { DurationType } from '~/types'

interface DurationTypeFilterProps {
    // what to call this when reporting analytics to ClairView
    onChangeEventDescription?: string
    onChange: (newFilter: DurationType) => void
    value?: DurationType
}

export function DurationTypeSelect({
    onChange,
    value,
    onChangeEventDescription,
}: DurationTypeFilterProps): JSX.Element {
    return (
        <LemonSelect
            data-attr="duration-type-selector"
            onChange={(v) => {
                clairview.capture(onChangeEventDescription || 'session recording duration type filter changed', {
                    durationChoice: v,
                })
                onChange((v || 'all') as DurationType)
            }}
            options={[
                {
                    label: 'total duration',
                    value: 'duration',
                },
                {
                    label: 'active duration',
                    value: 'active_seconds',
                },
                {
                    label: 'inactive duration',
                    value: 'inactive_seconds',
                },
            ]}
            size="small"
            value={value || 'duration'}
        />
    )
}
