import { CodeSnippet, Language } from 'lib/components/CodeSnippet'

import { SDKInstallFlutterInstructions } from '../sdk-install-instructions'

function FlutterCaptureSnippet(): JSX.Element {
    return (
        <CodeSnippet language={Language.Dart}>
            {
                "import 'package:clairview_flutter/clairview_flutter.dart';\n\nawait Markettor().screen(\n\tscreenName: 'Example Screen',\n);"
            }
        </CodeSnippet>
    )
}

export function ProductAnalyticsFlutterInstructions(): JSX.Element {
    return (
        <>
            <SDKInstallFlutterInstructions />
            <h3>Send an Event</h3>
            <FlutterCaptureSnippet />
        </>
    )
}
