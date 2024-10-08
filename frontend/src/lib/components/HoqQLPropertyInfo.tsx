import { midEllipsis } from 'lib/utils'

type ClairQLPropertyInfoProps = {
    value: string
}

export const ClairQLPropertyInfo = ({ value }: ClairQLPropertyInfoProps): JSX.Element => {
    return (
        <span title={value} className="font-mono text-primary text-xs">
            {midEllipsis(value, 60)}
        </span>
    )
}
