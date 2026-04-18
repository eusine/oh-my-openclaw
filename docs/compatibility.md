# Compatibility Notes

## Current recommendation

For a live private workspace, do not flip the running system in one shot.

The safer path is:

1. extract a clean public repo
2. test the rebranded names and runtime paths in a clean sandbox
3. add compatibility aliases only where resume behavior truly depends on them
4. migrate the live workspace after the sandbox path is stable

## Why

Live workflows may depend on existing state paths, hook assumptions, and older naming conventions.
A hard rename can break resume behavior before you notice, especially when resumable state and bootstrap glue are involved.
