import Lake
open Lake DSL

package «FormalProofs» {
  -- add package configuration options here
}

@[default_target]
lean_lib «FormalProofs» {
  -- add library configuration options here
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.8.0"
