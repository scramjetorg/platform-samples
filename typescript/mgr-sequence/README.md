# Sequence deployment together with starting Hubs

## Sequence description

### timestamp-manager

This Sequence starts multiple instances of the '@scramjet/timestamp-producer' sequence, calculates the time differences between received timestamps and local timestamps, and returns the overall average difference in milliseconds to the Instance output and stdout.

### timestamp-producer

This Sequence generates and sends timestamps to the output stream. Upon receiving the 'start' event, the Sequence starts generating the specified number of timestamps at the given interval and pushes them to the output stream. It uses the 'real-hrtime' module to generate timestamps. After generating the desired number of timestamps, it pushes an end indicator to signify the end of data.

## STH deployment command

```bash
sth -S typescript/mgr-sequence/seq-config.json -E -D typescript/mgr-sequence --runtime-adapter process --config typescript/mgr-sequence/shh-config.json
```

> Optionally you can use `DEVELOPMENT=1` env to see Runner logs.

Options used in the command:

* `-S <path>` or `--startup-config <path>` - option that points at configuration JSON file, which contains metadata needed for starting up the sequence(s). It works only with process adapter. As a `<path>` argument you should provide the location of a config file with the list of Sequences to be started along with the sth.
The example of a startup-config.json file:

```json
{
  "sequences": [
    {
      "id": "sequence-name",
      "args": [],
      "instanceId": "11111111-2222-3333-4444-555555555555"
    }
  ]
}
```

As the example above shows, you should pass in your own Sequence ID and Instance ID in your config file.

Sequence id given in the config file should be exactly the same as the same if the Sequence directory. Otherwise you will get a WARN like this in STH logs:

```bash
2023-06-16T13:58:54.067Z WARN  Host Sequence id not found for startup config [ { id: 'sequence-name', args: [], instanceId: '11111111-2222-3333-4444-555555555555' } ]
```

* `-E` or `--identify-existing` - this option scans the catalog and looks for Sequences, when there are any found they are added to STH and started right after.

· `-D <path>` or `--sequences-root <path>` - this option points at the location of the Sequences that will be started together with sth. This is also where ProcessSequenceAdapter saves new Sequences.

Optionally:

* `-X` or `--exit-with-last-instance` - thanks to this option STH will exit when no more Instances exist.

## Output

The results will be provided by the instance of the `timestamp-manager` Sequence.
Read `stdout` stream (`si inst stdout <instance-id>`), or check out STH logs, you should see something similar to this:

```bash
Channel averages (nanoseconds):
┌─────────┬──────────────┐
│ (index) │    Values    │
├─────────┼──────────────┤
│    0    │ '    422940' │
│    1    │ '    423649' │
│    2    │ '    422948' │
│    3    │ '    434039' │
│    4    │ '    412757' │
└─────────┴──────────────┘
Average from 5 output streams: 423266 (nanoseconds)
Average of 5 averages: 0.2116 (milliseconds)
```

To find out what each Sequence does look into the comments included in the code.
