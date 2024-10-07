import { Meta, StoryFn, StoryObj } from '@storybook/react'
import { useState } from 'react'

import { TorQLEditor } from './TorQLEditor'

type Story = StoryObj<typeof TorQLEditor>
const meta: Meta<typeof TorQLEditor> = {
    title: 'Components/TorQLEditor',
    component: TorQLEditor,
}
export default meta

const Template: StoryFn<typeof TorQLEditor> = (props): JSX.Element => {
    const [value, onChange] = useState(props.value ?? "countIf(properties.$browser = 'Chrome')")
    return <TorQLEditor {...props} value={value} onChange={onChange} />
}

export const TorQLEditor_: Story = Template.bind({})
TorQLEditor_.args = {}

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
