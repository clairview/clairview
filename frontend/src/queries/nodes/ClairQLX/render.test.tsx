import { parseClairQLX, renderClairQLX } from '~/queries/nodes/ClairQLX/render'

describe('ClairQLX', () => {
    describe('parse', () => {
        it('should parse tags', () => {
            const value = parseClairQLX(['__hx_tag', 'Sparkline', 'data', [1, 2, 3], 'type', ['line']])
            expect(value).toEqual({
                __hx_tag: 'Sparkline',
                data: [1, 2, 3],
                type: ['line'],
            })
        })

        it('should parse empty tags', () => {
            const value = parseClairQLX(['__hx_tag', 'Sparkline'])
            expect(value).toEqual({
                __hx_tag: 'Sparkline',
            })
        })

        it('should parse objects', () => {
            const value = parseClairQLX(['__hx_tag', '__hx_obj', 'a', 1, 'b', 2])
            expect(value).toEqual({
                a: 1,
                b: 2,
            })
        })

        it('should handle arrays', () => {
            const value = parseClairQLX(['a', 'b', 'c'])
            expect(value).toEqual(['a', 'b', 'c'])
        })

        it('should handle nested arrays', () => {
            const value = parseClairQLX(['a', ['b', 'c']])
            expect(value).toEqual(['a', ['b', 'c']])
        })

        it('should handle nested objects', () => {
            const value = parseClairQLX(['__hx_tag', '__hx_obj', 'a', ['b', 'c']])
            expect(value).toEqual({
                a: ['b', 'c'],
            })
        })

        it('should handle nested objects with tags', () => {
            const value = parseClairQLX([
                '__hx_tag',
                '__hx_obj',
                'a',
                ['__hx_tag', 'Sparkline', 'data', [1, 2, 3], 'type', ['line']],
            ])
            expect(value).toEqual({
                a: {
                    __hx_tag: 'Sparkline',
                    data: [1, 2, 3],
                    type: ['line'],
                },
            })
        })
    })

    describe('render', () => {
        it('should render Sparkline', () => {
            const value = {
                __hx_tag: 'Sparkline',
                data: [1, 2, 3],
                type: ['line'],
            }
            const element = renderClairQLX(value)
            expect(element).toMatchSnapshot()
        })

        it('should render object', () => {
            const value = {
                a: 1,
                b: 2,
            }
            const element = renderClairQLX(value)
            expect(element).toMatchSnapshot()
        })

        it('should render unknown tag', () => {
            const value = {
                __hx_tag: 'Unknown',
            }
            const element = renderClairQLX(value)
            expect(element).toMatchSnapshot()
        })

        it('should render array', () => {
            const value = [1, 2, 3]
            const element = renderClairQLX(value)
            expect(element).toMatchSnapshot()
        })
    })
})
