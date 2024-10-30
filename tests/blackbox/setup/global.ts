import { ChildProcess } from 'child_process';

const global = {
	clairview: {} as { [vendor: string]: ChildProcess },
	clairviewNoCache: {} as { [vendor: string]: ChildProcess },
};

export default global;
