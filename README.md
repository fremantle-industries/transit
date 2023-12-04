# Transit

A bytes first implementation of the Kafka API within an S3 keyspace

## Start Nix Devshell

```bash
> nix develop -c $SHELL
```

## Install Dependencies

```bash
> make deps/install
```

## Freeze Dependencies

```bash
> make deps/freeze
```

## Run

```bash
> make run/transitbroker
> make run/transitctl
```

## Format

```bash
> make format
```

## Lint

```bash
> make lint
```

## Test

```bash
> make test/transitbroker
> make test/transitclient
> make test/transitctl
```

## Coverage

```bash
> make coverage/transitbroker
> make coverage/transitclient
> make coverage/transitctl
```

## Build

```bash
> make build/sprout
> make build/sproutctl
```

## Execute

```bash
> make exec/sprout -- start
> make exec/sproutctl
```

## Clean

```bash
> make clean/sprout
> make clean/sproutctl
```

## Storage Keyspace

- Max key size 1024 bytes [S3 limit](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html)
- Sorted in UTF-8 order
- Base 62 encoded (0-9a-zA-Z)
- Message batch object includes delta encoding in object name (3+b)
- Each broker maintains a sliding window of the S3 protocol for tiered warm and hot set on local block storage and in memory

**Globally ordered sequence with partition details in descendent key space**

```sh
t/topic.1/b/k/ed25519/AAAAC3NzaC1lZDI1NTE5AAAAILGAXAVoZheauoHR3P20PYuPNKmw8OPcyYdUXA2sLcc1
t/topic.1/b/k/ed25519/AAAAC3NzaC1lZDI1NTE5AAAAIMkpZ0nWcTUEHbqIG0UH6uil7msEL2pWhQsdQlS1VE6X
t/topic.1/b/k/ed25519/AAAAC3NzaC1lZDI1NTE5AAAAILM0p3b52jtue01YfUFwwkLAuwELxMlJqbdPrEdmBpj2
t/topic.1/config
t/topic.1/cg/all-consumer-group/a
t/topic.1/cg/partition-consumer-group/a
t/topic.1/cg/partition-consumer-group/b
t/topic.1/r/0
t/topic.1/r/1+2
t/topic.1/r/1+2/p0
t/topic.1/r/1+2/p1
t/topic.1/r/4+B
t/topic.1/r/16+b
t/topic.1/r/79+5
...
```

**Globally ordered sequence with no partitions and delta encoded batching that can be used for range seek:**

- How would consumer groups partition themselves?

```sh
...
t/topic.1/config
...
t/topic.1/r/0
t/topic.1/r/1+2
t/topic.1/r/4+B
t/topic.1/r/16+b
t/topic.1/r/79+5
...
```

**Partitioned with globally ordered sequence and delta encoded batching:**

- Can S3 ignore the common prefix when ordering to maintain a global UTF-8 order?

```sh
...
t/topic.1/config
...
t/topic.1/r/p0/0
t/topic.1/r/p0/1+2
t/topic.1/r/p0/4+B
t/topic.1/r/p0/16+b
t/topic.1/r/p0/79+5
...
```

**Globally ordered sequence and delta encoded batching that can be used for range seek:**

```sh
...
t/topic.1/config
...
t/topic.1/r/0/p0
t/topic.1/r/1+2/p0
t/topic.1/r/4+B/p0
t/topic.1/r/16+b/p0
t/topic.1/r/79+5/p0
...
```

**Git like branching semantics will enable migrations and repartitioning schemes**

```sh
...
t/topic.1/branch
t/topic.1/config
...
t/topic.1/refs/origin/main/r/0/p0
t/topic.1/refs/origin/main/r/1/p1
t/topic.1/refs/origin/main/r/2/p2
t/topic.1/refs/origin/main/r/3/p3
t/topic.1/refs/origin/main/r/4/p0
t/topic.1/refs/origin/main/r/5/p1
t/topic.1/refs/origin/main/r/6/p2
t/topic.1/refs/origin/main/r/7/p3
...
```

```sh
...
t/topic.1/branch
t/topic.1/config
...
t/topic.1/refs/origin/main/r/0/p0
t/topic.1/refs/origin/main/r/1/p1
t/topic.1/refs/origin/main/r/2/p2
t/topic.1/refs/origin/main/r/3/p3
t/topic.1/refs/origin/main/r/4/p0
t/topic.1/refs/origin/main/r/5/p1
t/topic.1/refs/origin/main/r/6/p2
t/topic.1/refs/origin/main/r/7/p3
t/topic.1/refs/origin/main+fix/r/6/p2
t/topic.1/refs/origin/main+fix/r/7/p3
...
```

## Development

```sh
make
```

## Test

```sh
make test
```

## Authors

- Alex Kwiatkowski - alex+git@fremantle.io

## License

`transit` is released under the [MIT license](./LICENSE)
