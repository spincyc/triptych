<!-- SPDX-License-Identifier: MIT -->
# Native print worker image

This optional worker runs the existing native TeX recipes. It retains Latin
Modern for the provider publications, Libertinus for the server guides, Bibles
and reading plans, and the papal typesetter's Latin Modern, Junicode and FreeSerif
selection. Font programs remain external packages under their own licenses,
recorded in [THIRD_PARTY.md](../../THIRD_PARTY.md). No font copies or generated
PDFs are added to Git.

The image extends the existing immutable TeX Live baseline with the same
archive-pinned XeTeX and Latin-language packages as the manual print workflow.
It records installed package and engine versions in
`/usr/share/triptych-print/`. Two small build-time compilations check the native
font families, IPA, Greek, Cyrillic, liturgical signs and Latin hyphenation;
their font reports must show embedded subsets with Unicode maps. The probe
PDFs are discarded. Publishing and deploying the resulting image by
digest seals that complete layer; the older base-image digest alone does not.

Build from a **committed, pushed** source revision, from the repository root:

```sh
print_revision="$(git rev-parse HEAD)"
docker build --build-arg "SOURCE_REVISION=$print_revision" \
  --tag "triptych-native-print:$print_revision" containers/native-print
export TRIPTYCH_PRINT_TOOLCHAIN="$(docker image inspect \
  --format '{{.Id}}' "triptych-native-print:$print_revision")"
export TRIPTYCH_PRINT_IMAGE="$TRIPTYCH_PRINT_TOOLCHAIN"
docker compose -f containers/native-print/compose.yaml config
docker compose -f containers/native-print/compose.yaml up -d
```

The small build context contains only these packaging files. During the build,
Git fetches the exact public 40-character commit into `/app`; it does not copy
the local checkout, local Git configuration, credentials, or scratch files.
The service verifies the real source revision and tracked-file cleanliness.
The source revision must already contain `tools/native-print-service`.

For a registry deployment, publish the built image, pull its immutable digest
on the target, and set `TRIPTYCH_PRINT_IMAGE` to that digest reference. Set
`TRIPTYCH_PRINT_TOOLCHAIN` to the pulled image's full `sha256:` image ID, obtained
with `docker image inspect --format '{{.Id}}' "$TRIPTYCH_PRINT_IMAGE"`. This
binds the cache to the complete worker image without giving the service access
to the Docker socket or registry credentials.

The Compose service runs as numeric user 10001, with a read-only root
filesystem, two writable named volumes, one worker, and process, memory and CPU
limits. Both writable directories are initialized with that numeric owner in
the image. `/app/.scratch` holds native intermediates; `/var/lib/triptych-print`
holds the service cache and font caches. Replacing the container retains these
volumes; removing them discards reproducible products.

Only the host's loopback port 8080 is published. A TLS reverse proxy on the
host must forward the service routes to it. The internal Docker network
isolates runtime egress while retaining HTTP ingress through that proxy; do
not use `network_mode: none` for an HTTP listener. The default allowed browser
origin is `https://mystago.gy`. A different origin requires an explicit command
override. No request installs packages, downloads fonts or fetches repository
content.

This packaging does not create hosting, DNS or a public endpoint. Configure
and verify the actual TLS service before setting the website's print-service
endpoint. The image and Compose runtime need verification on a host with
Docker; a successful native build outside the image is not that verification.

Docker behavior follows its [Dockerfile reference](https://docs.docker.com/reference/dockerfile/),
[Compose service reference](https://docs.docker.com/reference/compose-file/services/)
and [internal-network definition](https://docs.docker.com/reference/compose-file/networks/#internal).
