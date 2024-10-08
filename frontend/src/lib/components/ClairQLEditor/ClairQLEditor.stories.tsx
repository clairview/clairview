import { Meta, StoryFn, StoryObj } from '@storybook/react'
import { useState } from 'react'

import { ClairQLEditor } from './ClairQLEditor'

type Story = StoryObj<typeof ClairQLEditor>
const meta: Meta<typeof ClairQLEditor> = {
    title: 'Components/ClairQLEditor',
    component: ClairQLEditor,
}
export default meta

const Template: StoryFn<typeof ClairQLEditor> = (props): JSX.Element => {
    const [value, onChange] = useState(props.value ?? "countIf(properties.$browser = 'Chrome')")
    return <ClairQLEditor {...props} value={value} onChange={onChange} />
}

export const ClairQLEditor_: Story = Template.bind({})
ClairQLEditor_.args = {}

export const NoValue: Story = Template.bind({})
NoValue.args = {
    value: '',
    disableAutoFocus: true,
}

export const NoValuePersonPropertiesDisabled: Story = Template.bind({})
NoValuePersonPropertiesDisabled.args = {
    disablePersonProperties: true,
    value: '',
    disableAutoFocus: true,
}
