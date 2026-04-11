import Lake
open Lake DSL

package «FormalMethods» {
  moreLinkArgs := #["-rdynamic"]
}

lean_lib «FormalMethods» {
  roots := #[`FormalMethods]
}

@[default_target]
lean_exe «formal_methods» {
  root := `Main
  supportInterpreter := true
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.8.0"
