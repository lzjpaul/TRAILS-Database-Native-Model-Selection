/*
This file is auto generated by pgrx.

The ordering of items is not stable, it is driven by a dependency graph.
*/

-- src/lib.rs:15
-- pg_extension::hello_pg
CREATE  FUNCTION "hello_pg"(
    "task" TEXT /* alloc::string::String */
) RETURNS TEXT /* alloc::string::String */
    IMMUTABLE STRICT PARALLEL SAFE
LANGUAGE c /* Rust */
AS 'MODULE_PATHNAME', 'hello_pgrxdemo_wrapper';