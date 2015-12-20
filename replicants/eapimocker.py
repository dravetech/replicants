"""
"""
import os
import json
import pyeapi


class Eapi(object):
    def __init__(self, connection):
        self.original_connection = connection
        self.device = connection.transport.host

        self.path = '{base}/{device}'.format(
            base=os.environ['REPLICANTS_FOLDER'],
            device=self.device
        )

    def __getattr__(self, item):
        return getattr(self.original_connection, item)

    @staticmethod
    def build_filename(path, command, encoding):
        return '{path}/{command}.{filetype}'.format(
            path=path,
            command=command.replace(' ', '_'),
            filetype='json' if encoding == 'json' else 'txt'
        )


class EapiRecorder(Eapi):
    def __init__(self, connection):
        super(EapiRecorder, self).__init__(connection)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def save_to_file(self, command, record, encoding):
        filename = self.build_filename(self.path, command, encoding)
        with open(filename, 'w') as f:
            f.write(json.dumps(record, sort_keys=True, indent=4))

    def save_records(self, response, encoding):
        for r in response:
            record = {
                'error': False,
                'result': r['output']
            }
            self.save_to_file(r['command'], record, encoding)

    def execute(self, *args):
        try:
            response = self.original_connection.execute(*args)
        except Exception as e:
            data = {a: getattr(e, a) for a in dir(e) if not a.startswith('__') and not callable(getattr(e, a))}
            record = {
                'error': True,
                'exception': e.__class__.__name__,
                'result': data,
            }
            self.save_records(response=e.trace, encoding=args[1])
            self.save_to_file(command=e.error_text.split('\'')[1], record=record, encoding=args[1])
            raise

        self.save_records(
            response=[{'output': response['result'][position], 'command': command}
                      for position, command in enumerate(args[0])],
            encoding=args[1]
        )
        return response


class EapiPlayer(Eapi):

    def raise_exception(self, record):
        error_code = record['result'].pop('error_code')
        error_text = record['result'].pop('error_text')
        del(record['result']['message'])

        raise pyeapi.eapilib.CommandError(error_code, error_text, **record['result'])

    def execute(self, *args):
        response = {
            'jsonrpc': 2.0,
            'result': [],
            'id': 46752342
        }

        for command in args[0]:
            filename = self.build_filename(self.path, command, encoding=args[1])

            with open(filename, 'r') as f:
                record = json.loads(f.read())

                if record['error']:
                    self.raise_exception(record)
                else:
                    response['result'].append(record['result'])

        return response
