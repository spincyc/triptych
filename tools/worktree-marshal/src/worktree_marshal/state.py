"""I/O-free run identity and state-location policy."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol


class StateProfile(Protocol):
    state_environment: str
    override_state_suffix: Sequence[str]
    default_state_parts: Sequence[str]


class StateRepository(Protocol):
    root: Path
    state_root: Path
    common_git_dir: Path


RUN_ID_RE = re.compile(r"^[0-9]{8}t[0-9]{6}z-[0-9a-f]{12}$")


def validate_run_id(
    run_id: str,
    *,
    pattern: Callable[[], Any],
    display_name: Callable[[], str],
    error_type: Callable[[], type[BaseException]],
) -> None:
    """Validate one syntactic run ID with a profile-aware diagnostic."""

    if not pattern().fullmatch(run_id):
        raise error_type()(f"invalid {display_name()} run ID")


def validate_manifest_core_paths(
    repository: StateRepository,
    manifest: Mapping[str, Any],
    *,
    run_state_test: Callable[[object], bool],
    retirement_states: set[str],
    path_factory: Callable[[str], Path],
    validate_temporary: Callable[[StateRepository, Mapping[str, Any]], Path],
    authenticate_temporary_parent: Callable[..., Any],
    worker_branch_prefix: Callable[[], str],
    object_id_pattern: Any,
    error_type: type[BaseException],
) -> str:
    """Validate core lifecycle, containment, branch, CWD, and base identity."""

    state = manifest.get("state")
    if not run_state_test(state):
        raise error_type("run manifest has an invalid lifecycle state")
    previous_state = manifest.get("integration_previous_state")
    if previous_state is not None and not run_state_test(previous_state):
        raise error_type(
            "run manifest has an invalid previous lifecycle state"
        )
    worktrees_root = (repository.state_root / "worktrees").resolve()
    worktree = path_factory(str(manifest.get("worktree", "")))
    if (
        not worktree.is_absolute()
        or worktree.parent.resolve() != worktrees_root
        or worktree.is_symlink()
    ):
        raise error_type("run manifest has an unsafe worktree path")
    run_id = manifest.get("run_id")
    tmp_root = (repository.state_root / "tmp").resolve()
    temporary = validate_temporary(repository, manifest)
    with authenticate_temporary_parent(repository, manifest):
        pass
    retirement_temporary = state in retirement_states or (
        state == "cleaned" and "retirement_completed_at" in manifest
    )
    unsafe_temporary = not retirement_temporary and (
        not temporary.is_absolute()
        or temporary.parent.resolve() != tmp_root
        or temporary.is_symlink()
    )
    if unsafe_temporary:
        raise error_type("run manifest has an unsafe temporary path")
    if worktree.name != run_id or temporary.name != run_id:
        raise error_type("run manifest paths do not match its run ID")
    if manifest.get("branch") != f"{worker_branch_prefix()}{run_id}":
        raise error_type("run manifest has an unexpected worker branch")
    relative_value = manifest.get("relative_cwd")
    if (
        not isinstance(relative_value, str)
        or not relative_value
        or "\0" in relative_value
    ):
        raise error_type(
            "run manifest has an unsafe relative working directory"
        )
    if relative_value != "." and (
        relative_value.startswith("/")
        or any(
            part in {"", ".", ".."}
            for part in relative_value.split("/")
        )
        or path_factory(relative_value).as_posix() != relative_value
    ):
        raise error_type(
            "run manifest has an unsafe relative working directory"
        )
    relative_cwd = path_factory(relative_value)
    try:
        child_cwd = (worktree / relative_cwd).resolve()
        child_cwd.relative_to(worktree.resolve())
    except (OSError, RuntimeError, ValueError) as exc:
        raise error_type(
            "run manifest working directory escapes its worktree"
        ) from exc
    control_root = path_factory(
        str(manifest.get("control_root", ""))
    )
    if (
        not control_root.is_absolute()
        or control_root.resolve() != repository.root
    ):
        raise error_type(
            "run manifest has an unexpected primary checkout"
        )
    base_sha = manifest.get("base_sha")
    if (
        not isinstance(base_sha, str)
        or not object_id_pattern.fullmatch(base_sha)
    ):
        raise error_type("run manifest has an invalid base commit")
    return state


def validate_manifest_checkpoint_fields(
    manifest: Mapping[str, Any],
    state: str,
    *,
    object_fields: Sequence[str],
    retirement_object_fields: Sequence[str],
    path_fields: Sequence[str],
    hash_fields: Sequence[str],
    retirement_timestamp_fields: Sequence[str],
    retirement_fields: Sequence[str],
    retirement_core_fields: Sequence[str],
    retirement_states: set[str],
    object_id_pattern: Any,
    hash_match: Callable[[str], Any],
    error_type: type[BaseException],
) -> None:
    """Validate integration and retirement checkpoint field structure."""

    for field in object_fields:
        value = manifest.get(field)
        if value is not None and (
            not isinstance(value, str) or not object_id_pattern.fullmatch(value)
        ):
            raise error_type(
                f"run manifest has an invalid {field.replace('_', ' ')}"
            )
    for field in retirement_object_fields:
        if field in manifest:
            value = manifest[field]
            if not isinstance(value, str) or not object_id_pattern.fullmatch(value):
                raise error_type(
                    f"run manifest has an invalid {field.replace('_', ' ')}"
                )
    for field in path_fields:
        paths = manifest.get(field)
        if paths is not None and (
            not isinstance(paths, list)
            or any(
                not isinstance(path, str)
                or not path
                or "\0" in path
                or path.startswith("/")
                or any(part in {"", ".", ".."} for part in path.split("/"))
                for path in paths
            )
        ):
            raise error_type(
                f"run manifest has invalid {field.replace('_', ' ')}"
            )
    for field in hash_fields:
        value = manifest.get(field)
        if value is not None and (
            not isinstance(value, str) or not hash_match(value)
        ):
            raise error_type(
                f"run manifest has an invalid {field.replace('_', ' ')}"
            )
    abort_mode = manifest.get("integration_abort_mode")
    if abort_mode is not None and (
        not isinstance(abort_mode, str)
        or abort_mode not in {"rebase", "precommit-rebase", "candidate"}
    ):
        raise error_type("run manifest has an invalid integration abort mode")
    manual_resolution = manifest.get("integration_manual_resolution")
    if manual_resolution is not None and manual_resolution is not True:
        raise error_type("run manifest has an invalid manual-resolution marker")
    source_anchor_created = manifest.get("integration_source_anchor_created")
    if source_anchor_created is not None and source_anchor_created is not True:
        raise error_type("run manifest has an invalid source-anchor marker")
    retirement_anchor_created = manifest.get("retirement_anchor_created")
    if retirement_anchor_created is not None and retirement_anchor_created is not True:
        raise error_type("run manifest has an invalid retirement-anchor marker")
    for field in retirement_timestamp_fields:
        if field in manifest and (
            not isinstance(manifest[field], str) or not manifest[field].strip()
        ):
            raise error_type(
                f"run manifest has an invalid {field.replace('_', ' ')}"
            )
    if "retirement_cleanup_warning" in manifest and (
        not isinstance(manifest["retirement_cleanup_warning"], str)
        or not manifest["retirement_cleanup_warning"].strip()
    ):
        raise error_type("run manifest has an invalid retirement cleanup warning")
    retirement_fields_present = any(field in manifest for field in retirement_fields)
    if state in retirement_states:
        if any(
            field not in manifest
            for field in (*retirement_core_fields, "retirement_started_at")
        ):
            raise error_type("run manifest has an incomplete retirement checkpoint")
        if state == "retirement-pending":
            if any(
                field in manifest
                for field in (
                    "retirement_worktree_removed_at",
                    "retirement_ref_transaction_committed_at",
                    "retirement_receipt_removed_at",
                    "retirement_completed_at",
                    "retirement_cleanup_warning",
                )
            ):
                raise error_type("run manifest has retirement cleanup data too early")
            cleanup_target_present = "retirement_cleanup_target_head" in manifest
            cleanup_started = "retirement_ref_cleanup_started_at" in manifest
            if cleanup_target_present != cleanup_started or (
                cleanup_target_present
                and manifest.get("retirement_anchor_created") is not True
            ):
                raise error_type(
                    "run manifest has an incomplete retirement cleanup checkpoint"
                )
        if state == "retirement-ref-cleanup-pending":
            if (
                manifest.get("retirement_anchor_created") is not True
                or "retirement_worktree_removed_at" not in manifest
                or "retirement_cleanup_target_head" not in manifest
                or "retirement_ref_cleanup_started_at" not in manifest
                or "retirement_completed_at" in manifest
                or (
                    "retirement_receipt_removed_at" in manifest
                    and "retirement_ref_transaction_committed_at" not in manifest
                )
            ):
                raise error_type(
                    "run manifest has an incomplete retirement cleanup checkpoint"
                )
    elif retirement_fields_present:
        if state != "cleaned" or "retirement_completed_at" not in manifest:
            raise error_type("run manifest has retirement data outside its lifecycle")
        if any(
            field not in manifest
            for field in (
                *retirement_core_fields,
                "retirement_cleanup_target_head",
                "retirement_started_at",
                "retirement_worktree_removed_at",
                "retirement_ref_cleanup_started_at",
                "retirement_ref_transaction_committed_at",
                "retirement_receipt_removed_at",
            )
        ) or (
            manifest.get("retirement_anchor_created") is not True
            or "retirement_cleanup_warning" in manifest
        ):
            raise error_type("run manifest has incomplete retired metadata")


def validate_exact_run_tmpdir(
    repository: StateRepository,
    manifest: Mapping[str, Any],
    *,
    validate_run_id: Callable[[], Callable[[str], None]],
    stringifier: Callable[[], Callable[[object], str]],
    error_type: Callable[[], type[BaseException]],
) -> Path:
    """Validate the manifest's exact lexical run temporary path."""

    run_id = manifest.get("run_id")
    if not isinstance(run_id, str):
        raise error_type()(
            "the retained run has no valid temporary-path identity"
        )
    validate_run_id()(run_id)
    expected = repository.state_root / "tmp" / run_id
    temporary_value = manifest.get("tmpdir")
    if (
        not isinstance(temporary_value, str)
        or temporary_value != stringifier()(expected)
    ):
        raise error_type()(
            "the temporary path is not the exact launcher path"
        )
    return expected


def load_manifest(
    repository: StateRepository,
    run_id: str,
    *,
    validate_run_id: Callable[[], Callable[[str], None]],
    manifest_path: Callable[[], Callable[[StateRepository, str], Path]],
    json_loads: Callable[[], Callable[[str], Any]],
    file_not_found_error_type: Callable[[], type[BaseException]],
    os_error_type: Callable[[], type[BaseException]],
    decode_error_type: Callable[[], type[BaseException]],
    active_profile: Callable[[], Any],
    validate_manifest_paths: Callable[
        [],
        Callable[[StateRepository, dict[str, Any]], None],
    ],
    stringifier: Callable[[], Callable[[object], str]],
    error_type: Callable[[], type[BaseException]],
) -> dict[str, Any]:
    """Load and authenticate one profile-bound repository manifest."""

    validate_run_id()(run_id)
    path = manifest_path()(repository, run_id)
    try:
        manifest = json_loads()(path.read_text(encoding="utf-8"))
    except file_not_found_error_type() as exc:
        raise error_type()(
            f"unknown {active_profile().display_name} run {run_id}"
        ) from exc
    except (os_error_type(), decode_error_type()) as exc:
        raise error_type()(f"cannot read run {run_id}: {exc}") from exc
    profile = active_profile()
    if (
        manifest.get("schema_version") != profile.schema_version
        or manifest.get("run_id") != run_id
        or not profile.validate_manifest_identity(manifest)
    ):
        raise error_type()(f"run {run_id} has an invalid manifest")
    expected_common = stringifier()(repository.common_git_dir)
    if manifest.get("common_git_dir") != expected_common:
        raise error_type()(
            f"run {run_id} belongs to a different repository"
        )
    validate_manifest_paths()(repository, manifest)
    return manifest


def write_manifest(
    repository: StateRepository,
    manifest: dict[str, Any],
    *,
    validate_run_id: Callable[[], Callable[[str], None]],
    current_timestamp: Callable[[], Callable[[], str]],
    manifest_path: Callable[[], Callable[[StateRepository, str], Path]],
    private_directory: Callable[[], Callable[[Path], None]],
    make_temporary: Callable[[], Callable[..., tuple[int, str]]],
    path_factory: Callable[[], Callable[[str], Path]],
    descriptor_chmod: Callable[[], Callable[[int, int], None]],
    descriptor_open: Callable[[], Callable[..., Any]],
    json_dump: Callable[[], Callable[..., None]],
    replace_path: Callable[[], Callable[[Path, Path], None]],
    directory_open: Callable[[], Callable[[Path, int], int]],
    read_only_flag: Callable[[], int],
    directory_flag: Callable[[], int],
    descriptor_sync: Callable[[], Callable[[int], None]],
    descriptor_close: Callable[[], Callable[[int], None]],
    error_type: Callable[[], type[BaseException]],
) -> None:
    """Atomically persist one manifest and synchronize its directory."""

    run_id = manifest.get("run_id")
    if not isinstance(run_id, str):
        raise error_type()("internal manifest has no run ID")
    validate_run_id()(run_id)
    manifest["updated_at"] = current_timestamp()()
    target = manifest_path()(repository, run_id)
    private_directory()(target.parent)
    descriptor, temporary_name = make_temporary()(
        prefix=f".{run_id}.",
        suffix=".tmp",
        dir=target.parent,
        text=True,
    )
    temporary = path_factory()(temporary_name)
    try:
        descriptor_chmod()(descriptor, 0o600)
        with descriptor_open()(
            descriptor,
            "w",
            encoding="utf-8",
        ) as stream:
            json_dump()(manifest, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            descriptor_sync()(stream.fileno())
        replace_path()(temporary, target)
        directory_descriptor = directory_open()(
            target.parent,
            read_only_flag() | directory_flag(),
        )
        try:
            descriptor_sync()(directory_descriptor)
        finally:
            descriptor_close()(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def private_directory(
    path: Path,
    *,
    os_error_type: Callable[[], type[BaseException]],
    error_type: Callable[[], type[BaseException]],
    directory_test: Callable[[], Callable[[int], bool]],
    flag_lookup: Callable[[], Callable[[str, int], int]],
    read_only_flag: Callable[[], int],
    file_open: Callable[[], Callable[[Path, int], int]],
    file_stat: Callable[[], Callable[[int], object]],
    same_stat: Callable[[], Callable[[object, object], bool]],
    file_chmod: Callable[[], Callable[[int, int], None]],
    file_close: Callable[[], Callable[[int], None]],
) -> None:
    """Create and descriptor-authenticate one private state directory."""

    try:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        metadata = path.lstat()
    except os_error_type() as exc:
        raise error_type()(
            "cannot create or inspect a private launcher directory"
        ) from exc
    if not directory_test()(metadata.st_mode):
        raise error_type()("a private launcher path is not a real directory")
    directory_flag = flag_lookup()("O_DIRECTORY", 0)
    nofollow_flag = flag_lookup()("O_NOFOLLOW", 0)
    if not directory_flag or not nofollow_flag:
        raise error_type()(
            "safe private launcher directory setup is unavailable"
        )
    try:
        descriptor = file_open()(
            path,
            read_only_flag()
            | directory_flag
            | nofollow_flag
            | flag_lookup()("O_CLOEXEC", 0),
        )
    except os_error_type() as exc:
        raise error_type()(
            "cannot open a private launcher directory safely"
        ) from exc
    try:
        opened = file_stat()(descriptor)
        if (
            not directory_test()(opened.st_mode)
            or not same_stat()(metadata, opened)
        ):
            raise error_type()(
                "a private launcher directory changed during setup"
            )
        file_chmod()(descriptor, 0o700)
    except os_error_type() as exc:
        raise error_type()(
            "cannot authenticate a private launcher directory"
        ) from exc
    finally:
        file_close()(descriptor)


def new_run_id(
    *,
    current_time: Callable[[], datetime],
    random_suffix: Callable[[], str],
) -> str:
    """Generate one run ID from explicit clock and entropy providers."""

    stamp = current_time().strftime("%Y%m%dt%H%M%Sz").lower()
    return f"{stamp}-{random_suffix()}"


def state_base(
    *,
    profile: StateProfile,
    environment: Callable[[], Mapping[str, str]],
    path_factory: Callable[[str], Path],
    home: Callable[[], Path],
    error_type: Callable[[], type[Exception]],
) -> Path:
    """Select the state base from explicit profile and environment providers."""

    override = environment().get(profile.state_environment)
    if override:
        candidate = path_factory(override)
        if not candidate.is_absolute():
            raise error_type()(
                f"{profile.state_environment} must be an absolute path"
            )
        return candidate.joinpath(*profile.override_state_suffix)

    xdg_state = environment().get("XDG_STATE_HOME")
    if xdg_state:
        candidate = path_factory(xdg_state)
        if not candidate.is_absolute():
            raise error_type()("XDG_STATE_HOME must be an absolute path")
        return candidate.joinpath(*profile.default_state_parts)
    return (home() / ".local" / "state").joinpath(
        *profile.default_state_parts
    )


def repository_slug(
    root: Path,
    *,
    substitute: Callable[[str, str, str], str],
) -> str:
    """Normalize a repository basename for its state-directory prefix."""

    slug = substitute(r"[^a-z0-9]+", "-", root.name.lower()).strip("-")
    return slug or "repository"


def repo_lock_path(state_root: Path) -> Path:
    return state_root / "repository.lock"


def run_lock_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.lock"


def manifest_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.json"
